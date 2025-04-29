from mcstatus import JavaServer
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from pymongo import MongoClient

class Player:
    def __init__(self, name, uuid, join_time=None, left_time=None):
        self.name = name
        self.id = uuid
        self.join_time = join_time
        self.left_time = left_time
    
    def __str__(self):
        return f"{self.name}:{self.id}:join_time {self.join_time}:left_time {self.left_time}:"
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

EVENT_TYPE = {
    "PLAYER_JOIN": 0,
    "PLAYER_LEAVE": 1,
    "NEW_PLAYER": 2
}

EVENT_TYPE_REV_MAP = {
    EVENT_TYPE["PLAYER_JOIN"]: "PLAYER_JOIN",
    EVENT_TYPE["PLAYER_LEAVE"]: "PLAYER_LEAVE",
    EVENT_TYPE["NEW_PLAYER"]: "NEW_PLAYER"
}

load_dotenv()

MONGO_STRING = os.getenv("MONGO_STRING")
MC_SERVER_IP = os.getenv("MC_SERVER_IP")
DB_NAME = os.getenv("MONGO_DATABASE_NAME")

SLEEP_TIME = 60

client = MongoClient(MONGO_STRING)
db = client[DB_NAME]

#global collections.
player_sessions = db.get_collection("player_sessions")
player_events = db.get_collection("player_events")
server_status = db.get_collection("server_status")
players = db.get_collection("Players")

def create_session(player, join_timestamp, leave_timestamp):
    play_time_minutes = round(calculate_playtime(join_timestamp, leave_timestamp))
    player_sessions.insert_one({
        "session_info": {
            "player_id": player.id,
            "player_name": player.name
        },
        "left_timestamp": leave_timestamp,
        "join_timestamp": join_timestamp,
        "play_time": play_time_minutes,
    })

def create_event(player, event_type, event_timestamp):
    player_events.insert_one({
        "timestamp": event_timestamp,
        "event_type": EVENT_TYPE_REV_MAP[event_type],
        "event_info": {
            "player_name": player.name,
            "player_id": str(player.id),
        }
    })
def create_server_status(player_count, player_list, timestamp):
    server_status.insert_one({
        "timestamp": timestamp,
        "player_list": player_list,
        "player_count": player_count
    })

def create_player(player, join_timestamp):
    players.insert_one({
        "_id": str(player.id),
        "player_name": player.name,
        "first_joined": join_timestamp,
        "last_seen": join_timestamp,
        "play_time": 0,
    })

def update_player(player, join_timestamp, leave_timestamp):
    play_time_minutes = round(calculate_playtime(join_timestamp, leave_timestamp))
    players.update_one(
        {"_id": str(player.id)},
        {
            "$inc": {"play_time": play_time_minutes},
            "$set": {"last_seen": leave_timestamp}
        }
    )

def calculate_playtime(isotime_start:datetime, isotime_end:datetime):
    duration = isotime_end - isotime_start
    total_minutes = duration.total_seconds() / 60
    return total_minutes

def player_exists(player_id):
    return players.find_one({"_id": str(player_id)}) is not None

def log_event(eventType, player_obj, timestamp):

    if eventType == EVENT_TYPE["PLAYER_JOIN"]:
        if not player_exists(player_obj.id):
            create_player(player_obj, timestamp)
            create_event(player_obj, EVENT_TYPE["NEW_PLAYER"], timestamp)

    elif eventType == EVENT_TYPE["PLAYER_LEAVE"]:
        update_player(player_obj, player_obj.join_time, timestamp)
        create_session(player_obj, player_obj.join_time, timestamp)

    create_event(player_obj, eventType, timestamp)

def main():
    # set of Player instances
    last_players_online = set()
    player_map = {}

    try:
        while True:
            try:
                #Get server object and status object to query the server.
                server = JavaServer.lookup(address=MC_SERVER_IP, timeout=10)
                status = server.status()
                current_time = datetime.now(timezone.utc)

                # get sampled list of players currently online then map them to a player object inside a set.
                current_sample = status.players.sample or []
                online_players = status.players.online
                current_players = {Player(p.name, p.id) for p in current_sample}
                
                # determine the recently joined players vs the players that left.
                joined_now = current_players - last_players_online
                left_now = last_players_online - current_players

                if joined_now or left_now:
                    print(f"[{current_time.isoformat()}] Server IP: {server.address}\tPlayers Online: {status.players.online}")
                    print("Players:", [p.name for p in current_players])

                    #log player list and count to server_session:
                    create_server_status(online_players, [{"player_name": p.name, "player_id": p.id} for p in current_players], current_time)

                # create event for joined players
                # save them locally in memory
                for player in joined_now:

                    if player.name not in player_map:
                        player_map[player.name] = player
                        player.join_time = current_time
                        print(f"[{current_time}] {player.name} joined.")
                        log_event(EVENT_TYPE["PLAYER_JOIN"], player, current_time)
                            

                #create leave event / session for each left players.
                for player in left_now:

                    leaving_player = player_map.get(player.name)
                    if leaving_player == None:
                        print(f"[{current_time.isoformat()}] [WARNING] player: {player.name} was not in the player_map")
                    else:

                        leaving_player.left_time = current_time

                        log_event(EVENT_TYPE["PLAYER_LEAVE"], leaving_player, current_time)
                        print(f"[{current_time.isoformat()}] {leaving_player.name} left the server.")
                        player_map.pop(player.name, None)

                last_players_online = current_players.copy()

            except Exception as e:
                print(f"[{datetime.now(timezone.utc).isoformat()}] Error: {e}")
            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        for player in player_map.values():
            print(f"Logging leave event for {player.name} due to shutdown.")
            log_event(EVENT_TYPE["PLAYER_LEAVE"], player, datetime.now(tz=timezone.utc))

if __name__ == "__main__":
    main()

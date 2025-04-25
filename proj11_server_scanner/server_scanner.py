from mcstatus import JavaServer
import time
import os
from datetime import datetime, timezone
from pymongo import MongoClient

class Player:
    def __init__(self, name, uuid, join_time=None, left_time=None):
        self.name = name
        self.id = uuid
        self.join_time = join_time
        self.left_time = left_time
    
    def __str__(self):
        return f"{self.name}:{self.id}"
    
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

MONGO_STRING = os.getenv("MONGO_STRING")
SLEEP_TIME = 60

client = MongoClient(MONGO_STRING)
db = client["Peters-Minecraft-Server"]

def create_session(player, join_timestamp, leave_timestamp):
    player_sessions = db.get_collection("player_sessions")
    play_time_minutes = round(calculate_playtime(join_timestamp.isoformat(), leave_timestamp.isoformat()))
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
    events = db.get_collection("player_events")
    events.insert_one({
        "timestamp": event_timestamp,
        "event_type": EVENT_TYPE_REV_MAP[event_type],
        "event_info": {
            "player_name": player.name,
            "player_id": str(player.id),
        }
    })

def create_player(player, join_timestamp):
    players = db.get_collection("Players")
    players.insert_one({
        "_id": str(player.id),
        "player_name": player.name,
        "first_joined": join_timestamp,
        "last_seen": join_timestamp,
        "play_time": 0,
    })

def update_player(player, join_timestamp, leave_timestamp):
    players = db.get_collection("Players")
    play_time_minutes = round(calculate_playtime(join_timestamp.isoformat(), leave_timestamp.isoformat()))
    players.update_one(
        {"_id": str(player.id)},
        {
            "$inc": {"play_time": play_time_minutes},
            "$set": {"last_seen": leave_timestamp}
        }
    )

def calculate_playtime(isotime_start, isotime_end):
    start = datetime.fromisoformat(isotime_start)
    end = datetime.fromisoformat(isotime_end)
    duration = end - start
    total_minutes = duration.total_seconds() / 60
    return total_minutes

def player_exists(player_id):
    players = db.get_collection("Players")
    return players.find_one({"_id": str(player_id)}) is not None

def log_event(eventType, player_obj, timestamp):
    if eventType == EVENT_TYPE["NEW_PLAYER"]:
        if player_exists(player_obj.id):
            return
        create_player(player_obj, timestamp)

    elif eventType == EVENT_TYPE["PLAYER_JOIN"]:
        pass

    elif eventType == EVENT_TYPE["PLAYER_LEAVE"]:
        update_player(player_obj, player_obj.join_time, timestamp)
        create_session(player_obj, player_obj.join_time, timestamp)

    create_event(player_obj, eventType, timestamp)

def main():
    player_map = {}  # maps name -> Player
    currently_online = set()  # set of Player instances
    last_players_online = set()

    try:
        while True:
            try:
                server = JavaServer.lookup(address="184.16.77.172:25565", timeout=10)
                status = server.status()
                current_time = datetime.now(timezone.utc)

                current_sample = status.players.sample or []
                current_players = {Player(p.name, p.id) for p in current_sample}

                joined_now = current_players - last_players_online
                left_now = last_players_online - current_players

                if joined_now or left_now:
                    print(f"[{current_time.isoformat()}] Server IP: {server.address}\tPlayers Online: {status.players.online}")
                    print("Players:", [p.name for p in current_players])

                for player in joined_now:
                    if player.name not in player_map:
                        player.join_time = current_time
                        player_map[player.name] = player
                        log_event(EVENT_TYPE["NEW_PLAYER"], player, current_time)
                    else:
                        player_map[player.name].join_time = current_time

                    currently_online.add(player_map[player.name])
                    log_event(EVENT_TYPE["PLAYER_JOIN"], player_map[player.name], current_time)
                    print(f"[{current_time}] {player.name} joined.")

                for player in left_now:
                    if player.name in player_map:
                        player_map[player.name].left_time = current_time
                        log_event(EVENT_TYPE["PLAYER_LEAVE"], player_map[player.name], current_time)
                        print(f"[{current_time.isoformat()}] {player.name} left the server.")
                        currently_online.discard(player_map[player.name])

                last_players_online = current_players

            except Exception as e:
                print(f"[{datetime.now(timezone.utc).isoformat()}] Error: {e}")

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        for player in currently_online:
            print(f"Logging leave event for {player.name} due to shutdown.")
            log_event(EVENT_TYPE["PLAYER_LEAVE"], player, datetime.now())

if __name__ == "__main__":
    main()

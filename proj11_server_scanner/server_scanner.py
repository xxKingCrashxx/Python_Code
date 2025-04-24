from mcstatus import JavaServer
import time
import os
from datetime import datetime
from pymongo import MongoClient

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

    player_sessions = db.get_collection("player_sessions_timeseries")
    play_time_minutes = round(calculate_playtime(join_timestamp.isoformat(), leave_timestamp.isoformat()))
    player_sessions.insert_one({
            "session_info": {
                "play_time": play_time_minutes,
                "player": {
                    "player_id": player["player"].id, 
                    "player_name": player["player"].name
                },
                "left_timestamp": leave_timestamp
            },
            "join_timestamp": join_timestamp, 
        })

def create_event(player, event_type, event_timestamp):
    events = db.get_collection("player_events_timeseries")
    events.insert_one({
            "timestamp": event_timestamp,
            "event_info": {
                "player_name": player["player"].name,
                "player_id": str(player["player"].id),
                "event_type": EVENT_TYPE_REV_MAP[event_type],
            }
    })

def create_player(player, join_timestamp):
    players = db.get_collection("Players")
    if player_exists(player["player"].id):
            return
        
    players.insert_one({
        "_id": str(player["player"].id),
        "player_name": player["player"].name,
        "first_joined": join_timestamp,
        "last_seen": join_timestamp,
        "play_time": 0,
    })

def update_player(player, join_timestamp, leave_timestamp):
     players = db.get_collection("Players")
     play_time_minutes = round(calculate_playtime(join_timestamp.isoformat(), leave_timestamp.isoformat()))
     players.update_one(
            {"_id": str(player["player"].id)},
            {
                "$inc": {"play_time": play_time_minutes}, 
                "$set": {"last_seen":leave_timestamp}
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
    player = players.find_one({
        "_id": str(player_id)
    })

    if player is not None:
            return True
    return False
    
def log_event(eventType, player, timestamp ):

    if eventType == EVENT_TYPE["NEW_PLAYER"]:
        # player_map stored in memory may not have all the players, check db before writing the new_player event.
        create_player(player, timestamp)

    elif eventType == EVENT_TYPE["PLAYER_JOIN"]:
        pass

    elif eventType == EVENT_TYPE["PLAYER_LEAVE"]:
        update_player(player, timestamp)
        create_session(player, player["joined_at"], timestamp)

    # regardless of what event it is, log it into the database. 
    create_event(player, eventType, timestamp)
    
    
def main():
    player_map = {}
    currently_online_map = {}
    last_players_online = set()
    
    try:
        while True:
            try:
                server = JavaServer.lookup(address="184.16.77.172:25565", timeout=10)
                status = server.status()
                current_time = datetime.now()

                current_sample = status.players.sample or []
                current_players_online = set(p.name for p in current_sample)

                joined_now = current_players_online - last_players_online
                left_now = last_players_online - current_players_online

                if joined_now or left_now:
                    print(f"[{current_time.isoformat()}] Server IP: {server.address}\tPlayers Online: {status.players.online}")
                    print("Players:", [p.name for p in current_sample])

                for player in current_sample:
                    if player.name in joined_now:
                        if player.name not in player_map:
                            player_map[player.name] = {
                                "player": player,
                                "joined_at": current_time,
                                "left_at": None
                            }
                            log_event(EVENT_TYPE["NEW_PLAYER"], player_map[player.name], current_time)

                        print(f"[{current_time}] {player.name} joined.")
                        player_map[player.name]["joined_at"] = current_time
                        currently_online_map[player.name] = player_map[player.name];
                        log_event(EVENT_TYPE["PLAYER_JOIN"], player_map[player.name], current_time)
                    

                for name in left_now:
                    player_map[name]["left_at"] = current_time
                    log_event(EVENT_TYPE["PLAYER_LEAVE"], player_map[name], current_time)
                    currently_online_map.pop(name, None)
                    print(f"[{current_time.isoformat()}] {name} left the server.")

                last_players_online = current_players_online
            except Exception as e:
                print(f"[{datetime.now().isoformat()}] Error: {e}")

            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        for name, player in currently_online_map.items():
            print(f"Logging leave event for {name} due to shutdown.")
            log_event(EVENT_TYPE["PLAYER_LEAVE"], player, datetime.now())
    

if __name__ == "__main__":
    main()
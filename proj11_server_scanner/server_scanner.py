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
def calculate_playtime(isotime_start, isotime_end):
    start = datetime.fromisoformat(isotime_start)
    end = datetime.fromisoformat(isotime_end)

    duration = end - start
    total_minutes = duration.total_seconds() / 60
    return total_minutes 

def log_event(eventType, player, timestamp_string ):

    events = db.get_collection("player_events")
    if eventType == EVENT_TYPE["NEW_PLAYER"]:
        players = db.get_collection("Players")
        player = players.find_one({
            "_id": str(player[player].id)
        })

        if player is not None:
            return
        
        players.insert_one({
            "_id": str(player["player"].id),
            "player_name": player["player"].name,
            "first_joined": timestamp_string,
            "play_time": 0,
        })

    if eventType == EVENT_TYPE["PLAYER_LEAVE"]:
        players = db.get_collection("Players")
        players.update_one(
            {"_id": str(player["player"].id)},
            {
                "$inc": {"play_time": calculate_playtime(player["joined_at"], timestamp_string)}, 
                "$set": {"last_seen":timestamp_string}
            }
        )
        player_sessions = db.get_collection("player_sessions")
        player_sessions.insert_one({
            "play_time": calculate_playtime(player["joined_at"], timestamp_string),
            "player": {"player_id": player["player"].id, 
                       "player_name": player["player"].name},
            "join_timestamp": player["joined_at"],
            "left_timestamp": timestamp_string
        })

    events.insert_one({
            "player_name": player["player"].name,
            "player_id": str(player["player"].id),
            "event_type": EVENT_TYPE_REV_MAP[eventType],
            "timestamp": timestamp_string,
    })

    
    


    
def main():
    player_map = {}
    last_players_online = set()
    
    while True:
        try:
            server = JavaServer.lookup(address="184.16.77.172:25565", timeout=10)
            status = server.status()
            current_time = datetime.now().isoformat()

            current_sample = status.players.sample or []
            current_players_online = set(p.name for p in current_sample)

            joined_now = current_players_online - last_players_online
            left_now = last_players_online - current_players_online

            if joined_now or left_now:
                print(f"[{current_time}] Server IP: {server.address}\tPlayers Online: {status.players.online}")
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
                    log_event(EVENT_TYPE["PLAYER_JOIN"], player_map[player.name], current_time)
                    

            for name in left_now:
                player_map[name]["left_at"] = current_time
                log_event(EVENT_TYPE["PLAYER_LEAVE"], player_map[name], current_time)
                print(f"[{current_time}] {name} left the server.")


            last_players_online = current_players_online
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Error: {e}")

        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
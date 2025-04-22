from mcstatus import JavaServer
import time
from datetime import datetime


SLEEP_TIME = 60
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
                            "uuid": str(player.id),
                            "online": [current_time],
                            "joined": 1
                        }
                    else:
                        player_map[player.name]["online"].append(current_time)
                        player_map[player.name]["joined"] += 1
                    print(f"[{current_time}] {player.name} joined.")

            for name in left_now:
                print(f"[{current_time}] {name} left the server.")

            last_players_online = current_players_online
            print(player_map)
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Error: {e}")

        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
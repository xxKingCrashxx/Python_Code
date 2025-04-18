#Author: King_Crash
#Date: 14 April 2025

from shutil import make_archive 
import sys
import platform
from datetime import date
from os import path, listdir, remove, stat
from mcrcon import MCRcon
import socket
import time
import subprocess

#change variables as needed.
#Config
SRC_DIR = r"" 		#		probably the absolute directory to the minecraft server.
DEST_DIR = r"" 		# 		absolute directory to where you wish to store the backups.
MAX_BACKUPS = 10 	#		max number of backups to keep until script starts replacing older backups.
SERVER_HOST = ""	#		IP of the minecraft server.
SERVER_PORT = 25565	#		Port of the minecraft server. *default 25565*
RCON_PORT = 25575	#		Rcon port of the minecraft server. *make sure to enable rcon in the server.properties file*
RCON_PASSWORD = r""	#		Rcon password to access server. *make it complicated, set-up is in server.properties file*
START_COMMAND = r""	#		typically the bat file you used to start up the minecraft server with certain java arguments.
TIMEOUT = 60

host_platform = platform.system()

#helper function that gets the st_ctime of all the zip files located in the DEST_DIR
#searches for the dir with the smallest "existence" time and stores it in a new list
#function returns the dir with the oldest time using the max_existence
def get_oldest_backup(dirs: list) -> str: 
	dir_existence_time = [None] * len(dirs)
	min_existence = sys.float_info.max

	for i, dir in enumerate(dirs):
		res = stat(DEST_DIR + "\\" + dir).st_ctime
		dir_existence_time[i] = res

		if min_existence > res:
			min_existence = res
	old_dir_index = dir_existence_time.index(min_existence)
	return dirs[old_dir_index]


# simple function that utilizes sockets and attempts to create a connection
# with the minecraft port. If it cannot make a connection, the assumption is
# that the minecraft server is not up and/or listening on that port.
def is_server_up() -> bool:
	try:
		with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=2):
			return True
	except (ConnectionRefusedError, socket.timeout, OSError):
		return False


def stop_server():
	try:
		print("[INFO] Sending RCON Stop command...")
		with MCRcon(SERVER_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
			mcr.command("say [BACK UP] Server backup script starting, please leave the server...")

			count_start = 10
			while count_start != 0:
				mcr.command(f"say [BACK UP] Server Restarting in: {count_start}")
				count_start = count_start - 1
				time.sleep(1)
			mcr.command("say [BACK UP] Server is closing...")
			mcr.command("save-all")
			mcr.command("stop")
	except Exception as e:
		print(f"[ERROR] Failed to send RCON command {e}")
		exit(1)

	# wait for server to fully shut down.
	start_time = time.time()
	while is_server_up():
		if time.time() - start_time > TIMEOUT:
			print("[ERROR] Timeout Reached. Server is still up.")
			exit(1)
		time.sleep(2)
	print("[INFO] Server is offline.")


def restart_server():
	print("[INFO] Restarting Server...")
	try:
		match host_platform:
			case "Windows":
				subprocess.Popen(
					["cmd.exe", "/k", START_COMMAND],
					cwd=SRC_DIR
				)
			case "Linux":
				subprocess.Popen(START_COMMAND, cwd=SRC_DIR, shell=True)
			case _:
				print("[ERROR] Unsupported os.")
				exit(1)
	except Exception as e:
		print(f"[ERROR] Failed to start server: {e}")
		exit(1)
	print("[INFO] Server has restarted successfully.")

def backup_folder():
	backup_file_name = "backup-" + str(date.today())
	backup_file_dir = DEST_DIR + "\\" + backup_file_name

	if not path.exists(SRC_DIR):
		print(f"directory: {SRC_DIR} does not exist")
		exit(-1)

	if not path.exists(DEST_DIR):
		print(f"directory: {DEST_DIR} does not exist")
		exit(-1)

	dirs = listdir(DEST_DIR)
	if MAX_BACKUPS <= len(dirs):
		old_dir = get_oldest_backup(dirs)
		remove(DEST_DIR + "\\" + dirs.pop(dirs.index(old_dir)))

	if (backup_file_name + ".zip") in dirs:
			remove((backup_file_dir + ".zip"))

	make_archive(base_name=backup_file_dir, format="zip", root_dir=SRC_DIR)
	print(f"[INFO] backup: {backup_file_name}.zip has been successfully created on {str(date.today())}")

def main():
	stop_server()
	backup_folder()
	restart_server()

if __name__ == '__main__':
	main()

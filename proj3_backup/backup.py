#Author: King_Crash
#Date: 9 May 2022

from shutil import make_archive 
import sys
from datetime import date
from os import path, listdir, remove, stat

#variables that represent the src directory and destination directory.
#change variables as needed.
SRC_DIR = r"C:\Users\ajdec\Desktop\1.18_minecraft_server\world"
DEST_DIR = r"C:\Users\ajdec\Desktop\1.18_minecraft_server\backups"
MAX_BACKUPS = 10

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

def main():
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
		#old_dir_backup = DEST_DIR + "\\" + old_dir
		remove(DEST_DIR + "\\" + dirs.pop(dirs.index(old_dir)))
		
	if (backup_file_name + ".zip") in dirs:
			remove((backup_file_dir + ".zip"))

	make_archive(base_name=backup_file_dir, format="zip", root_dir=SRC_DIR)
	print(f"backup: {backup_file_name}.zip has been successfully created on {str(date.today())}")

if __name__ == '__main__':
	main()
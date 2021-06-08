from pathlib import Path
from datetime import datetime
import sys, exifread, time, shutil

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
FILETYPES = ['.png', '.jpg', '.arw', '.nef', '.mp4', '.wav', '.mp3']
LOGO='''
    ____  __________________  _______________   __
   / __ \/ ____/ ____/ __ \ \/ / ____/ ____/ | / /
  / / / / __/ / __/ / /_/ /\  / __/ / __/ /  |/ / 
 / /_/ / /___/ /___/ _, _/ / / /___/ /___/ /|  /  
/_____/_____/_____/_/ |_| /_/_____/_____/_/ |_/   
                                                  '''
filecount = 0
copycount = 0

def get_date(file: Path):
	try:
		f = open(file, 'rb')
	except PermissionError:
		raise

	exifdata = exifread.process_file(f, stop_tag='Image DateTime')
	f.close()
	if exifdata.get('Image DateTime') == None: # If I can't find any EXIF data...
		file_stats = file.stat()
		file_ctime = file_stats.st_mtime
		formatted_ctime = datetime.strptime(time.ctime(file_ctime), '%a %b %d %H:%M:%S %Y')
		return str(formatted_ctime).replace(':', '-').split(' ')
	
	return str(exifdata.get('Image DateTime')).replace(':', '-').split(' ')

def create_dirs(target):
	if target.is_dir():
		return
	else:
		print(f"The target \"{target}\" doesn't exist, creating...")
		try:
			target.mkdir()
			return
		except PermissionError:
			raise

if __name__ == "__main__":
	for element in input_path.glob('**/*'):
		if element.is_dir():
			print("Found dir, skipping...")
			continue

		filecount = filecount+1
		if not element.suffix.lower() in FILETYPES:
			print(f"WARNING: {element.name} isn't a supported filetype.")
			continue

		file_date = None
		try:
			file_date = get_date(element)
		except PermissionError:
			print(f"WARNING: Couldn't open {element}; PermissionError")
			continue
		
		target_path = Path(output_path, file_date[0])
		try:
			create_dirs(target_path)
		except PermissionError:
			print(f"WARNING: Couldn't create target directory \"{target_path}\"; Permission Error")
			continue

		if Path(target_path,element.name).exists():
			print(f"File {element.name} already exists in target folder. Skipping...")
			continue

		try:
			print(f"Copying {element.name} to {target_path}")
			shutil.copy(element, target_path)
		except PermissionError:
			print(f"WARNING: Couldn't copy file to target directory; PermissionError")
			continue

		copycount = copycount+1

	print(f"\n\nFinished! Stats:\n  Files Scanned:  {filecount}\n  Files Copied:  {copycount}")
	print("\n\n Thank you for using me! :D")
	print(LOGO)
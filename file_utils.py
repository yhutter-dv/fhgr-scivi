def get_last_part_of_path(path):
	# Returns the last part of a file path. e.g /data/foo/bar/baz => baz
	return os.path.basename(os.path.normpath(path))
import os
import glob
import pathlib

def get_subdirectories(path):
	return [ f.path for f in os.scandir(path) if f.is_dir() ]

def get_files(path, file_extension):
	return [ f for f in glob.glob(f'{path}/*.{file_extension}') ]

def get_file_name_without_extension(file_path):
	return pathlib.Path(file_path).stem

def panic_if_file_not_exists(file_path):
	if not os.path.exists(file_path):
		sys.exit(f"Expected file {file_path} to exist but it was not there...")

def ensure_directory(directory_path):
	if not os.path.exists(directory_path):
		print(f"Expected directory {directory_path} to be available but it was not, it will be created now...")
		os.makedirs(directory_path)


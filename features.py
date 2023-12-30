from paths import * 
from file_utils import get_subdirectories, get_last_part_of_path

def get_feature_file_paths():
	return get_subdirectories(FEATURES_DIRECTORY_PATH)

def get_feature_names():
	return [ get_last_part_of_path(path) for path in get_feature_file_paths() ]
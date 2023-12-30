from rich.console import Console
from PIL import Image
import os

from features import get_feature_file_paths, get_feature_names
from file_utils import ensure_directory, get_files, get_file_name_without_extension

# Global variables
PREVIEW_IMAGES_FOLDER_NAME = "preview_images"
GIF_FOLDER_NAME = "gifs"
KEY_FRAME = 0 # Extract first frame

console = Console()

def create_preview_image_from_gif(gif_file_path, preview_image_name, preview_image_full_path):
	with Image.open(gif_file_path) as f:
		f.seek(KEY_FRAME)
		f.save(preview_image_full_path)



if __name__ == "__main__":
	feature_file_paths = get_feature_file_paths()
	feature_names = get_feature_names()

	print("Found the following features and file paths")
	for feature_name, file_path in zip(feature_names, feature_file_paths):
		print(f"{feature_name} => {file_path}")

	for index, feature_path in enumerate(feature_file_paths):
		feature_name = feature_names[index]
		preview_images_folder_path = os.path.join(feature_path, PREVIEW_IMAGES_FOLDER_NAME)
		gifs_folder_path = os.path.join(feature_path, GIF_FOLDER_NAME)

		ensure_directory(preview_images_folder_path)

		if not os.path.isdir(gifs_folder_path):
			print(f"Could not find gif folder, expected path was {gifs_folder_path}")
			print(f"Skipping...")
			continue

		gif_files = get_files(gifs_folder_path, "gif")
		print(gif_files)
		if len(gif_files) == 0:
			print(f"Did not find any matching gif files make sure you have some files with extension .gif inside the directory {gifs_folder_path}")
			print("Skipping...")
			continue

		print("Found the following gif files ", gif_files)

		# Iterate through all the found gif files and generate a preview image
		for gif_file_path in gif_files:
			with console.status(f"Creating preview images from gif files for {feature_name}") as status:
				try:
					gif_file_name_without_extension = get_file_name_without_extension(gif_file_path)
					
					preview_image_name = f"{gif_file_name_without_extension}.png"
					preview_image_full_path = os.path.join(preview_images_folder_path, preview_image_name)

					create_preview_image_from_gif(gif_file_path, preview_image_name, preview_image_full_path)
				except Exception as e:
					print(f"Failed to create preview images due to error {e}")


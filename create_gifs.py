from rich.console import Console
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os

from features import get_feature_file_paths, get_feature_names
from file_utils import ensure_directory, get_files, get_file_name_without_extension
from tracking_data import create_tracking_data_from_file, get_tracking_data_information, create_df_from_tracking_data
from color_utils import hex_to_rgb, KEYPOINT_COLORS, CHART_BACKGROUND_COLOR

# Global variables
GIF_FOLDER_NAME = "gifs"
TRACK_DATA_FOLDER_NAME = "track_data"
TRACK_DATA_FILE_EXTENSION = "pb"
VIEWPORT_WIDTH_RATIO = 16
VIEWPORT_HEIGHT_RATIO = 9
DISPLAY_AXIS = False
DISPLAY_TITLE = False

console = Console()

def create_frame(frame, data, scatter):

	x = [kp.posX for kp in tracking_data.frameData[frame].poseData[0].keyPoints]
	y = [kp.posY for kp in tracking_data.frameData[frame].poseData[0].keyPoints]
	
	data = [xy for xy in zip(x, y)]
	scatter.set_offsets(data)
	return scatter

def create_gif(tracking_data, tracking_data_information, file_path):
	# Set background color for the chart
	fig, ax = plt.subplots(1, 1, figsize=(VIEWPORT_WIDTH_RATIO, VIEWPORT_HEIGHT_RATIO))
	ax.set_facecolor(CHART_BACKGROUND_COLOR)

	# Set limits for x and y axis
	ax.set_xlim([0, tracking_data_information["resolution_x"]])
	ax.set_ylim([tracking_data_information["resolution_y"], 0])

	if not DISPLAY_AXIS:
		ax.set_axis_off()

	if DISPLAY_TITLE:
		# Set title
		plt.title(file_path)

	# Create new scatter plot instance to pass into the update function
	scatter = ax.scatter(0, 0)

	# Set colors for the 24 different keypoints.
	scatter.set_facecolor(KEYPOINT_COLORS)

	frames = tracking_data_information["num_frames"]
	fps = tracking_data_information["frame_rate"]
	interval = 1000 / fps

	# https://matplotlib.org/stable/users/explain/animations/animations.html
	anim = animation.FuncAnimation(fig, create_frame, repeat=True, frames=frames, interval=interval, fargs=(tracking_data.frameData, scatter))

	# Will only work if ffmpeg is actually installed...
	try:
		anim.save(file_path)
	except Exception as error:
		print(f"Failed to save gif for matplotlib because of {error}")
		print(f"Do you have ffmpeg installed on your system?")
		exit(-1)


if __name__ == "__main__":
	feature_file_paths = get_feature_file_paths()
	feature_names = get_feature_names()

	print("Found the following features and file paths")
	for feature_name, file_path in zip(feature_names, feature_file_paths):
		print(f"{feature_name} => {file_path}")

	for index, feature_path in enumerate(feature_file_paths):
		feature_name = feature_names[index]
		track_data_folder = os.path.join(feature_path, TRACK_DATA_FOLDER_NAME)
		gif_folder_path = os.path.join(feature_path, GIF_FOLDER_NAME)

		ensure_directory(gif_folder_path)

		if not os.path.isdir(track_data_folder):
			print(f"Could not find track data folder, expected path was {track_data_folder}")
			print(f"Skipping...")
			continue

		track_data_files = get_files(track_data_folder, TRACK_DATA_FILE_EXTENSION)
		if len(track_data_files) == 0:
			print(f"Did not find any matching track data files make sure you have some files with extension .{TRACK_DATA_FILE_EXTENSION} inside the directory {track_data_folder}")
			print("Skipping...")
			continue

		print("Found the following track data files", track_data_files)

		# Iterate through all the found data files
		for track_data_file in track_data_files:
			with console.status(f"Creating gifs for feature {feature_name}") as status:
				track_data_file_name_without_extension = get_file_name_without_extension(track_data_file)
				
				gif_name = f"{track_data_file_name_without_extension}.gif"
				gif_full_path = os.path.join(gif_folder_path, gif_name)

				tracking_data = create_tracking_data_from_file(track_data_file)

				# Show general information about tracking data
				tracking_data_information = get_tracking_data_information(tracking_data)
				print(tracking_data_information)

				try:
					# Create gif
					print(f"Creating gif for {track_data_file} ...")
					create_gif(tracking_data, tracking_data_information, gif_full_path)
				except Exception as e:
					print(f"Failed to create gif due to error {e}")


import os
import pandas as pd
import cv2
from rich.console import Console
from features import get_feature_file_paths, get_feature_names
from file_utils import ensure_directory, get_files, get_file_name_without_extension
from tracking_data import create_tracking_data_from_file, get_tracking_data_information, create_df_from_tracking_data
from color_utils import hex_to_rgb, KEYPOINT_COLORS

# Global variables
VIEWPORT_WIDTH_RATIO = 16
VIEWPORT_HEIGHT_RATIO = 9
TRACK_DATA_FOLDER_NAME = "track_data"
VIDEO_DATA_FOLDER_NAME = "videos"
VIDEO_OVERLAY_FOLDER_NAME = "video_overlays"
TRACK_DATA_FILE_EXTENSION = "pb"
VIDEO_FILE_EXTENSION = "MOV"

console = Console()

def create_video_overlay(tracking_data, tracking_data_information, video_file_path, overlay_file_path):
	# Create data frame
	df = create_df_from_tracking_data(tracking_data)

	# Open the video file
	cap = cv2.VideoCapture(video_file_path)

	# open output file
	fps = tracking_data_information["frame_rate"]
	res_x = tracking_data_information["resolution_x"]
	res_y = tracking_data_information["resolution_y"]

	out = cv2.VideoWriter(overlay_file_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (res_x,res_y))

	frame_number = 0
	try:
		while cap.isOpened():
			success, frame = cap.read()
			if success:
				if frame_number in df.index.get_level_values(0):
					x = df.loc[frame_number, pd.IndexSlice[:,['x']]].values.squeeze()
					y = df.loc[frame_number, pd.IndexSlice[:,['y']]].values.squeeze()

					for i, kp in enumerate(zip(x, y)):
						color_tuple = hex_to_rgb(KEYPOINT_COLORS[i])
						frame = cv2.circle(frame, (int(kp[0]), int(kp[1])), 5, color_tuple, -1)

				out.write(frame)
				frame_number += 1
			else:
				break
	except Exception as error:
		print(f"Failed on frame {frame_number} due to {error}")
	finally:
		cap.release()
		out.release()

if __name__ == "__main__":
	feature_file_paths = get_feature_file_paths()
	feature_names = get_feature_names()

	print("Found the following features and file paths")
	for feature_name, file_path in zip(feature_names, feature_file_paths):
		print(f"{feature_name} => {file_path}")

	for index, feature_path in enumerate(feature_file_paths):
		feature_name = feature_names[index]
		track_data_folder = os.path.join(feature_path, TRACK_DATA_FOLDER_NAME)
		video_data_folder = os.path.join(feature_path, VIDEO_DATA_FOLDER_NAME)
		video_overlay_folder_path = os.path.join(feature_path, VIDEO_OVERLAY_FOLDER_NAME)

		ensure_directory(video_overlay_folder_path)

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

		video_data_files = []
		# Only generate video overlay if an actual video was provided...
		generate_video_overlay = os.path.isdir(video_data_folder)
		if not generate_video_overlay:
			print(f"Could not find video folder, expected path was {video_data_folder}")
			print(f"Generating video overlays will be skipped...")

		else:
			# Get all video files wich match the given extension
			video_data_files = get_files(video_data_folder, VIDEO_FILE_EXTENSION)

		# Iterate through all the found data files and try to find a matching video file (e.g same file name)
		for track_data_file, video_data_file in zip(track_data_files, video_data_files):
			with console.status(f"Creating video overlays for feature {feature_name}") as status:
				track_data_file_name_without_extension = get_file_name_without_extension(track_data_file)
				video_data_file_name_without_extension = get_file_name_without_extension(video_data_file)

				video_overlay_name = f"{track_data_file_name_without_extension}.mp4"
				video_overlay_full_path = os.path.join(video_overlay_folder_path, video_overlay_name)

				found_match_video_file = track_data_file_name_without_extension == video_data_file_name_without_extension

				tracking_data = create_tracking_data_from_file(track_data_file)

				# Show general information about tracking data
				tracking_data_information = get_tracking_data_information(tracking_data)
				print(tracking_data_information)

				if not found_match_video_file:
					print(f"Found no matching video file for track data file {track_data_file_name_without_extension}")
					print(f"Generating video overlay will be skipped for this file...")
					continue

				try:
					# Create video overlay
					print(f"Creating video overlay for {track_data_file} ...")
					create_video_overlay(tracking_data, tracking_data_information, video_data_file, video_overlay_full_path)
				except Exception as e:
					print(f"Failed to create video overlay due to error {e}")


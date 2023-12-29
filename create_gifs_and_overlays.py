import trackingDataPb_pb2
import os
import json
from rich import print
from rich.console import Console
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import pandas as pd
import glob
import pathlib

# Global variables
VIEWPORT_WIDTH_RATIO = 16
VIEWPORT_HEIGHT_RATIO = 9
KEYPOINT_COLORS = [
    '#F92672', '#66D9EF', '#A6E22E', '#FD971F', '#E6DB74', '#AE81FF',
    '#66FF66', '#FF99CC', '#FFB366', '#99CCFF', '#66CCCC', '#FF6666',
    '#6699FF', '#CC99FF', '#C6E2FF', '#FFCCCC', '#A8FF60', '#FFE666',
    '#C6FFDD', '#E1F5C4', '#FF80AB', '#B19CD9', '#FF91AF', '#A8FF60'
]
CHART_BACKGROUND_COLOR = '#272822'
FEATURES_DIRECTORY_PATH = "./data/features"
TRACK_DATA_FOLDER_NAME = "track_data"
VIDEO_DATA_FOLDER_NAME = "videos"
GIF_FOLDER_NAME = "gifs"
VIDEO_OVERLAY_FOLDER_NAME = "video_overlays"
TRACK_DATA_FILE_EXTENSION = "pb"
VIDEO_FILE_EXTENSION = "MOV"


console = Console()

def get_tracking_data_information(tracking_data):
	video_metadata = tracking_data.videoMeta
	frame_rate = video_metadata.frameRate
	resolution_x = video_metadata.resX
	resolution_y = video_metadata.resY
	num_frames = len(tracking_data.frameData)
	first_frame = get_first_frame_with_data(tracking_data)
	return { "frame_rate": frame_rate, "resolution_x": resolution_x, "resolution_y": resolution_y, "num_frames": num_frames, "first_frame": first_frame }

def get_first_frame_with_data(tracking_data):
	for i, frame in enumerate(tracking_data.frameData):
	    if frame.poseData:
	        return i
	return -1

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

def create_df_from_tracking_data(tracking_data):
	df = []
	for frame in tracking_data.frameData:
		# For some reason we can get two elements in poseData which messes up the structure of the dataframe.
		# TODO: Check why we get two poses (e.g frame 21 in file ./data/test/track_data/guemah_forehand_flat_02out.pb)
		if len(frame.poseData) > 1:
			print(f"Got multiple pose data for frame {frame.index}")
		for pose in frame.poseData:
			# We are only interested in poses with id 0, skip the rest. This only occurs when we have multiple pose data per frame.
			if pose.id != 0:
				continue
			for keypoint in pose.keyPoints:
				# add frame and keypoint information to array
				df.append([frame.index, pose.id, keypoint.type, keypoint.posX, keypoint.posY, keypoint.absPosX, keypoint.absPosY, keypoint.absPosZ])

	df = pd.DataFrame(df, columns=["frame", "pose", "keypoint", "x", "y", "absX", "absY", "absZ"])
	df = df.pivot(index=["frame", "pose"], columns="keypoint", values=["x", "y", "absX", "absY", "absZ"])
	df = df.swaplevel(axis=1)
	return df

def hex_to_rgb(hex_string):
    # Remove '#' if present
    if hex_string.startswith('#'):
        hex_string = hex_string[1:]

    # Ensure the hex string is valid
    if len(hex_string) != 6:
        raise ValueError("Invalid hex string length. It should be 6 characters long (excluding '#').")

    # Convert hex to RGB
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)

    return (r, g, b)

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

def get_last_part_of_path(path):
	# Returns the last part of a file path. e.g /data/foo/bar/baz => baz
	return os.path.basename(os.path.normpath(path))

def get_subdirectories(path):
	return [ f.path for f in os.scandir(path) if f.is_dir() ]

def get_files(path, file_extension):
	return [ f for f in glob.glob(f'{path}/*.{file_extension}') ]

def get_file_name_without_extension(file_path):
	return pathlib.Path(file_path).stem

def ensure_directory(directory_path):
	if not os.path.exists(directory_path):
		print(f"Expected directory {directory_path} to be available but it was not, it will be created now...")
		os.makedirs(directory_path)

if __name__ == "__main__":
	# Get the name of all features (e.g folders listed under data/features)
	feature_file_paths = get_subdirectories(FEATURES_DIRECTORY_PATH)
	feature_names = [ get_last_part_of_path(path) for path in feature_file_paths ]

	print("Found the following features and file paths")
	for feature_name, file_path in zip(feature_names, feature_file_paths):
		print(f"{feature_name} => {file_path}")

	for index, feature_path in enumerate(feature_file_paths):
		feature_name = feature_names[index]
		track_data_folder = os.path.join(feature_path, TRACK_DATA_FOLDER_NAME)
		video_data_folder = os.path.join(feature_path, VIDEO_DATA_FOLDER_NAME)
		gif_folder_path = os.path.join(feature_path, GIF_FOLDER_NAME)
		video_overlay_folder_path = os.path.join(feature_path, VIDEO_OVERLAY_FOLDER_NAME)

		ensure_directory(gif_folder_path)
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
			with console.status(f"Creating gifs and video overlays for feature {feature_name}") as status:
				track_data_file_name_without_extension = get_file_name_without_extension(track_data_file)
				video_data_file_name_without_extension = get_file_name_without_extension(video_data_file)
				
				gif_name = f"{track_data_file_name_without_extension}.gif"
				gif_full_path = os.path.join(gif_folder_path, gif_name)

				video_overlay_name = f"{track_data_file_name_without_extension}.mp4"
				video_overlay_full_path = os.path.join(video_overlay_folder_path, video_overlay_name)

				found_match_video_file = track_data_file_name_without_extension == video_data_file_name_without_extension

				tracking_data = trackingDataPb_pb2.trackingData()

				# Load tracking data
				with open(track_data_file, "rb") as f:
					print(f"Reading in file {track_data_file}")
					tracking_data.ParseFromString(f.read())

				# Show general information about tracking data
				tracking_data_information = get_tracking_data_information(tracking_data)
				print(tracking_data_information)

				try:
					# Create gif
					print(f"Creating gif for {track_data_file} ...")
					create_gif(tracking_data, tracking_data_information, gif_full_path)
				except Exception as e:
					print(f"Failed to create gif due to error {e}")

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


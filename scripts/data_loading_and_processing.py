import trackingDataPb_pb2
import os
import json
from rich import print
from rich.console import Console
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import pandas as pd

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
CONFIG_FILE_PATH = "./data_loading_and_processing.json"


console = Console()


def print_information(tracking_data):
	# Show metadata about video
	video_metadata = tracking_data.videoMeta
	frame_rate = video_metadata.frameRate
	resolution_x = video_metadata.resX
	resolution_y = video_metadata.resY
	num_frames = len(tracking_data.frameData)
	print(f"Frame Rate {frame_rate}")
	print(f"Resolution [bold magenta] {resolution_x}x{resolution_y} [/bold magenta]")
	print(f"Number of Frames {num_frames}")

def get_video_information(tracking_data):
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

def create_matploblib_frame(frame, data, scatter):

	x = [kp.posX for kp in tracking_data.frameData[frame].poseData[0].keyPoints]
	y = [kp.posY for kp in tracking_data.frameData[frame].poseData[0].keyPoints]
	
	data = [xy for xy in zip(x, y)]
	scatter.set_offsets(data)
	return scatter

def create_matplotlib_gif(tracking_data, video_information, file_path):
	with console.status(f"[bold green]Creating matplotib gif {file_path} [/bold green]") as status:
		# Set background color for the chart
		fig, ax = plt.subplots(1, 1, figsize=(VIEWPORT_WIDTH_RATIO, VIEWPORT_HEIGHT_RATIO))
		ax.set_facecolor(CHART_BACKGROUND_COLOR)

		# Set limits for x and y axis
		ax.set_xlim([0, video_information["resolution_x"]])
		ax.set_ylim([video_information["resolution_y"], 0])

		# Set title
		plt.title(file_path)

		# Create new scatter plot instance to pass into the update function
		scatter = ax.scatter(0, 0)

		# Set colors for the 24 different keypoints.
		scatter.set_facecolor(KEYPOINT_COLORS)

		frames = video_information["num_frames"]
		fps = video_information["frame_rate"]
		interval = 1000 / fps

		# https://matplotlib.org/stable/users/explain/animations/animations.html
		anim = animation.FuncAnimation(fig, create_matploblib_frame, repeat=True, frames=frames, interval=interval, fargs=(tracking_data.frameData, scatter))

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

def create_video_overlay(tracking_data, video_information, video_file_path, overlay_file_path):
	ensure_file_path(video_file_path)

	# Create data frame
	df = create_df_from_tracking_data(tracking_data)

	# Open the video file
	cap = cv2.VideoCapture(video_file_path)

	# open output file
	fps = video_information["frame_rate"]
	res_x = video_information["resolution_x"]
	res_y = video_information["resolution_y"]

	out = cv2.VideoWriter(overlay_file_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (res_x,res_y))

	frame_number = 0
	try:
		with console.status(f"[bold green]Creating video overlay {overlay_file_path} [/bold green]") as status:
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

def process(tracking_data, config):
	video_information = get_video_information(tracking_data)
	print(video_information)
	create_matplotlib_gif(tracking_data, video_information, config["matplotlib_gif_out_path"])

	try:
		create_video_overlay(tracking_data, video_information, config["video_path"], config["video_overlay_out_path"])
	except Exception as e:
		print(f"Failed to create video overlay for video {config["video_path"]} due to error {e}")
	
def ensure_file_path(file_path):
	if not os.path.isfile(file_path):
		print(f"Expected to find file under path {file_path} but was not found!")
		exit(-1)
	
if __name__ == "__main__":
	ensure_file_path(CONFIG_FILE_PATH)

	with open(CONFIG_FILE_PATH, "r") as f:
		config = json.load(f)["config"]

	for element in config:
		tracking_data = trackingDataPb_pb2.trackingData()
		track_data_file_path = element["track_data_file_path"]
		ensure_file_path(track_data_file_path)
		with open(track_data_file_path, "rb") as f:
			print(f"Reading in file {track_data_file_path}")
			tracking_data.ParseFromString(f.read())
		process(tracking_data, element)

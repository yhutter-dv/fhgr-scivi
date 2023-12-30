import trackingDataPb_pb2
import pandas as pd

from file_utils import panic_if_path_not_exists

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

def create_tracking_data_from_file(file_path):
	panic_if_path_not_exists(file_path)
	tracking_data = trackingDataPb_pb2.trackingData()

	# Load tracking data
	with open(file_path, "rb") as f:
		print(f"Reading in file {file_path}")
		tracking_data.ParseFromString(f.read())
	return tracking_data
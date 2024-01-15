import os
import sys
import trackingDataPb_pb2
import pandas as pd

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Expected file '{file_path}' but was not found...")
        
def load_tracking_data(file_path):
    ensure_file(file_path)
    with open(file_path, "rb") as f:
        # create tracking data object
        tracking_data = trackingDataPb_pb2.trackingData()
        
        # parse string from file
        tracking_data.ParseFromString(f.read())
    return tracking_data

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
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import trackingDataPb_pb2

def create_app():
    app = FastAPI()

    # Allow CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()

def get_first_frame_with_data(tracking_data):
	for i, frame in enumerate(tracking_data.frameData):
	    if frame.poseData:
	        return i
	return -1

def get_tracking_data_information(tracking_data):
	video_metadata = tracking_data.videoMeta
	frame_rate = video_metadata.frameRate
	resolution_x = video_metadata.resX
	resolution_y = video_metadata.resY
	num_frames = len(tracking_data.frameData)
	first_frame = get_first_frame_with_data(tracking_data)
	return { "frame_rate": frame_rate, "resolution_x": resolution_x, "resolution_y": resolution_y, "num_frames": num_frames, "first_frame": first_frame }


@app.post("/predict_movement")
async def file(file: UploadFile):
	print(f"Got file ", file)

	tracking_data = trackingDataPb_pb2.trackingData()

	with file.file as pb_file:
		# Load tracking data
		tracking_data.ParseFromString(pb_file.read())

	tracking_data_information = get_tracking_data_information(tracking_data)
	print(tracking_data_information)

	# TODO Implement with DTW Algorithm...
	return tracking_data_information
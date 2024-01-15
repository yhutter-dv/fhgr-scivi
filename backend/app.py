from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import trackingDataPb_pb2
import json
from utils import ensure_file
from classification import classify_with_elbow_angle

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

def load_train_config():
    file_path = "./train_config.json"
    ensure_file(file_path)
    with open(file_path, "r") as f:
        result = json.load(f)
    return result["config"]

TRAIN_CONFIG = load_train_config()
app = create_app()

@app.post("/predict_movement")
async def predict_movement(file: UploadFile):
    tracking_data = trackingDataPb_pb2.trackingData()

    with file.file as pb_file:
        # Load tracking data
        tracking_data.ParseFromString(pb_file.read())

    result = classify_with_elbow_angle(TRAIN_CONFIG, tracking_data)
    print("Got result", result)
    return result
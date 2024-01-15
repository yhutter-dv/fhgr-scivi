import vg
import sys
import pandas as pd
from utils import create_df_from_tracking_data, load_tracking_data
from dtw import compare_datasets

def get_elbow_angle(tracking_data, smooth = True, is_left = True):
    df = create_df_from_tracking_data(tracking_data)
    if is_left:
        kp16 = df.loc[:,pd.IndexSlice[16,["absX", "absY", "absZ"]]].values
        kp18 = df.loc[:,pd.IndexSlice[18,["absX", "absY", "absZ"]]].values
        kp20 = df.loc[:,pd.IndexSlice[20,["absX", "absY", "absZ"]]].values
        vg16_18 = kp16 - kp18
        vg18_20 = kp18 - kp20
        result = vg.angle(vg16_18, vg18_20)
    else:
        kp17 = df.loc[:,pd.IndexSlice[17,["absX", "absY", "absZ"]]].values
        kp19 = df.loc[:,pd.IndexSlice[19,["absX", "absY", "absZ"]]].values
        kp21 = df.loc[:,pd.IndexSlice[21,["absX", "absY", "absZ"]]].values
        vg17_19 = kp17 - kp19
        vg19_21 = kp19 - kp21
        result = vg.angle(vg17_19, vg19_21)
    if smooth:
        result = pd.Series(result).rolling(5, center = True, min_periods=1).mean().values
    return result

def classify_with_elbow_angle(train_config, test_track_data, smooth = True):
     # Load train data (for left and right)
    train_data_left = []
    train_data_right = []
    train_data_paths_right = []
    train_data_paths_left = []
    file_path_to_classification_mapping = {}
    train_config_left = [config for config in train_config if config["is_left"] == True]
    train_config_right = [config for config in train_config if config["is_left"] == False]
    
    for config in train_config_left:
        file_path = config["file_path"]
        file_path_to_classification_mapping[file_path] = config["classification"]
        tracking_data = load_tracking_data(file_path)
        elbow_angle = get_elbow_angle(tracking_data, smooth, is_left = True) 
        train_data_left.append(elbow_angle)
        train_data_paths_left.append(file_path)

    for config in train_config_right:
        file_path = config["file_path"]
        file_path_to_classification_mapping[file_path] = config["classification"]
        tracking_data = load_tracking_data(file_path)
        elbow_angle = get_elbow_angle(tracking_data, smooth, is_left = False) 
        train_data_right.append(elbow_angle)
        train_data_paths_right.append(file_path)
        
     # Load test data (for left and right)
    test_elbow_angle_left = get_elbow_angle(test_track_data, smooth, is_left = True)
    test_elbow_angle_right = get_elbow_angle(test_track_data, smooth, is_left = False)

    # Define classification results
    classification_result_left = {
        "classification": "None",
        "file_path": "None",
        "cost": sys.maxsize
    }

    classification_result_right = {
        "classification": "None",
        "file_path": "None",
        "cost": sys.maxsize
    }
    
    # Check Left
    print(f"Checking Left")
    for config in train_config_left:
        print(".", end = " ")
        for index, compare_with in enumerate(train_data_left):
            alignment_cost, _ = compare_datasets(test_elbow_angle_left, compare_with)
            train_data_file_path = train_data_paths_left[index]
            if alignment_cost < classification_result_left["cost"]:
                new_classification = file_path_to_classification_mapping[train_data_file_path]
                classification_result_left["cost"] = alignment_cost
                classification_result_left["classification"] = new_classification
                classification_result_left["file_path"] = train_data_file_path

    # Check Right
    print()
    print(f"Checking Right")
    for config in train_config_right:
        print(".", end = " ")
        for index, compare_with in enumerate(train_data_right):
            alignment_cost, _ = compare_datasets(test_elbow_angle_right, compare_with)
            train_data_file_path = train_data_paths_right[index]
            if alignment_cost < classification_result_right["cost"]:
                new_classification = file_path_to_classification_mapping[train_data_file_path]
                classification_result_right["cost"] = alignment_cost
                classification_result_right["classification"] = new_classification
                classification_result_right["file_path"] = train_data_file_path

    print()
    if classification_result_right["cost"] < classification_result_left["cost"]:
        return classification_result_right
    else:
        return classification_result_left
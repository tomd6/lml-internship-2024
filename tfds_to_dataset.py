"""
Utility Script used to convert the google RT-1 dataset (https://console.cloud.google.com/storage/browser/gresearch/rt-1-data-release;tab=objects) into a lava-compatible dataset
"""

import tensorflow_datasets as tfds
from torch.utils.data import DataLoader
import matplotlib as plt
import cv2
from pathlib import Path
import os
from datasets import load_dataset
from PIL import Image
from io import BytesIO
import requests
import json
import uuid

"""
Convert the rt1 dataset's action array to a series of numbers as a string
The first 3 numbers represent if this is the last action of an episode or not
The 3 after that represent the movements made by the robot in the x, y and z axis.
Then, the 3 after that represent the rotation of the robot. 
Finally, the last one is a boolean telling us if the gripper is closed or open.
"""
def convert_to_string(array):
        total = 0
        string = ""
        terminate_action = array['terminate_episode']
        string = string + str(terminate_action[0]) + ' ' + str(terminate_action[1]) + ' ' + str(terminate_action[2]) + ' ' 
        world_vector = array['world_vector'] 
        total+= sum(world_vector)
        string = string + str(world_vector[0]) + ' ' + str(world_vector[1]) + ' ' + str(world_vector[2]) + ' '
        rotation = array['rotation_delta']
        total += sum(rotation)
        string = string + str(rotation[0]) + ' ' + str(rotation[1]) + ' ' + str(rotation[2]) + ' '
        string += str(array['gripper_closedness_action'][0])
        total += array['gripper_closedness_action'][0]
        return string,total

"""
Process the raw rt-1 dataset and convert it to a dataset fine-tunable by LLaVA-type models.
dataset : the raw rt-1 dataset, opened with the tfds library
output_folder : the folder in which the final dataset will be stored.
subset_name : either train or test.
iterate : the number of data we want to save.
"""
def process_and_save(dataset, output_folder, subset_name,iterate):
    #training is either 'train' or 'test'
    # Define image subfolder within output folder
    subset_folder = os.path.join(output_folder, subset_name)
    image_subfolder = os.path.join(output_folder, 'images')


    if not os.path.exists(image_subfolder):
        os.makedirs(image_subfolder)
    if not os.path.exists(subset_folder):
        os.makedirs(subset_folder)


    # Initialize list to hold all JSON data
    json_data_list = []


    # Process and save images and labels
    i = 0
    for x in range(iterate):
        print(i)
        for steps in range (len(dataset[x]['steps'])):
                 i = i + 1
        # Load image if it's a URL or a file path
                 im = dataset[x]['steps'][steps]['observation']['image']
                         # Create a unique ID for each image
                 unique_id = str(uuid.uuid4())
                 image_path = os.path.join(image_subfolder, f"{unique_id}.jpg")
                 cv2.imwrite(image_path, cv2.cvtColor(im, cv2.COLOR_RGB2BGR)) 
                # Remove duplicates and format answers
                 answer_arr = dataset[x]['steps'][steps]['action']
                 answer,total = convert_to_string(answer_arr)
                 if(total != 0):


                 # Structure for LLaVA JSON
                    json_data = {
                    "id": unique_id,
                    "image": f"{unique_id}.jpg",
                    "conversations": [
                        {
                            "from": "human",
                            "value": "<image>\n" + str(dataset[x]['steps'][steps]['observation']['natural_language_instruction'])[2:-1]
                        },
                        {
                        "from": "gpt",
                            "value": answer
                        }
                    ]
                }

            # Append to list
                 json_data_list.append(json_data)
            # Save the JSON data list to a file
    json_output_path = os.path.join(output_folder, subset_name, 'dataset.json')
    with open(json_output_path, 'w') as json_file:
        json.dump(json_data_list, json_file, indent=4)


test = tfds.builder_from_directory('./datasets/rt1') #Path to the RT1 dataset
test.download_and_prepare()
test_data = test.as_data_source(split='train[:20%]')
train_data = test.as_data_source(split=('train[20%:]'))

test.download_and_prepare()

process_and_save(test_data,'./datasets/rt1_llava_full_dataset','test',len(test_data))
process_and_save(train_data,'./datasets/rt1_llava_full_dataset','train',len(train_data))
#rt1_llava_full_dataset

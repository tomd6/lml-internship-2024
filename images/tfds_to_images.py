"""
Script used to convert the google RT-1 dataset into an ordered series of images
"""
import tensorflow_datasets as tfds
from torch.utils.data import DataLoader
import matplotlib as plt
import cv2
from pathlib import Path
import os
import torch
test = tfds.builder_from_directory('./datasets/rt1')
test_info = test.info

test.download_and_prepare()

ds= test.as_data_source()

for x in range(len(ds['train']):
    Path('./datasets/rt1_visual/'+str(x)).mkdir(parents=True,exist_ok=True)
    stri = (ds['train'][x]['steps'][0]['observation']['natural_language_instruction'])
    f = open('./datasets/rt1_visual/'+str(x)+'/'+str(stri)+".txt", "w")
    for steps in range (len(ds['train'][x]['steps'])):
        im = ds['train'][x]['steps'][steps]['observation']['image']
        cv2.imwrite('./datasets/rt1_visual/'+str(x)+'/'+'im_'+str(steps)+'.jpg', cv2.cvtColor(im, cv2.COLOR_RGB2BGR)) 

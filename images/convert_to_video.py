"""
Convert the different images of each action (see tfds_to_image.py) into an animated gif
"""
import imageio
import os
from natsort import natsorted
import tensorflow_datasets as tfds

test = tfds.builder_from_directory('./datasets/rt1')
mnist_info = test.info

test.download_and_prepare()
ds= test.as_data_source()

for x in range(len(ds['train'])):
    with imageio.get_writer('./datasets/rt1_visual/'+str(x)+'/movie.gif', mode='I',loop=0) as writer:
        im_list = []
        for file in natsorted(os.listdir('./datasets/rt1_visual/'+str(x))):
            filename = os.fsdecode(file)
            if filename.endswith(".png") or filename.endswith(".jpg"): 
                image = imageio.imread('./datasets/rt1_visual/'+str(x)+'/'+filename)
                writer.append_data(image)

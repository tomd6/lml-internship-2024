## Context
This is a compilation of different pieces of code that were used in order to try to replicate the RT-2 paper:
https://arxiv.org/pdf/2307.15818
Each one serves a different purpose and depends on different files.
Please note that some of them were made in order to run on the French supercalculator Jean Zay, and may be of little use of you use something else.
Also note that a lot of the scripts presented here use relative path and links, which you should change appropriately when running the scripts on your machine.

### RT-1 Dataset

The goal of the tfds_to_dataset and the images folder is to download the RT-1 dataset and convert it, either to LLaVA-type dataset or to human-viewable images and videos.
Please first download the dataset from here before launching the scripts.
You can download the raw dataset here:
https://console.cloud.google.com/storage/browser/gresearch/rt-1-data-release;tab=objects


| File name              | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| `tfd_to_dataset.py`    | Main Script, transforms the raw dataset into a dataset with the LLaVA format             |
| `tfds_to_image.py`     | Images folder. Converts the raw dataset into a series of images within ordered folders.  |
| `convert_to_video.py`  | Images folder. Converts the result of tfds_to_image.py into a series of animated gif.    |


### LLaVA_scripts folder

Scripts and files used in order to fine-tune the original LLaVA with the RT-1 dataset.
You should drop those files in this folder :
https://github.com/haotian-liu/LLaVA
Please note that this implementation of LLaVA has some problemes, most notably the checkpoints not working when fine-tuning with lora. 
Hence why we switched to LLaVA-MED.

| File name              | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| `finetune_custom.sh`   | Main Script, used to fine-tune LLaVA with the RT-1 dataset.                              |
| `tllava_jzay_script.sh`| Used to launch the main script finetue_custom.sh on the French supercalculator Jean Zay. |
| `mm_projector.bin`     | Pre-Trained LLaVA Model's weights.                                                       |

### LLaVA_scripts folder

Scripts and files used in order to fine-tune LLaVA-MED with the RT-1 dataset.
You should drop those files in this folder :
hhttps://github.com/microsoft/LLaVA-Med
LLaVA-MED is an implementation of LLaVA made for Biomedecine. However, it works more or less like the original version of LLaVA, minus some bugs.

| File name              | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| `finetune_custom.sh`   | Main Script, used to fine-tune LLaVA with the RT-1 dataset.                              |
| `tllava_jzay_script.sh`| Used to launch the main script finetue_custom.sh on the French supercalculator Jean Zay. |

import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from llava.conversation import conv_templates
from llava.utils import disable_torch_init
from transformers import CLIPVisionModel, CLIPImageProcessor, StoppingCriteria
from llava import LlavaLlamaForCausalLM
from llava.model.utils import KeywordsStoppingCriteria

from PIL import Image

import os
import requests
from PIL import Image
from io import BytesIO

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys

device = 'cuda' if torch.cuda.is_available() else 'cpu'


model_path = "./checkpoints/llava-rt2-7b-v3-pretrain"


DEFAULT_IMAGE_TOKEN = "<image>"
DEFAULT_IMAGE_PATCH_TOKEN = "<im_patch>"
DEFAULT_IM_START_TOKEN = "<im_start>"
DEFAULT_IM_END_TOKEN = "<im_end>"

def load_image(image_file):
    if image_file.startswith('http') or image_file.startswith('https'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image


def get_model(model_name):
    disable_torch_init()
    model_name = os.path.expanduser(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = LlavaLlamaForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).cuda()
    image_processor = CLIPImageProcessor.from_pretrained(model.config.mm_vision_tower, torch_dtype=torch.float16)

    mm_use_im_start_end = getattr(model.config, "mm_use_im_start_end", False)
    tokenizer.add_tokens([DEFAULT_IMAGE_PATCH_TOKEN], special_tokens=True)
    if mm_use_im_start_end:
        tokenizer.add_tokens([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN], special_tokens=True)

    vision_tower = model.model.vision_tower[0]
    vision_tower.to(device='cuda', dtype=torch.float16)
    vision_config = vision_tower.config
    vision_config.im_patch_token = tokenizer.convert_tokens_to_ids([DEFAULT_IMAGE_PATCH_TOKEN])[0]
    vision_config.use_im_start_end = mm_use_im_start_end
    if mm_use_im_start_end:
        vision_config.im_start_token, vision_config.im_end_token = tokenizer.convert_tokens_to_ids([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN])
    image_token_len = (vision_config.image_size // vision_config.patch_size) ** 2

    return tokenizer, model, image_processor, mm_use_im_start_end, image_token_len

tokenizer, model, image_processor, mm_use_im_start_end, image_token_len = get_model(model_path)




def predict(prompt, image_path, tokenizer, model, image_processor, mm_use_im_start_end, image_token_len):
    qs = prompt
    if mm_use_im_start_end:
        qs = qs + '\n' + DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_PATCH_TOKEN * image_token_len + DEFAULT_IM_END_TOKEN
    else:
        qs = qs + '\n' + DEFAULT_IMAGE_PATCH_TOKEN * image_token_len

    conv = conv_templates["multimodal"].copy()
    conv.append_message(conv.roles[0], qs)
    prompt = conv.get_prompt()
    inputs = tokenizer([prompt])

    image = load_image(image_path)
    image_tensor = image_processor.preprocess(image, return_tensors='pt')['pixel_values'][0]

    input_ids = torch.as_tensor(inputs.input_ids).cuda()

    keywords = ['###']
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor.unsqueeze(0).half().cuda(),
            do_sample=True,
            temperature=0.1,
            max_new_tokens=500,
            stopping_criteria=[stopping_criteria])

    input_token_len = input_ids.shape[1]
    n_diff_input_output = (input_ids != output_ids[:, :input_token_len]).sum().item()
    if n_diff_input_output > 0:
        print(f'[Warning] {n_diff_input_output} output_ids are not the same as the input_ids')
    outputs = tokenizer.batch_decode(output_ids[:, input_token_len:], skip_special_tokens=True)[0]

    while True:
        cur_len = len(outputs)
        outputs = outputs.strip()
        for pattern in ['###', 'Assistant:', 'Response:']:
            if outputs.startswith(pattern):
                outputs = outputs[len(pattern):].strip()
        if len(outputs) == cur_len:
            break

    try:
        index = outputs.index(conv.sep)
    except ValueError:
        outputs += conv.sep
        index = outputs.index(conv.sep)

    outputs = outputs[:index].strip()
    return outputs

PORT_NUMBER = 5331
SIZE = 1024
hostName = gethostbyname('0.0.0.0')

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

def receved_msg():
    (prompt, addr) = mySocket.recvfrom(SIZE)

    image = open("tmp_img.jpg", "wb")
    (data, addr) = mySocket.recvfrom(SIZE)

    while data != b"end_img":
        image.write(data)
        (data, addr) = mySocket.recvfrom(SIZE)

    image.close()
    return prompt.decode("utf-8"), addr


while True:
    
    prompt, addr = receved_msg()
    prompt = DEFAULT_IMAGE_TOKEN + "\n" + prompt
    print("Image receved")
    prediction = predict(prompt, "tmp_img.jpg", tokenizer, model, image_processor, mm_use_im_start_end, image_token_len)
    print("--------------")
    print(prediction)
    print("--------------")

    mySocket.sendto(prediction.encode(), addr)

sys.exit()

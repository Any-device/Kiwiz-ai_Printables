import json
import gradio as gr
import requests
import os 
from pathlib import Path
import time


from transformers.models.mobilebert.modeling_mobilebert import OutputBottleneck



URL = URL = "https://8188-01k19pahvmjcp2yqcaan23e7c8.cloudspaces.litng.ai//prompt"
OUTPUT_DIR = Path("/teamspace/studios/this_studio/ComfyUI/output")
files = os.listdir(OUTPUT_DIR)  # This works fine


def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    response = requests.post(URL, data=data)

    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        print("❌ Failed to decode JSON")
        print("🔍 Raw response text:\n", response.text)
        raise


def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png','.jpg','.jpeg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image


def generate_image(Positive_Prompt,Negative_prompt):
  with open("ColuringBook-Redmond_api.json", "r") as file_json:
   prompt = json.load(file_json)
   prompt["3"]["inputs"]["text"] = f"digital artwork of a {Positive_Prompt}"
   prompt["4"]["inputs"]["text"] = Negative_prompt

   previous_image = get_latest_image(OUTPUT_DIR)
   start_queue(prompt)
   
   while True:
    latest_image = get_latest_image(OUTPUT_DIR)

    if latest_image != previous_image:
                return latest_image
    time.sleep(1)
    
demo = gr.Interface(fn=generate_image,inputs=["text","text"], outputs=["image"])


demo.launch()

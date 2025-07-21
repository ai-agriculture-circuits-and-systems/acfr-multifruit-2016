import os
import json
import time
import random
from PIL import Image

def get_image_info(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        format = img.format
    size = os.path.getsize(image_path)
    return width, height, size, format

def load_labelsmap(labelmap_path):
    with open(labelmap_path, 'r') as f:
        labels = json.load(f)
    # labels is a list of dicts with object_id, label_id, object_name
    categories = []
    for item in labels:
        categories.append({
            "id": int(item.get("label_id", item.get("object_id", 0))),
            "name": item["object_name"],
            "supercategory": item["object_name"]
        })
    return categories

def load_annotation(annotation_path):
    if not os.path.exists(annotation_path):
        return []
    with open(annotation_path, 'r') as f:
        try:
            ann = json.load(f)
        except Exception:
            return []
    if isinstance(ann, dict):
        return [ann]
    return ann

def generate_unique_id():
    base = random.randint(1000000000, 9999999999)
    last3 = int(str(int(time.time() * 1000))[-3:])
    return int(str(base)[:-3] + f"{last3:03d}")

def process_folder(folder):
    images_dir = os.path.join(folder, "images")
    annotations_dir = os.path.join(folder, "annotations")
    labelmap_path = os.path.join(folder, "labelmap.json")
    categories = load_labelsmap(labelmap_path)

    for img_file in os.listdir(images_dir):
        if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img_path = os.path.join(images_dir, img_file)
        width, height, size, format = get_image_info(img_path)
        ann_file_json = os.path.splitext(img_file)[0] + ".json"
        ann_file_txt = os.path.splitext(img_file)[0] + ".txt"
        ann_path_json = os.path.join(annotations_dir, ann_file_json)
        ann_path_txt = os.path.join(annotations_dir, ann_file_txt)
        if os.path.exists(ann_path_json):
            annotations = load_annotation(ann_path_json)
        elif os.path.exists(ann_path_txt):
            with open(ann_path_txt, 'r') as f:
                annotations = f.read().splitlines()
        else:
            annotations = []

        out_json = {
            "info": {
                "description": "data",
                "version": "1.0",
                "year": 2025,
                "contributor": "search engine",
                "source": "augmented",
                "license": {
                    "name": "Creative Commons Attribution 4.0 International",
                    "url": "https://creativecommons.org/licenses/by/4.0/"
                }
            },
            "images": [
                {
                    "id": generate_unique_id(),
                    "width": width,
                    "height": height,
                    "file_name": img_file,
                    "size": size,
                    "format": format,
                    "url": "",
                    "hash": "",
                    "status": "success"
                }
            ],
            "annotations": annotations,
            "categories": categories
        }
        out_path = os.path.join(images_dir, os.path.splitext(img_file)[0] + ".json")
        with open(out_path, 'w') as f:
            json.dump(out_json, f, indent=2)

if __name__ == "__main__":
    for fruit in ["almonds", "apples", "mangoes"]:
        if os.path.exists(fruit):
            process_folder(fruit) 
# ACFR Multifruit Dataset 2016

<<<<<<< HEAD
A comprehensive dataset of fruit images collected from different farms across Australia, designed for fruit detection, classification, and segmentation tasks. The dataset includes images and annotations for apples, mangoes, and almonds.
=======
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/) [![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#changelog)
>>>>>>> 92bf405

High-quality orchard imagery for fruit detection and instance recognition across apples, mangoes, and almonds. Suitable for object detection, segmentation (apples), and yield-estimation experiments.

<<<<<<< HEAD
The ACFR Multifruit Dataset contains high-resolution images of three different fruit types collected at various Australian farms. This dataset is specifically designed for computer vision and deep learning applications in agricultural detection, classification, and segmentation tasks.
=======
- Project page: `https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/`
>>>>>>> 92bf405

## TL;DR
- Task: detection (+ segmentation for apples)
- Modality: RGB • Platform: ground • Real/Synthetic: real
- Images: Apples 1,120 • Mangoes 1,964 • Almonds 620 • Resolution: 308×202 (apples/almonds), 500×500 (mangoes)
- Annotations: per-image CSV (x,y,r or x,y,w,h); apples include per-pixel masks
- License: CC BY-NC 4.0 (see License)
- Citation: see below

<<<<<<< HEAD
| Fruit   | Image Info                                                                                     | Annotation Info                                      | Notes                                                               |
| ------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| Apples  | 1,120 Images, PNG, 308x202, 8-bit/color RGB, Sensor: PointGrey Ladybug3                       | Circle Annotation (x,y,radius), Pixel-wise annotation | Collected at Warburton, Australia. Apple varieties: Pink Lady, Kanzi |
| Mangoes | 1,964 Images, PNG, 500x500, 16-bit/color RGB, Sensor: Prosilica GT3300c, Strobes Used         | Rectangle Annotation (x,y,dx,dy)                     | Collected at Bundaberg, Australia. Mango varieties: Calypso          |
| Almonds | 620 Images, PNG, 308x202, 8-bit/color RGB, Sensor: Canon EOS60D                               | Rectangle Annotation (x,y,dx,dy)                     | Collected at Mildura, Australia. Almond variety: Nonpareil           |
=======
## What's inside
- [Download](#download)
- [Dataset structure](#dataset-structure)
- [Annotation schema](#annotation-schema)
- [Stats and splits](#stats-and-splits)
- [Quick start](#quick-start)
- [Evaluation and baselines](#evaluation-and-baselines)
- [Datasheet (data card)](#datasheet-data-card)
- [Known issues and caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)
>>>>>>> 92bf405

## Download
- Original dataset: `https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/`
- This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.
- Local license file: see `LICENSE` (Creative Commons Attribution-NonCommercial 4.0).

## Dataset structure
```
acfr-multifruit-2016/
├── almonds/
<<<<<<< HEAD
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   └── sets/
├── apples/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   ├── segmentations/
=======
│   ├── annotations/           # CSV per image
│   ├── images/                # PNG images
│   ├── labelmap.json
│   └── sets/                  # train.txt / val.txt / test.txt
├── apples/
│   ├── annotations/           # CSV per image (circles)
│   ├── images/
│   ├── labelmap.json
│   ├── segmentations/         # PNG masks (apples only)
>>>>>>> 92bf405
│   └── sets/
├── mangoes/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   └── sets/
<<<<<<< HEAD
└── README.md
```

- `images/`: Contains the fruit images.
- `annotations/`: Contains annotation files for each image (format may be JSON or TXT).
- `labelmap.json`: List of label definitions for the dataset.
- `sets/`: Dataset splits for training, testing, and validation.
- `segmentations/`: (Apples only) Contains pixel-wise segmentation masks.

## Annotation JSON Structure

Each image can be associated with a COCO-style annotation JSON file, generated automatically. The structure is as follows:

```
{
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
      "id": 1234567890,
      "width": 640,
      "height": 640,
      "file_name": "example.jpg",
      "size": 68187,
      "format": "JPEG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [
    // Annotation objects, e.g. bounding boxes, segmentations, etc.
  ],
  "categories": [
    {
      "id": 1,
      "name": "almond",
      "supercategory": "almond"
    }
    // ...
  ]
}
```

- `info`: Metadata about the dataset and license.
- `images`: List of image metadata (id, size, file name, etc.).
- `annotations`: List of annotation objects for the image (bounding boxes, segmentations, etc.).
- `categories`: List of category definitions, derived from `labelmap.json`.

## labelmap.json Structure

The `labelmap.json` file in each fruit directory is a list of label definitions. Example:

```
[
  {
    "object_id": 0,
    "label_id": 0,
    "keyboard_shortcut": "0",
    "object_name": "background"
  },
  {
    "object_id": 1,
    "label_id": 1,
    "keyboard_shortcut": "1",
    "object_name": "almond"
  }
]
```

- `label_id`: The integer ID for the label/category.
- `object_name`: The name of the object/category.

## Generating COCO-style Annotation Files

A Python script `generate_annotations.py` is provided to automatically generate COCO-style annotation JSON files for each image in the `images/` folders of almonds, apples, and mangoes.

### Requirements
- Python 3.x
- Pillow

Install dependencies (if needed):
```
pip install pillow
```

### Usage
Run the script from the root of the dataset:
```
python generate_annotations.py
```

This will generate a JSON file for each image in the `images/` folder of each fruit type, with the same base name as the image (e.g., `image1.jpg` → `image1.json`).

### Output
- Each generated JSON file will be saved in the same directory as the corresponding image.
- The JSON structure follows the format described above.

## Segmentation Annotations (Apples Only)

The `apples/segmentations/` directory contains pixel-wise segmentation masks for apple images. The `segmentation` field in annotation JSONs refers to the polygon or mask data for instance segmentation tasks, enabling pixel-level object detection.
=======
├── annotations/               # COCO JSON output 
├── scripts/
│   └── convert_to_coco.py     # conversion utility
└── README.md
```
- Splits: `sets/train.txt`, `sets/val.txt`, `sets/test.txt` (and also `all.txt`, `train_val.txt`) list image basenames (no extension). If missing, all images are used.

## Annotation schema
- CSV per-image schemas:
  - Apples (circles): columns include `x, y, r` (radius in pixels). Converted to COCO bbox `[x-r, y-r, 2r, 2r]`.
  - Mangoes/Almonds (rectangles): columns include `x, y, w, h` or `dx, dy` or `width, height`.
- COCO-style (generated):
```json
{
  "info": {"year": 2016, "version": "1.0.0", "description": "ACFR 2016 <fruit> <split>", "url": "https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/"},
  "images": [{"id": 1, "file_name": "apples/images/IMG_0001.png", "width": 308, "height": 202}],
  "categories": [{"id": 1, "name": "apple", "supercategory": "fruit"}],
  "annotations": [{"id": 10, "image_id": 1, "category_id": 1, "bbox": [x, y, w, h], "area": 1234, "iscrowd": 0}]
}
```

- Label maps: each fruit folder includes a `labelmap.json` for original IDs; the provided converter normalizes to a single category per fruit. In combined mode, categories are assigned as: `apple=1`, `mango=2`, `almond=3`.

## Stats and splits
- Apples: 1,120 images; Mangoes: 1,964 images; Almonds: 620 images.
- Splits provided via `sets/*.txt`. You may define your own splits by editing those files.

## Quick start
Python (COCO):
```python
from pycocotools.coco import COCO
coco = COCO("annotations/apples_instances_train.json")
img_ids = coco.getImgIds()
img = coco.loadImgs(img_ids[0])[0]
ann_ids = coco.getAnnIds(imgIds=img['id'])
anns = coco.loadAnns(ann_ids)
```
Convert CSV to COCO JSON:
```bash
python scripts/convert_to_coco.py --root . --out annotations --fruits apples mangoes almonds --splits train val test --combined
```

Dependencies:
```bash
python -m pip install pillow
```
Optional for the COCO API example:
```bash
python -m pip install pycocotools
```
>>>>>>> 92bf405

## Evaluation and baselines
- Metric: mAP@[.50:.95] for detection; report F1 for historical comparison if desired.
- Reference F1 (original paper): Apple 0.904, Mango 0.908, Almond 0.775.

<<<<<<< HEAD
This dataset can be used for:
- Fruit detection and classification
- Instance and semantic segmentation
- Computer vision research
- Deep learning model training
- Agricultural AI applications
- Yield estimation
- Automated fruit sorting systems

=======
## Datasheet (data card)
- Motivation: fruit detection and yield estimation in orchards.
- Composition: RGB images across apples, mangoes, almonds; apples include segmentation masks.
- Collection process: Australian orchards; sensors include PointGrey Ladybug3, Prosilica GT3300c, Canon EOS60D.
- Preprocessing: none required; use provided image sizes.
- Distribution: data hosted by ACFR; this repo provides ancillary scripts.
- Maintenance: community contributions via issue tracker.

## Known issues and caveats
- CSV headers vary; the converter handles common variants but may need updates for edge cases.
- Apple masks exist only for apples; other fruits have boxes only.
- Image extensions may vary (`.png` vs `.jpg`); the converter tries both.
- Coordinates are in pixel units with origin at the image top-left. Ensure downstream tooling expects absolute COCO boxes.

## License
- Creative Commons Attribution-NonCommercial 4.0 (`LICENSE`). Check the original dataset terms and cite appropriately.

>>>>>>> 92bf405
## Citation
```bibtex
@article{bargoti2016deep,
  title={Deep Fruit Detection in Orchards},
  author={Bargoti, Suchet and Underwood, James},
  journal={arXiv preprint arXiv:1610.03677},
  year={2016}
}

@article{Bargoti2016,
  title={Image Segmentation for Fruit Detection and Yield Estimation in Apple Orchards},
  author={Bargoti, Suchet and Underwood, James},
  journal={Journal of Field Robotics},
  year={2016}
}
```

## Changelog
- v1.0.0: initial structure and COCO conversion utility

## Contact
- Maintainers: Open to contributions via issue tracker.
- Original authors (per dataset page): Suchet Bargoti and James Underwood.
- Source: `https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/`
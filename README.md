# ACFR Multifruit Dataset 2016

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/) 
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#changelog)

High-quality orchard imagery for fruit detection and instance recognition across apples, mangoes, and almonds. Suitable for object detection, segmentation (apples), and yield-estimation experiments.

- Project page: `https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/`

## TL;DR
- Task: detection (+ segmentation for apples)
- Modality: RGB • Platform: ground • Real/Synthetic: real
- Images: Apples 1,120 • Mangoes 1,964 • Almonds 620 • Resolution: 308×202 (apples/almonds), 500×500 (mangoes)
- Annotations: per-image CSV (x,y,r or x,y,w,h); apples include per-pixel masks
- License: CC BY-NC 4.0 (see License)
- Citation: see below

## What's inside
- Download
- Dataset structure
- Annotation schema
- Stats and splits
- Quick start
- Evaluation and baselines
- Datasheet (data card)
- Known issues and caveats
- License
- Citation
- Changelog
- Contact

## Download
- Original dataset: `https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/`
- This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.
- Local license file: see `LICENSE` (Creative Commons Attribution-NonCommercial 4.0).

## Dataset structure
```
acfr-multifruit-2016/
├── almonds/
│   ├── annotations/           # CSV per image
│   ├── images/                # PNG images
│   ├── labelmap.json
│   └── sets/                  # train.txt / val.txt / test.txt
├── apples/
│   ├── annotations/           # CSV per image (circles)
│   ├── images/
│   ├── labelmap.json
│   ├── segmentations/         # PNG masks (apples only)
│   └── sets/
├── mangoes/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   └── sets/
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

## Evaluation and baselines
- Metric: mAP@[.50:.95] for detection; report F1 for historical comparison if desired.
- Reference F1 (original paper): Apple 0.904, Mango 0.908, Almond 0.775.

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
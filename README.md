# ACFR Multifruit Dataset 2016

A comprehensive dataset of fruit images collected from different farms across Australia, designed for fruit detection, classification, and segmentation tasks. The dataset includes images and annotations for apples, mangoes, and almonds.

## Dataset Description

The ACFR Multifruit Dataset contains high-resolution images of three different fruit types collected at various Australian farms. This dataset is specifically designed for computer vision and deep learning applications in agricultural detection, classification, and segmentation tasks.

### Data Summary

| Fruit   | Image Info                                                                                     | Annotation Info                                      | Notes                                                               |
| ------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| Apples  | 1,120 Images, PNG, 308x202, 8-bit/color RGB, Sensor: PointGrey Ladybug3                       | Circle Annotation (x,y,radius), Pixel-wise annotation | Collected at Warburton, Australia. Apple varieties: Pink Lady, Kanzi |
| Mangoes | 1,964 Images, PNG, 500x500, 16-bit/color RGB, Sensor: Prosilica GT3300c, Strobes Used         | Rectangle Annotation (x,y,dx,dy)                     | Collected at Bundaberg, Australia. Mango varieties: Calypso          |
| Almonds | 620 Images, PNG, 308x202, 8-bit/color RGB, Sensor: Canon EOS60D                               | Rectangle Annotation (x,y,dx,dy)                     | Collected at Mildura, Australia. Almond variety: Nonpareil           |

## Dataset Structure

```
acfr-multifruit-2016/
├── almonds/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   └── sets/
├── apples/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   ├── segmentations/
│   └── sets/
├── mangoes/
│   ├── annotations/
│   ├── images/
│   ├── labelmap.json
│   └── sets/
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

## Applications

This dataset can be used for:
- Fruit detection and classification
- Instance and semantic segmentation
- Computer vision research
- Deep learning model training
- Agricultural AI applications
- Yield estimation
- Automated fruit sorting systems

## Citation

When using this dataset in your research, please cite:

1. For fruit level annotations:
```
@article{bargoti2016deep,
  title={Deep Fruit Detection in Orchards},
  author={Bargoti, Suchet and Underwood, James},
  journal={arXiv preprint arXiv:1610.03677},
  year={2016}
}
```

2. For pixel level segmentations (apple only):
```
@article{Bargoti2016,
  author={Bargoti, Suchet and Underwood, James},
  journal={To Appear in Journal of Field Robotics},
  title={Image Segmentation for Fruit Detection and Yield Estimation in Apple Orchards},
  year={2016}
}
```

## Contact

For any questions, please contact:
- James Underwood: james.underwood@sydney.edu.au
- Suchet Bargoti: suchet.bargoti@sydney.edu.au

## Source

The dataset is available at: https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/ 
# ACFR Multifruit Dataset 2016

A comprehensive dataset of fruit images collected from different farms across Australia, designed for fruit detection and classification tasks. The dataset includes images and annotations for apples, mangoes, and almonds.

## Dataset Description

The ACFR Multifruit Dataset contains high-resolution images of three different fruit types collected at various Australian farms. This dataset is specifically designed for computer vision and deep learning applications in agricultural detection and classification tasks.

### Data Summary

| Fruit   | Image Info                                                                                    | Annotation Info                                      | Notes                                                               |
| ------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| Apples  | 1,120 Images PNG Image Data 308 x 202, 8-bit/color RGB Sensor: PointGrey Ladybug3              | Circle Annotation (x,y,radius) Pixel-wise annotation | Collected at Warburton, Australia Apple varieties: Pink Lady, Kanzi |
| Mangoes | 1,964 Images PNG Image Data 500 x 500, 16-bit/color RGB Sensor: Prosilica GT3300c Strobes Used | Rectangle Annotation (x,y,dx,dy)                     | Collected at Bundaberg, Australia Mango varieties: Calypso          |
| Almonds | 620 Images PNG Image Data 308 x 202, 8-bit/color RGB Sensor: Canon EOS60D                     | Rectangle Annotation (x,y,dx,dy)                     | Collected at Mildura, Australia Almond variety: Nonpareil           |

## Dataset Structure

```
acfr-fruit-dataset
├── almonds
│   ├── annotations
│   ├── images
│   ├── labelmap.json
│   └── sets
├── apples
│   ├── annotations
│   ├── images
│   ├── labelmap.json
│   ├── segmentations
│   └── sets
├── mangoes
│   ├── annotations
│   ├── images
│   ├── labelmap.json
│   └── sets
└── readme.txt
```

Each fruit directory contains:
- `images/`: Contains the fruit images
- `annotations/`: Contains corresponding .csv files with fruit annotation information
- `labelmap.json`: Mapping file for labels to IDs
- `sets/`: Dataset splits for training, testing, and validation
- `segmentations/`: (Apples only) Contains pixel-wise annotations

## Model Performance

The fruit detection F1-scores as reported in the original paper:

| Fruit  | F1-score |
| ------ | -------- |
| Apple  | 0.904    |
| Mango  | 0.908    |
| Almond | 0.775    |

## Applications

This dataset can be used for:
- Fruit detection in orchards
- Computer vision research
- Deep learning model training
- Agricultural AI applications
- Yield estimation
- Automated fruit sorting systems

## Categories

- Computer Science
- Artificial Intelligence
- Computer Vision
- Object Detection
- Machine Learning
- Agriculture
- Deep Learning
- Fruit Recognition

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
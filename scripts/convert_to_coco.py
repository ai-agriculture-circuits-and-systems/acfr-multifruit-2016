# SPDX-License-Identifier: CC-BY-NC-4.0

"""Convert ACFR Multifruit 2016 annotations to COCO JSON.

License: CC BY-NC 4.0 (see LICENSE). This script is distributed alongside the
dataset and follows the same non-commercial usage terms. Cite the original ACFR
dataset in publications.

This script converts per-image CSV annotations in the ACFR Multifruit 2016
dataset into COCO-style JSON files, per fruit and/or combined across fruits.

Usage examples:
    python scripts/convert_to_coco.py --root . --out annotations --fruits apples \
        --splits train val test

    python scripts/convert_to_coco.py --root . --out annotations --fruits apples mangoes almonds \
        --splits train val --combined

Notes:
- Apples may use circle annotations (x, y, r). This script converts circles to
  COCO bounding boxes using [x - r, y - r, 2r, 2r].
- Mangoes/Almonds typically use rectangle annotations with width/height.
- The script attempts to robustly detect column names (case-insensitive) among
  common variants: x, y, r, w, h, dx, dy, width, height.

This code is intentionally verbose and defensive to ease maintenance.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Literal, Optional, Sequence, Tuple

from PIL import Image


FruitName = Literal["apples", "mangoes", "almonds"]
SplitName = Literal["train", "val", "test"]


@dataclass(frozen=True)
class CsvBox:
    """Normalized representation of a single annotation box.

    Always stored as COCO bbox [x, y, width, height] in pixel units.
    """

    x: float
    y: float
    width: float
    height: float


def _lower_keys(mapping: Dict[str, str]) -> Dict[str, str]:
    """Return a case-insensitive mapping by lowering keys.

    Args:
        mapping: Original header-to-index mapping as produced by DictReader.

    Returns:
        Mapping with lowered keys for robust lookups.
    """

    return {k.lower(): v for k, v in mapping.items()}


def _circle_to_bbox(x: float, y: float, r: float) -> CsvBox:
    """Convert circle center and radius to a bounding box.

    Args:
        x: Circle center x in pixels.
        y: Circle center y in pixels.
        r: Circle radius in pixels.

    Returns:
        CsvBox with top-left x, y and width, height.
    """

    return CsvBox(x=x - r, y=y - r, width=2 * r, height=2 * r)


def _rect_to_bbox(x: float, y: float, w: float, h: float) -> CsvBox:
    """Create a CsvBox from rectangle parameters.

    Args:
        x: Top-left x in pixels.
        y: Top-left y in pixels.
        w: Width in pixels.
        h: Height in pixels.

    Returns:
        CsvBox with top-left x, y and width, height.
    """

    return CsvBox(x=x, y=y, width=w, height=h)


def _read_split_list(split_file: Path) -> List[str]:
    """Read image base names (without extension) from a split file.

    Args:
        split_file: Path to a split list, one image id per line.

    Returns:
        List of image stems (without extension).
    """

    if not split_file.exists():
        return []
    lines = [line.strip() for line in split_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]


def _image_size(image_path: Path) -> Tuple[int, int]:
    """Return (width, height) for an image path using PIL.

    Args:
        image_path: Path to an image file.

    Returns:
        A tuple of (width, height) in pixels.
    """

    with Image.open(image_path) as img:
        return img.width, img.height


def _parse_csv_boxes(csv_path: Path) -> List[CsvBox]:
    """Parse a single per-image CSV file and return COCO-style bboxes.

    The parser is resilient to header variants by using case-insensitive
    lookups. Supported schemas:
      - Circle: x, y, r
      - Rectangle: x, y, w/h or dx/dy or width/height

    Args:
        csv_path: Path to a CSV annotation file.

    Returns:
        List of CsvBox objects found in the CSV.
    """

    if not csv_path.exists():
        return []

    boxes: List[CsvBox] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return boxes
        header = _lower_keys({k: k for k in reader.fieldnames})
        # Column candidates
        def get(row: Dict[str, str], *keys: str) -> Optional[float]:
            for key in keys:
                if key in row and row[key] not in (None, ""):
                    try:
                        return float(row[key])
                    except ValueError:
                        continue
            return None

        for raw_row in reader:
            row = {k.lower(): v for k, v in raw_row.items()}
            x = get(row, "x", "xc", "x_center")
            y = get(row, "y", "yc", "y_center")
            # Circle
            r = get(row, "r", "radius")
            # Rectangle sizes
            w = get(row, "w", "width", "dx")
            h = get(row, "h", "height", "dy")

            if x is None or y is None:
                # Skip rows without coordinates
                continue
            if r is not None:
                boxes.append(_circle_to_bbox(x, y, r))
            elif w is not None and h is not None:
                boxes.append(_rect_to_bbox(x, y, w, h))
            else:
                # No supported schema found; skip.
                continue

    return boxes


def _collect_annotations_for_split(
    fruit_root: Path,
    split: SplitName,
    fruit_name: FruitName,
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    """Collect COCO dictionaries for images, annotations, and categories.

    Args:
        fruit_root: Root directory for a single fruit, e.g., `apples`.
        split: One of "train", "val", or "test".
        fruit_name: Fruit name literal used for category naming.

    Returns:
        A tuple of (images, annotations, categories) COCO lists for the split.
    """

    images_dir = fruit_root / "images"
    annotations_dir = fruit_root / "annotations"
    sets_dir = fruit_root / "sets"

    split_file = sets_dir / f"{split}.txt"
    image_stems = set(_read_split_list(split_file))
    if not image_stems:
        # If no split list is provided, fall back to all images
        image_stems = {p.stem for p in images_dir.glob("*.png")}

    images: List[Dict[str, object]] = []
    anns: List[Dict[str, object]] = []
    categories: List[Dict[str, object]] = [
        {"id": 1, "name": fruit_name[:-1] if fruit_name.endswith("s") else fruit_name, "supercategory": "fruit"}
    ]

    image_id_counter = 1
    ann_id_counter = 1
    for stem in sorted(image_stems):
        img_path = images_dir / f"{stem}.png"
        if not img_path.exists():
            # Try JPG fallback if PNG not found
            jpg_path = images_dir / f"{stem}.jpg"
            if jpg_path.exists():
                img_path = jpg_path
            else:
                continue
        width, height = _image_size(img_path)
        images.append(
            {
                "id": image_id_counter,
                "file_name": str(img_path.relative_to(fruit_root.parent)),
                "width": width,
                "height": height,
            }
        )

        csv_path = annotations_dir / f"{stem}.csv"
        for box in _parse_csv_boxes(csv_path):
            anns.append(
                {
                    "id": ann_id_counter,
                    "image_id": image_id_counter,
                    "category_id": 1,
                    "bbox": [box.x, box.y, box.width, box.height],
                    "area": box.width * box.height,
                    "iscrowd": 0,
                }
            )
            ann_id_counter += 1

        image_id_counter += 1

    return images, anns, categories


def _merge_coco_splits(
    per_fruit: List[Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]],
    fruit_names: Sequence[FruitName],
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    """Merge multiple single-category COCO lists into a multi-category dataset.

    Categories are assigned ids in order of `fruit_names` and annotations remapped
    to the proper category id based on source fruit order.
    """

    images: List[Dict[str, object]] = []
    anns: List[Dict[str, object]] = []
    categories: List[Dict[str, object]] = []

    # Map each fruit to category id
    fruit_to_cat: Dict[FruitName, int] = {}
    for idx, fruit in enumerate(fruit_names, start=1):
        categories.append(
            {"id": idx, "name": fruit[:-1] if fruit.endswith("s") else fruit, "supercategory": "fruit"}
        )
        fruit_to_cat[fruit] = idx

    # Remap ids to keep uniqueness across fruits
    next_image_id = 1
    next_ann_id = 1
    for (img_list, ann_list, _cats), fruit in zip(per_fruit, fruit_names):
        # Create mapping from old image id to new merged id
        id_map: Dict[int, int] = {}
        for img in img_list:
            old_id = int(img["id"])  # type: ignore[reportGeneralTypeIssues]
            new_img = dict(img)
            new_img["id"] = next_image_id
            images.append(new_img)
            id_map[old_id] = next_image_id
            next_image_id += 1

        for ann in ann_list:
            new_ann = dict(ann)
            new_ann["id"] = next_ann_id
            new_ann["image_id"] = id_map[int(ann["image_id"]) ]  # type: ignore[index]
            new_ann["category_id"] = fruit_to_cat[fruit]
            anns.append(new_ann)
            next_ann_id += 1

    return images, anns, categories


def _build_coco_dict(
    images: List[Dict[str, object]],
    anns: List[Dict[str, object]],
    categories: List[Dict[str, object]],
    description: str,
) -> Dict[str, object]:
    """Build a complete COCO dict from components.

    Args:
        images: COCO images list.
        anns: COCO annotations list.
        categories: COCO categories list.
        description: Short description for the info block.

    Returns:
        COCO dictionary ready to `json.dump`.
    """

    return {
        "info": {
            "year": 2016,
            "version": "1.0.0",
            "description": description,
            "url": "https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/",
        },
        "images": images,
        "annotations": anns,
        "categories": categories,
        "licenses": [],
    }


def convert(
    root: Path,
    out_dir: Path,
    fruits: Sequence[FruitName],
    splits: Sequence[SplitName],
    combined: bool,
) -> None:
    """Convert selected fruits and splits to COCO JSON files.

    Args:
        root: Dataset root directory containing `apples/`, `mangoes/`, `almonds/`.
        out_dir: Output directory to write JSON files into.
        fruits: Fruits to include.
        splits: Splits to generate.
        combined: Whether to also produce combined multi-class JSON files.
    """

    out_dir.mkdir(parents=True, exist_ok=True)

    for split in splits:
        # Per-fruit conversion
        per_fruit_results: List[Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]] = []
        for fruit in fruits:
            fruit_root = root / fruit
            images, anns, categories = _collect_annotations_for_split(fruit_root, split, fruit)
            desc = f"ACFR 2016 {fruit} {split} split"
            coco = _build_coco_dict(images, anns, categories, desc)
            out_path = out_dir / f"{fruit}_instances_{split}.json"
            out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
            per_fruit_results.append((images, anns, categories))

        if combined:
            images, anns, categories = _merge_coco_splits(per_fruit_results, fruits)
            desc = f"ACFR 2016 combined {split} split ({', '.join(fruits)})"
            coco = _build_coco_dict(images, anns, categories, desc)
            out_path = out_dir / f"combined_instances_{split}.json"
            out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional sequence of arguments for testing. Defaults to sys.argv.

    Returns:
        Parsed argparse namespace.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Dataset root containing fruit subfolders (default: dataset root)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "annotations",
        help="Output directory for COCO JSON files (default: <root>/annotations)",
    )
    parser.add_argument(
        "--fruits",
        nargs="+",
        type=str,
        default=["apples", "mangoes", "almonds"],
        choices=["apples", "mangoes", "almonds"],
        help="Fruits to include (default: apples mangoes almonds)",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        type=str,
        default=["train", "val", "test"],
        choices=["train", "val", "test"],
        help="Dataset splits to generate (default: train val test)",
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Also produce a combined multi-class JSON per split",
    )

    args = parser.parse_args(argv)

    # Coerce to typed literals at runtime
    args.fruits = [f for f in args.fruits]  # type: ignore[attr-defined]
    args.splits = [s for s in args.splits]  # type: ignore[attr-defined]
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the converter CLI.

    Args:
        argv: Optional list of CLI arguments for testing.

    Returns:
        Exit code integer (0 on success).
    """

    args = _parse_args(argv)
    convert(
        root=Path(args.root),
        out_dir=Path(args.out),
        fruits=[f for f in args.fruits],
        splits=[s for s in args.splits],
        combined=bool(args.combined),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



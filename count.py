from ultralytics import YOLO
import numpy as np
import argparse
import cv2
import sys
import os


parser = argparse.ArgumentParser(description="Detect palm tree from aerial imaging. Specify chosen model and input image to detect.")
parser.add_argument("-q", "--quiet", action="store_true", help="minimize output information in quiet mode.")
parser.add_argument("-i", "--image", required=True, type=str, help="specify the path to input image.")
parser.add_argument("-m", "--model", required=True, type=str, help="specify the path to model weights.")
parser.add_argument("-o", "--output", default="output.jpg", type=str, help="where the output is saved. defaults to output.jpg.")
parser.add_argument("-t", "--target-tile-size", default=None, type=int, help="tiles the input image target tilesize in pixels. not tiling if this option isn't specified.")

args = parser.parse_args()
IMAGEPATH = args.image
MODELPATH = args.model
OUTPATH = args.output
TILING = args.target_tile_size
qprint = lambda text: print(text) if not args.quiet else None

if not os.path.exists(IMAGEPATH):
    raise FileNotFoundError(f"Image file {IMAGEPATH} doesn't exist!")
if not os.path.exists(MODELPATH):
    raise FileNotFoundError(f"Model file {MODELPATH} doesn't exist!")

image = cv2.imread(IMAGEPATH)
imageH, imageW, _ = np.shape(image)
qprint(f"Input image height: {imageH}, width: {imageW}")
if TILING and (imageH > 3084 or imageW > 3084):
    nVert = imageH // TILING + 1
    nHori = imageW // TILING + 1
    tileHeight = imageH // nVert # several pixels will be clipped but not a problem
    tileWidth = imageW // nHori
    patch_list = []
    for i in range(nVert):
        for j in range(nHori):
            patch_row = i * tileHeight
            patch_col = j * tileWidth
            patch_list.append(image[patch_row : patch_row + tileHeight, patch_col : patch_col + tileWidth, :])
    image = patch_list
    qprint(f"Input image tiled into {nVert} x {nHori} tiles.\nTile size: {tileHeight} x {tileWidth} pixels.")
else:
    image = image if isinstance(image, list) else [image]
    qprint("Input image not tiled.")

model = YOLO(MODELPATH)
results = model(image, imgsz=640, iou=.6, conf=.35)

last_idx = 0
for j, (r, orig_img) in enumerate(zip(results, image)):
    xyxy = r.boxes.xyxy.cpu().numpy().astype(np.int32)
    conf = r.boxes.conf.cpu().numpy().astype(np.float32)

    for i, c in enumerate(xyxy):
        cv2.rectangle(orig_img, c[:2], c[-2:], (255, 0, 0), 5)
        cv2.putText(orig_img, f"{i + last_idx}", [c[0], c[1] - 10], cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 120), 3)
    last_idx += i

    border_width= 8 # SET TO 0 UNTUK HILANGKAN BORDER BEETWEEN TILES
    if len(results) > 1:
        orig_img = cv2.copyMakeBorder(
            orig_img,
            top=border_width,
            bottom=border_width,
            left=border_width,
            right=border_width,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )
    image[j] = orig_img

if len(results) > 1:
    image = np.concatenate([np.concatenate(image[i * nHori : (i + 1) * nHori], axis=1) for i in range(nVert)], axis=0)
else:
    image = image[0]

if cv2.imwrite(OUTPATH, image):
    qprint(f"Image saved into {OUTPATH}")
else:
    raise RuntimeError(f"Output image fails to be saved at {OUTPATH}")

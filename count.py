from ultralytics import YOLO
import numpy as np
import cv2
import sys
import os

if len(sys.argv)%2 == 0:
    raise SyntaxError("Invalid program call. Valid call: `python3 count.py --modelpath to/sawit/model.pt --imagepath to/your/image.jpg --target-tile-size 1280 --output sawit-detection.jpg`")

IMAGEPATH = None
MODELPATH = None
OUTPATH = None
TILING = None
for i, arg in enumerate(sys.argv):
    if i%2 == 0:
        continue
    if arg == "--imagepath":
        if not os.path.exists(sys.argv[i + 1]):
            raise FileNotFoundError(f"File {sys.argv[i + 1]} doesn't exist! Specify aerial sawit image.")
        IMAGEPATH = sys.argv[i + 1]
    elif arg == "--target-tile-size":
        TILING = int(sys.argv[i + 1])
    elif arg == "--modelpath":
        if not os.path.exists(sys.argv[i + 1]):
            raise FileNotFoundError(f"File {sys.argv[i + 1]} doesn't exist! Specify path to sawit model.")
        MODELPATH = sys.argv[i + 1]
    elif arg == "--output":
        OUTPATH = sys.argv[i + 1]
    else:
        raise TypeError(f"Flag {arg} does not exist.")
    
if MODELPATH is None:
    raise RuntimeError("Model hasn't been specified.")
if IMAGEPATH is None:
    raise RuntimeError("Image han't been specified.")
if OUTPATH is None:
    OUTPATH = "output.jpg"

image = cv2.imread(IMAGEPATH)
imageH, imageW, _ = np.shape(image)
print(f"image height: {imageH}, image width: {imageW}")
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
image = image if isinstance(image, list) else [image]

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

    border_width= 8
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
cv2.imwrite(OUTPATH, image)

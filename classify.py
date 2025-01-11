from ultralytics import YOLO
import numpy as np
import argparse
import cv2
import os


def red_yellow_green(image: np.ndarray, mask: np.ndarray):
    image = image[:, :, 1:]
    image_filtered = image[mask]
    median_green_red_delta = np.median(image_filtered[:, 0].astype(np.int32) - image_filtered[:, 1].astype(np.int32)) # ascending of (green - red)

    if median_green_red_delta < -45:
        return "red"
    elif median_green_red_delta < 0:
        return "yellow"
    else:
        return "green"

parser = argparse.ArgumentParser(description="Detect palm tree from aerial imaging. Specify chosen model and input image to detect.")
parser.add_argument("-q", "--quiet", action="store_true", help="minimize output information in quiet mode.")
parser.add_argument("-i", "--image", required=True, type=str, help="specify the path to input image.")
parser.add_argument("-o", "--output", default=".", type=str, help="the directory the output is saved. defaults to current directory.")
parser.add_argument("-s", "--seg", action="store_true", help="provides segmented apple images. ")

args = parser.parse_args()
IMAGEPATH = args.image
OUTPATH = args.output
qprint = lambda text: print(text) if not args.quiet else None

if not os.path.exists(IMAGEPATH):
    raise FileNotFoundError(f"Image file {IMAGEPATH} doesn't exist!")

model = YOLO("yolo11x-seg.pt") # just use pretrained model. it detects apple (COCO-17)
image = cv2.imread(IMAGEPATH)
imageH, imageW, _ = np.shape(image)

if not (os.path.exists(OUTPATH) and os.path.isdir(OUTPATH)):
    os.makedirs(OUTPATH)
    qprint(f"Specified directory doesn't exist. Making new.")

results = model(image, imgsz=640, retina_masks=True, iou=.7, conf=.3, classes=[47])[0] # apple is 47
mask_arr = results.masks.data.cpu().numpy().astype(np.uint8).transpose((1, 2, 0)) # * 255
class_arr = results.boxes.cls.cpu().numpy().astype(np.uint32)
box_arr = results.boxes.xyxy.cpu().numpy().astype(np.uint32)

tempMask = []
tempBox = []
color_count = {"red": 0, "yellow": 0, "green": 0}
for i, cls in enumerate(class_arr):
    xmin, ymin, xmax, ymax = box_arr[i]
    patch_img = image[ymin:ymax, xmin:xmax, :] # vertical = y | horizontal = x
    patchW, patchH, _ = np.shape(patch_img)
    
    ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    patch_msk = mask_arr[ymin:ymax, xmin:xmax, i:i+1]
    patch_msk = cv2.erode(patch_msk.astype(np.uint8), ellipse_kernel).astype(np.bool)#[..., np.newaxis]
    
    patch_color = red_yellow_green(patch_img, patch_msk)
    patch_idx = color_count[patch_color]
    color_count[patch_color] += 1

    output_name = f"{patch_color}_{patch_idx}"
    full_path = os.path.join(OUTPATH, output_name)
    cv2.imwrite(f"{full_path}.jpg", patch_img)

    if args.seg:
        patch_seg = patch_img * patch_msk[..., np.newaxis]
        cv2.imwrite(f"{full_path}_seg.jpg", patch_seg)

qprint(f"Count: {color_count}")
qprint(f"Image(s) saved at: {'current dir' if OUTPATH == '.' else os.path.join(OUTPATH)} {'with segmentation' if args.seg else ''}")
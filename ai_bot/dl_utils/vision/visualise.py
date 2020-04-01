import os
import colorsys
import random
import skimage.io
import numpy as np

SAVEPATH = os.path.abspath("images/")
if not os.path.exists(SAVEPATH):
    os.mkdir(SAVEPATH)

##################################
# Detection Visualisation
##################################

class_id_to_name = [
                    "unlabeled", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
                    "street sign", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
                    "hat", "backpack", "umbrella", "shoe", "eye glasses", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "plate", "wine glass", "cup", "fork", "knife", "spoon",
                    "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
                    "bed", "mirror", "dining table", "window", "desk", "toilet", "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
                    "oven", "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush", "hair brush"
                ]

def random_colours(num, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / num, 1, brightness) for i in range(num)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask > 0.7,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def add_detections_to_images(names, images, predictions):
    # Dict to hold savepaths and objects found given image name
    image_path_objects = {}
    for name, image, prediction in zip(names, images, predictions):
        image_path_objects[name] = {"path": os.path.join(SAVEPATH, name),
                                    "objects": [],
                                    "probs": []}
        boxes = prediction["boxes"].numpy()
        labels = prediction["labels"].numpy()
        masks = prediction["masks"].numpy()
        scores = prediction["scores"].numpy()
        num_objects = boxes.shape[0]
        
        if num_objects == 0:
            continue
        
        colours = random_colours(num_objects)
        image = (image.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        masked_image = image.copy()

        for i in range(num_objects):
            class_id = labels[i]
            image_path_objects[name]["objects"].append(class_id_to_name[class_id])
            image_path_objects[name]["probs"].append(scores[i])
            colour = colours[i]

            mask = masks[i, 0, :, :]
            
            masked_image = apply_mask(masked_image, mask, colour)
        
        skimage.io.imsave(image_path_objects[name]["path"], masked_image)
    return image_path_objects
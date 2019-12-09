import os
import cv2
import numpy as np
import pyautogui
from config import coordinates
import image_reader as ir
import pickle

"""
Rec screen imgs into video without img save
"""


def main(option):
    if option == "rec":
        video_record()
    if option == "read_image":
        image_extractor()


# img basic crop tool
def crop_image(image, x, y, w, h):
    return image[y:y + h, x:x + w]


def set_path(folder_name):
    actual_path = os.getcwd() + "\\{0}".format(folder_name)
    directories = [x[0] for x in os.walk(actual_path)]
    try:
        next_folder = str(int(directories[-1][-1]) + 1)
    except ValueError:
        next_folder = str(0)
    except IndexError:
        next_folder = str(0)

    directory = actual_path + "\\" + next_folder + "\\"
    print("The current working directory is %s" % directory + "\n")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def video_record():
    output = "test.avi"
    video_output_path = set_path("video") + output
    img_path = set_path("img")

    # get info from pic
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width, channels = image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(video_output_path, fourcc, 20.0, (width, height))
    count = 0
    while True:
        try:
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            out.write(image)
            StopIteration(0.5)
            if count % 20 == 0:
                cv2.imwrite(img_path + str(count) + ".jpg", image)
                print("recording, step: ", count)
            count += 1
        except KeyboardInterrupt:  # ctrl+c
            print("stop recording")
            break

    out.release()
    cv2.destroyAllWindows()


def image_extractor():
    # load x,y,width,height screen coords from poker table
    coords = coordinates.load_coordinates()
    path = "img\\0"
    output_path = set_path("table_parts")
    # images = ir.image_reader(path)
    images = load_vars("coordinates")
    for i, image in enumerate(images):
        for key, coord in coords.items():
            x = coords[key]["x"]
            y = coords[key]["y"]
            width = coords[key]["width"]
            height = coords[key]["height"]
            cropped_image = crop_image(image, x, y, width, height)
            cv2.imwrite(output_path + key + "_" + str(i) + ".jpg", cropped_image)
    pass


def save_vars(content):
    with open("coordinates", "wb") as f:
        pickle.dump(content, f)


def load_vars(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


# options:
# rec - video recorder
# read_image - reads a folder of image and process it
if __name__ == "__main__":
    main("read_image")

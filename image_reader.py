import os
import cv2


def image_reader(path_to_images):
    images = os.listdir(path_to_images)
    # preparing all img files into a list
    frame_array = []
    for image in images:
        frame_array.append(cv2.imread(path_to_images + "\\" + image))

    return frame_array


if __name__ == "__main__":
    pass


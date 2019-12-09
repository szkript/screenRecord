import os
import cv2
from tqdm import tqdm


def filename(path, index):
    constructed_filename = path + str(index) + ".jpg"
    return constructed_filename


def image_reader(path_to_images):
    start = 0
    num_of_files = len(os.listdir(path_to_images))
    # preparing all img files into a list
    frame_array = []
    end = num_of_files-start
    for i in tqdm(range(start, end)):
        # reading each files
        # inserting the frames into an image array
        frame_array.append(cv2.imread(filename(path_to_images, i)))

    return frame_array


if __name__ == "__main__":
    pass


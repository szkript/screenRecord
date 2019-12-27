import os
import cv2
import numpy as np
import pyautogui
from config import coordinates
import image_reader as ir
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
"""
Rec screen imgs into video without img save
"""

VAR_BASEPATH = "pyvars"


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
    filter = []
    for x in range(1,6):
        filter.append("card_{}".format(x))
    # load x,y,width,height screen coords from poker table
    coords = coordinates.load_coordinates()
    path = "img\\2"
    output_path = set_path("table_parts")
    # images = ir.image_reader(path)
    # save_vars("img3", images)
    images = load_vars("img3")
    count = 0
    for i, image in enumerate(images):
        for key, coord in coords.items():
            if key in filter:
                x = coords[key]["x"]
                y = coords[key]["y"]
                width = coords[key]["width"]
                height = coords[key]["height"]
                cropped_image = crop_image(image, x, y, width, height)
                cv2.imwrite(output_path + str(count) + ".jpg", cropped_image)
                count += 1
    pass


def images2variable():
    path = "table_parts\\3"
    save_vars("table_parts3", ir.image_reader(path))


def save_vars(filename, content):
    file_path = os.path.join(VAR_BASEPATH, filename)
    with open(file_path, "wb") as f:
        pickle.dump(content, f)
    print("variable saved: {}".format(file_path))


def load_vars(filename):
    file_path = os.path.join(VAR_BASEPATH, filename)
    with open(file_path, "rb") as f:
        print("variable content loaded: {}".format(file_path))
        return pickle.load(f)


def find_duplicates():
    # images = load_vars("table_parts3")
    comparable = ir.image_reader("cards")
    images = ir.image_reader("table_parts\\0")
    for compare in comparable:
        for fi, image in enumerate(images):
            titles = ["actual {0}".format(fi), "compare", "difference"]
            if image.shape == compare.shape:
                difference = cv2.subtract(image, compare)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print("The images are completely Equal {0} - {1}".format(fi-1, fi))
                # visualize
                fig = plt.figure(figsize=(3., 3.))
                grid = ImageGrid(fig, 111,  # similar to subplot(111)
                                 nrows_ncols=(2, 2),  # creates 2x2 grid of axes
                                 axes_pad=0.1,  # pad between axes in inch.
                                 )

                index = 0
                for ax, im in zip(grid, [image, compare, difference]):
                    # Iterating over the grid returns the Axes.
                    ax.imshow(im)
                    ax.set_title(titles[index])
                    index += 1

                plt.show()


def sum_image(img_gray):
    # grayscale image
    sum_of_image = []
    for row in img_gray:
        sum_of_image.append(sum(row))
    return sum_of_image


def main(option):
    if option == "rec":
        video_record()
    if option == "read_image":
        image_extractor()
    if option == "find_duplicate":
        find_duplicates()
    if option == "save_to_var":
        images2variable()


# options:
# rec - video recorder
# read_image - reads a folder of image and process it
# find_duplicate - first step-> compare 2 img and mark as duplicate if is similar
# save_to_var - read folder of images and save the result in a var for be faster to experiment with them in the future
if __name__ == "__main__":
    main("read_image")

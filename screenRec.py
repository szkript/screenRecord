import os
import cv2
import numpy as np
import pyautogui
from config import coordinates

"""
Rec screen imgs into video without img save
"""


# img basic crop tool
def crop_image(image, x, y, w, h):
    return image[y:y + h, x:x + w]


def set_path():
    actual_path = os.getcwd() + "\\img"
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


def main():
    output = "test.avi"
    # load x,y,width,height screen coords from poker table
    coords = coordinates.load_coordinates()
    # get info from pic
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width, channels = image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))
    count = 0
    path = set_path()
    while True:
        try:
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            out.write(image)
            StopIteration(0.5)
            if count % 20 == 0:
                cv2.imwrite(path + str(count) + ".jpg", image)
                print("recording", count, " step")
            count += 1
        except KeyboardInterrupt:   # ctrl+c
            print("stop recording")
            break

    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

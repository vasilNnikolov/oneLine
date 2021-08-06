import os
import numpy as np

from PIL import Image, ImageDraw
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io


class Superpixel:
    def __init__(self, average_color, area, center_of_mass):
        self.average_color = average_color
        self.area = area
        self.center_of_mass = center_of_mass


def cli_superpixel_image_export():
    """
    returns the superpixel transformed image
    :return:
    """
    # get image filename
    filename = input("Enter the filename of the image: ")
    while not os.path.isfile(filename):
        filename = input("Enter a valid filename(the image should be in the directory of the file: ")

    # get number of superpixels
    n_pixels = int(input("Enter the number of superpixels(preferably over 2000): "))
    return make_superpixel_image(filename, n_pixels)

def make_superpixel_image(filename, n_pixels):
    pil_image = Image.open(filename).convert("LA")
    pil_pixels = pil_image.load()
    image = img_as_float(io.imread(filename))
    segment_matrix = slic(image, n_pixels, sigma=15, start_label=1)

    # make new image with averaged color over all the pixels
    shape = segment_matrix.shape
    output_image = Image.new("LA", shape, 0)
    output_pixels = output_image.load()


    superpixels = get_superpixels(segment_matrix, pil_pixels)

    # set output image
    for y in range(shape[0]):
        for x in range(shape[1]):
            output_pixels[x, y] = (superpixels[segment_matrix[y][x]].average_color, 255)

    draw = ImageDraw.Draw(output_image)
    COM_radius = 1
    for s in superpixels.values():
        draw.ellipse((int(s.center_of_mass[0] - COM_radius), int(s.center_of_mass[1] - COM_radius),
                      int(s.center_of_mass[0] + COM_radius), int(s.center_of_mass[1] + COM_radius)),
                     fill="red")

    output_image.show()

def get_superpixels(segment_matrix, pil_pixels):
    """
    returns a dict with keys superpixel index, and values superpixel objects
    :param segmentation_matrix:
    :return:
    """
    n_pixels = np.amax(segment_matrix)
    average_color = {i: 0 for i in range(1, n_pixels + 1)}
    size_of_pixel = {i: 0 for i in range(1, n_pixels + 1)}
    xs = {i: 0 for i in range(1, n_pixels + 1)}
    ys = {i: 0 for i in range(1, n_pixels + 1)}
    center_of_mass = {}
    for y in range(segment_matrix.shape[0]):
        for x in range(segment_matrix.shape[1]):
            size_of_pixel[segment_matrix[y][x]] += 1
            average_color[segment_matrix[y][x]] += pil_pixels[x, y][0]
            xs[segment_matrix[y][x]] += x
            ys[segment_matrix[y][x]] += y

    for superpixel_index in average_color.keys():
        average_color[superpixel_index] = int(average_color[superpixel_index]/size_of_pixel[superpixel_index])
        center_of_mass[superpixel_index] = (xs[superpixel_index]/size_of_pixel[superpixel_index], ys[superpixel_index]/size_of_pixel[superpixel_index])

    superpixels = {i: Superpixel(average_color[i], size_of_pixel[i], center_of_mass[i]) for i in range(1, n_pixels + 1)}
    return superpixels



if __name__ == "__main__":
    make_superpixel_image("cute_qna_vasko_square.jpg", 10000)


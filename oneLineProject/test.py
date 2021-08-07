# import oneLineLibrary as one
#
# from PIL import Image
#
# pixel_sidelength = 40
#
# n_pixels = 100
#
# output_image = Image.new("LA", (pixel_sidelength*n_pixels, pixel_sidelength*n_pixels), 0)
#
# for y in range(n_pixels):
#     for x in range(n_pixels):
#         intensity = (x + y)/(2*n_pixels)
#         image_to_paste = one.make_square_spiral(10*intensity, (pixel_sidelength, )*2, (0, pixel_sidelength/2), (pixel_sidelength, pixel_sidelength/2))
#         output_image.paste(image_to_paste, (x*pixel_sidelength, y*pixel_sidelength))
#     print(y)
#
# output_image.show()
import numpy as np

import oneLineHexagons

from PIL import Image

hexagon_height = 40

n_pixels = 20

w = int(0.9*n_pixels*hexagon_height)
h = w

output_image = Image.new("L", (w, h), 0)

hexagon_matrix = oneLineHexagons.get_hexagon_matrix(hexagon_height)
hexagon_area = np.count_nonzero(hexagon_matrix == 1)

original_image = Image.open("cute_qna_vasko_square.jpg").resize((w, h), resample=Image.BICUBIC)
original_pixels = original_image.load()

centers = oneLineHexagons.get_hexagon_centers(w, h, hexagon_height)

start_point = (0, hexagon_height//2)
end_point = (int(1.4*hexagon_height), hexagon_height)
for center_index, c in enumerate(centers):
    # get intensity of the region in the matrix
    total_intensity = 0
    for x in range(int(c[0] - hexagon_matrix.shape[0]//2), int(c[0] + hexagon_matrix.shape[0]//2)):
        for y in range(int(c[1] - hexagon_matrix.shape[1]//2), int(c[1] + hexagon_matrix.shape[1]//2)):
            matrix_x = int(x - c[0] + hexagon_matrix.shape[0]//2)
            matrix_y = int(y - c[1] + hexagon_matrix.shape[1]//2)
            if 0 <= x < w and 0 <= y < h and hexagon_matrix[matrix_x][matrix_y] == 1:
                total_intensity += original_pixels[x, y][0]

    total_intensity /= hexagon_area

    # set the color of the hexagon to total_intensity
    turns = (255 - total_intensity)/255*15

    image_to_paste = oneLineHexagons.make_hexagon_spiral(turns, (int(1.4*hexagon_height), hexagon_height), start_point, end_point)
    output_image.paste(image_to_paste, (int(c[0] - 0.7*hexagon_height), int(c[1] - hexagon_height//2)))

    if center_index%50 == 0:
        print(center_index)


output_image.show()

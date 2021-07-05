import oneLineLibrary as one

from PIL import Image

pixel_sidelength = 40

n_pixels = 25

output_image = Image.new("LA", (pixel_sidelength*n_pixels, pixel_sidelength*n_pixels), 0)

for y in range(n_pixels):
    for x in range(n_pixels):
        intensity = (x + y)/(2*n_pixels)
        image_to_paste = one.make_square_spiral(10*intensity, (pixel_sidelength, )*2, (0, pixel_sidelength/2), (pixel_sidelength, pixel_sidelength/2))
        output_image.paste(image_to_paste, (x*pixel_sidelength, y*pixel_sidelength))
    print(y)

output_image.show()

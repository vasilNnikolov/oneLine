from PIL import Image, ImageDraw
def make_picture_circular(image):
    w, h = image.size
    output = Image.new("LA", (w, h), 0)
    output_pixels = output.load()

    for y in range(h):
        for x in range(w):
            if (x/w - 0.5)**2 + (y/h - 0.5)**2 <= 0.25:
                output_pixels[x, y] = image.getpixel((x, y))
    return output
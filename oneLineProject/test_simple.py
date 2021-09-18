from PIL import Image
filename = "cute_image_4.jpg"
nPixels = 100
image = Image.open(filename).resize((nPixels, nPixels)).convert("L").resize((500, 500))

image.show()
from PIL import Image, ImageOps

def ImgNegative(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i, j] = (255 - r, 255 - g, 255 - b)
   
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output

def ImgRotate(img_input):
    return img_input.rotate(90, expand=True)
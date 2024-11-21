from PIL import Image

def load_image(image_path)->Image:
    """ Load an image from the specified file path """
    image = Image.open(image_path)
    image.load()
    return image

def color_filter(image:Image , rgb:dict)->Image:
    """ Apply a red filter to the image
        - rgb: dictionary with the percentage to increase the color [ r : [0,100%] , g : [0,100%] , b : [0,100%] ]
    """
    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (r + int(r * rgb["r"]/100), g + int(g * rgb["g"]/100),  r+ int(b * rgb["b"]/100))
    return image

def brightness(image:Image, brightness:float)->Image:
    """ Apply a brightness filter to the image """
    return color_filter(image, {"r":brightness, "g":brightness, "b":brightness})


# \text{Luminance} = 0.299 \times R + 0.587 \times G + 0.114 \times B
def black_and_white(image:Image, use_luminance:bool= True  )->Image:
    """ Apply a black and white filter to the image """
    new_image = Image.new("L", (image.width, image.height))
    new_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            # calculate luminance which is the average of the RGB values
            if ( use_luminance):
                luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            else:
                luminance = int((r + g + b) / 3)
            new_image.putpixel((i, j), luminance)
    return new_image



def save_image(image:Image, save_path:str)->None:
    """ Save an image to the specified file path """
    image.save(save_path)





def main():
    main_image= load_image("example.jpg")
    image = main_image.copy()
    # r1 = color_filter(image, {"r":20, "g":0, "b":0})
    # r2 = brightness(image, 150)
    # r3 = color_filter(image, {"r":0, "g":30, "b":0})
    # save_image(r1, "output.jpg")
    # save_image(r2, "output2.jpg")
    # save_image(r3, "output3.jpg")
    r4 = black_and_white(image)
    save_image(r4, "output4.jpg")
    r5 = black_and_white(image, False)
    save_image(r5, "output5.jpg")


if __name__ == "__main__":
    main()
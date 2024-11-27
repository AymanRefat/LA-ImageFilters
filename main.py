from PIL import Image
# TODO : Implement Blur Filter
# TODO : Implement Sharpen Filter
# TODO : Implement Contrast Filter

def load_image(image_path) -> Image:
    """ Load an image from the specified file path """
    image = Image.open(image_path)
    image.load()
    return image


def color_filter(image: Image, rgb: dict) -> Image:
    """ Apply a red filter to the image
        - rgb: dictionary with the percentage to increase the color [ r : [0,100%] , g : [0,100%] , b : [0,100%] ]
    """

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (r + int(r * rgb["r"] / 100), g + int(g * rgb["g"] / 100), r + int(b * rgb["b"] / 100))
    return image


def brightness(image: Image, brightness: float) -> Image:
    """ Apply a brightness filter to the image """
    if brightness < 0:
        raise ValueError("Brightness must be a positive number")
    return color_filter(image, {"r": brightness, "g": brightness, "b": brightness})


def darkness(image: Image, darkness: float) -> Image:
    """ Apply a darkness filter to the image
        - darkness: percentage to decrease [0,100%]"""
    if 0 <= darkness <= 100:
        raise ValueError("Darkness must be a positive number")
    return color_filter(image, {"r": -darkness, "g": -darkness, "b": -darkness})

# \text{Luminance} = 0.299 \times R + 0.587 \times G + 0.114 \times B
def black_and_white(image: Image, use_luminance: bool = True) -> Image:
    """ Apply a black and white filter to the image """
    new_image = Image.new("L", (image.width, image.height))
    new_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            # calculate luminance which is the average of the RGB values
            if (use_luminance):
                luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            else:
                luminance = int((r + g + b) / 3)
            new_image.putpixel((i, j), luminance)
    return new_image


def save_image(image: Image, save_path: str) -> None:
    """ Save an image to the specified file path """
    image.save(save_path)


def main():
    main_image = load_image("example.jpg")
    image1 = main_image.copy()
    image2 = main_image.copy()
    image3 = main_image.copy()
    image4 = main_image.copy()
    image5 = main_image.copy()
    image6 = main_image.copy()

    r1 = color_filter(image1, {"r":20, "g":0, "b":0})
    save_image(r1, "output.jpg")
    r2 = brightness(image2, 50)
    save_image(r2, "output2.jpg")
    r3 = color_filter(image3, {"r":0, "g":30, "b":0})
    save_image(r3, "output3.jpg")
    r4 = black_and_white(image4)
    save_image(r4, "output4.jpg")
    r5 = black_and_white(image5, False)
    save_image(r5, "output5.jpg")
    r6 = darkness(image6, 10)
    save_image(r6, "output6.jpg")


if __name__ == "__main__":
    main()

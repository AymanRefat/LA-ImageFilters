from PIL import Image
#TODO : fourier filter

sharp_kernal    = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
blur_kernal3by3 = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
blur_kernel5by5 = [
    [ 1/225,  4/225,  6/225,  4/225,  1/225],
    [ 4/225, 16/225, 24/225, 16/225,  4/225],
    [ 6/225, 24/225, 36/225, 24/225,  6/225],
    [ 4/225, 16/225, 24/225, 16/225,  4/225],
    [ 1/225,  4/225,  6/225,  4/225,  1/225]
]


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
    if not ( 0 <= darkness <= 100):
        raise ValueError("Darkness must be a positive number")
    return color_filter(image, {"r": -darkness, "g": -darkness, "b": -darkness})

# \text{Luminance} = 0.299 \times R + 0.587 \times G + 0.114 \times B
def gray(image: Image, use_luminance: bool = True) -> Image:
    """ Convert the image to grayscale
        - use_luminance: if True use the luminance formula, otherwise use the average of the RGB values """
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


def black_and_white(image: Image, threshold: int , use_luminance = True) -> Image:
    """ Convert the image to black and white
        - threshold: value to determine if the pixel is black or white """
    # Convert the image to grayscale
    if not (0 <= threshold <= 256):
        raise ValueError("Threshold must be between 0 and 256")

    new_image = Image.new("L", (image.width, image.height))
    new_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            if use_luminance :
                luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            else :
                luminance = (r + g + b) // 3
            if luminance > threshold:
                new_image.putpixel((i, j), 255)
            else:
                new_image.putpixel((i, j), 0)
    return new_image

#TODO : use np and give the ability to change the degree of the blur
def convolution(image: Image, kernel: list) -> Image:
    """ Apply a convolution filter to the image
        - kernel: 2D list with the kernel values."""
    new_image = Image.new("RGB", (image.width, image.height))
    new_image.load()
    pixels = image.load()
    radius = len(kernel)//2
    # start from second pixel and end at the second last pixel
    for i in range(radius ,  image.width-radius):
        for j in range(radius , image.height-radius):
            new_pixel = [0, 0, 0]
            for x in range(-radius, radius+1 ):
                for y in range(-radius, radius+1):
                        r, g, b = pixels[i + x, j + y]
                        new_pixel[0] += r * kernel[x + 1][y + 1]
                        new_pixel[1] += g * kernel[x + 1][y + 1]
                        new_pixel[2] += b * kernel[x + 1][y + 1]

            new_image.putpixel((i, j), (int(new_pixel[0]), int(new_pixel[1]), int(new_pixel[2])))
    return new_image




def main():
    main_image = load_image("example.jpg")
    image1 = main_image.copy()
    image2 = main_image.copy()
    image3 = main_image.copy()
    image4 = main_image.copy()
    image5 = main_image.copy()
    image6 = main_image.copy()
    image7 = main_image.copy()
    image8 = main_image.copy()
    image9 = main_image.copy()

    r1 = color_filter(image1, {"r":20, "g":0, "b":0})
    save_image(r1, "output.jpg")
    print("Image 1 saved")
    r2 = brightness(image2, 50)
    save_image(r2, "output2.jpg")
    print("Image 2 saved")
    r3 = color_filter(image3, {"r":0, "g":30, "b":0})
    save_image(r3, "output3.jpg")
    print("Image 3 saved")
    r4 = gray(image4)
    save_image(r4, "output4.jpg")
    print( "Image 4 saved")
    r5 = gray(image5, False)
    save_image(r5, "output5.jpg")
    print( "Image 5 saved")
    r6 = darkness(image6, 50)
    save_image(r6, "output6.jpg")
    print( "Image 6 saved")

    r7 = black_and_white(image7, 128)
    save_image(r7, "output7.jpg")
    print( "Image 7 saved")

    r8 = convolution(image8, sharp_kernal)
    save_image(r8, "output8.jpg")
    print( "Image 8 saved")

    r9 = convolution(image9, blur_kernel5by5)
    save_image(r9, "output9.jpg")
    print( "Image 9 saved")





if __name__ == "__main__":
    main()

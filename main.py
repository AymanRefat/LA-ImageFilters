from PIL import Image
import numpy as np
sharp_kernal = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
blur_kernel101by101 = np.ones((101, 101)) / 101**2

def load_image(image_path) -> Image:
    """ Load an image from the specified file path """
    image = Image.open(image_path)
    image.load()
    return image

def color_filter(image: Image, rgb: dict) -> Image:
    """
    Apply a color filter to the image.
    - rgb: dictionary with percentages to adjust the colors (r, g, b).
    - r: percentage to adjust the red channel.
    - g: percentage to adjust the green channel.
    - b: percentage to adjust the blue channel
    """
    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]  # Get the current pixel values
            # Adjust the pixel values by the specified percentage
            pixels[i, j] = (
                r + int(r * rgb["r"] / 100),
                g + int(g * rgb["g"] / 100),
                b + int(b * rgb["b"] / 100)
            )
    return image  # Return the modified image

def brightness(image: Image, brightness: float , use_lumiance:bool = True) -> Image:
    """
    Apply a brightness filter to the image.
    - brightness: positive percentage to increase brightness.
    - use_lumiance: if True, use luminance formula; otherwise, apply the same increase to all channels.
    """
    if brightness < 0:
        raise ValueError("Brightness must be a positive number")

    if ( use_lumiance) :
        # Use the luminance formula to calculate the brightness
        return color_filter(image, {"r": brightness*.299, "g": brightness*.587, "b": brightness*.114})

    # Use the color filter function to apply the same increase to all channels
    return color_filter(image, {"r": brightness, "g": brightness, "b": brightness})

def darkness(image: Image, darkness: float , use_lumiance: bool = True) -> Image:
    """
    Apply a darkness filter to the image.
    - darkness: percentage to decrease brightness in each channel.
    - use_lumiance: if True, use luminance formula; otherwise, apply the same decrease to all channels.
    """
    if not (0 <= darkness <= 100):
        raise ValueError("Darkness must be between 0 and 100")

    if (use_lumiance) :
        # Use the luminance formula to calculate the darkness
        return color_filter(image, {"r": -darkness*.299, "g": -darkness*.587, "b": -darkness*.114})
    # Use a negative percentage to reduce brightness in all channels
    return color_filter(image, {"r": -darkness, "g": -darkness, "b": -darkness})

def gray(image: Image, use_luminance: bool = True) -> Image:
    """
    Convert the image to grayscale.
    - use_luminance: if True, use luminance formula; otherwise, use the RGB average.
    """
    # Create a new grayscale image
    new_image = Image.new("L", (image.width, image.height))
    new_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            # Calculate luminance or average based on the parameter
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b) if use_luminance else int((r + g + b) / 3)
            new_image.putpixel((i, j), luminance)  # Set the grayscale value
    return new_image  # Return the grayscale image

def save_image(image: Image, save_path: str) -> None:
    """ Save the image to the specified file path """
    image.save(save_path)

def black_and_white(image: Image, threshold: int, use_luminance=True) -> Image:
    """
    Convert the image to black and white.
    - threshold: Value to determine the cutoff between black and white.
    """
    if not (0 <= threshold <= 256):
        raise ValueError("Threshold must be between 0 and 256")
    # Convert the image to grayscale first
    new_image = Image.new("L", (image.width, image.height))
    new_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            # Calculate luminance or average based on the parameter
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b) if use_luminance else (r + g + b) // 3
            # Compare with threshold and set pixel to either black or white
            new_image.putpixel((i, j), 255 if luminance > threshold else 0)
    return new_image

def convolution(image: Image, kernel: list) -> Image:
    """
    Apply a convolution filter to the image.
    - kernel: 2D list representing the convolution kernel.
    """
    new_image = Image.new("RGB", (image.width, image.height))  # Create an output image
    new_image.load()
    radius = len(kernel) // 2
    # Pad the image
    padded_image = Image.new("RGB", (image.width + 2 * radius, image.height + 2 * radius))
    padded_image.paste(image, (radius, radius))
    pixels = padded_image.load()
    # Iterate through each pixel, avoiding the borders
    for i in range(radius, image.width + radius):
        for j in range(radius, image.height + radius):
            new_pixel = [0, 0, 0]
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    r, g, b = pixels[i + x, j + y]  # Get the neighboring pixel values
                    # Multiply each channel by the corresponding kernel value
                    weight = kernel[x + radius][y + radius]
                    new_pixel[0] += r * weight
                    new_pixel[1] += g * weight
                    new_pixel[2] += b * weight
            new_image.putpixel((i-radius, j-radius), tuple(map(int, new_pixel)))
    return new_image  # Return the modified image

def faster_convolution(image: Image, kernel: list) -> Image:
        """
        Apply a convolution filter to the image using NumPy for speed.
        - kernel: 2D list representing the convolution kernel.
        """
        # Convert the image and kernel to NumPy arrays
        kernel = np.array(kernel)
        image_array = np.array(image)

        # Extract the dimensions of the image and kernel
        kernel_size = kernel.shape[0]
        radius = kernel_size // 2
        height, width, channels = image_array.shape

        # Pad the image to handle border pixels during convolution
        padded_image = np.pad(image_array, ((radius, radius), (radius, radius), (0, 0)), mode='edge')

        # Create an empty array for the output image
        output_array = np.zeros_like(image_array)

        # Perform convolution using nested loops and NumPy operations
        for i in range(height):
            for j in range(width):
                # Extract the region of interest (ROI) from the padded image
                roi = padded_image[i:i + kernel_size, j:j + kernel_size]
                # Apply the kernel to each channel (R, G, B)
                for c in range(channels):
                    output_array[i, j, c] = np.sum(roi[:, :, c] * kernel)

        # Clip the values to stay in the valid range [0, 255]
        output_array = np.clip(output_array, 0, 255).astype(np.uint8)

        # Convert the result back to a PIL image
        return Image.fromarray(output_array)

def main():
    """ Main function to demonstrate the image processing operations """
    main_image = load_image("example.jpg")  # Load the input image
    # Create copies of the main image for different operations
    image1, image2, image3, image4, image5, image6, image7, image8, image9 , image10 , image11 = [main_image.copy() for _ in range(11)]

    # Apply color filter (increase red channel by 20%)
    save_image(color_filter(image1, {"r": 20, "g": 0, "b": 0}), "output.jpg")
    print("Image 1 saved")

    # Apply brightness filter (increase brightness by 50%)
    save_image(brightness(image2, 50), "output2.jpg")
    print("Image 2 saved")

    #apply brightness filter + luminance
    save_image(brightness(image10, 50, True), "output2_luminance.jpg")
    print("Image 2 saved with luminance")

    # Apply color filter (increase green channel by 30%)
    save_image(color_filter(image3, {"r": 0, "g": 30, "b": 0}), "output3.jpg")
    print("Image 3 saved")

    # Convert image to grayscale using luminance formula
    save_image(gray(image4), "output4.jpg")
    print("Image 4 saved")

    # Convert image to grayscale using average formula
    save_image(gray(image5, False), "output5.jpg")
    print("Image 5 saved")

    # Apply darkness filter (reduce brightness by 50%)
    save_image(darkness(image6, 50), "output6.jpg")
    print("Image 6 saved")

    # Apply darkness filter + luminance
    save_image(darkness(image11, 50, True), "output6_luminance.jpg")
    print("Image 6 saved with luminance")

    # Convert image to black and white with threshold of 128
    save_image(black_and_white(image7, 128), "output7.jpg")
    print("Image 7 saved")

    # Apply sharpening filter using convolution
    save_image(convolution(image8, sharp_kernal), "output8.jpg")
    print("Image 8 saved")

    # Apply 101x101 blur filter using convolution
    save_image(faster_convolution(image9, blur_kernel101by101), "output9.jpg")
    print("Image 9 saved")

if __name__ == "__main__":
    main()
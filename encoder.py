from PIL import Image

def encode_image(input_image_path, secret_message, output_image_path):
    """Encode a secret message into an image using simple LSB."""
    image = Image.open(input_image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message += '1111111111111110'  # EOF marker

    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    pixels = list(image.getdata())
    new_pixels = []

    message_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            g = (g & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            b = (b & ~1) | int(binary_message[message_index])
            message_index += 1
        new_pixels.append((r, g, b))
    
    image.putdata(new_pixels)
    image.save(output_image_path)
    return output_image_path
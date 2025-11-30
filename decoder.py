from PIL import Image

def decode_image(encoded_image_path):
    """Decode secret message from image using LSB."""
    image = Image.open(encoded_image_path)
    binary_message = ''
    for pixel in image.getdata():
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111111':  # EOF marker
            break
        message += chr(int(byte, 2))
    return message
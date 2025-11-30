from PIL import Image

def check_image(image_path):
    """Check if image can be opened."""
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except Exception:
        return False
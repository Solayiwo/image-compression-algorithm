from PIL import Image # type: ignore
import os


def compress_image(image, compression_type):
    img_path = image.path
    with Image.open(img_path) as img:
        if compression_type == "lossy":
            compressed_img_path = f"{os.path.splitext(img_path)[0]}_lossy.jpg"
            img.save(compressed_img_path, "JPEG", quality=70)
        else:
            compressed_img_path = f"{os.path.splitext(img_path)[0]}_lossless.png"
            img.save(compressed_img_path, "PNG", optimizer=True)
    
    return compressed_img_path
from PIL import Image # type: ignore
import io


def compress_image(image, compression_type):
    img = Image.open(image)

    compressed_io = io.BytesIO()

    if compression_type == "lossy":
        #img = img.convert('RGB')
        img.save(compressed_io, "JPEG", quality=70)
    else:
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        img.save(compressed_io, "PNG", optimize=True)
        
    compressed_io.seek(0)
    return compressed_io
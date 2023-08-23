from PIL import Image, ImageOps
import base64
from io import BytesIO
def process_img(img):
    # decoding
    bilde = BytesIO(base64.b64decode(img[22:]))

    bilde = Image.open(bilde)
    bilde = ImageOps.grayscale(bilde)
    
    # encoding
    buffered = BytesIO()
    bilde.save(buffered, format="JPEG")
    new_img = str(base64.b64encode(buffered.getvalue()))[2:-1]
    return "data:image/jpeg;base64," + new_img
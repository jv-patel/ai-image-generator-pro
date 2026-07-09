from io import BytesIO
from zipfile import ZipFile
from PIL import Image


def image_to_bytes(image: Image.Image):
    """
    Convert PIL Image to PNG bytes.
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def create_zip(images):
    """
    Create ZIP file from a list of PIL Images.
    Returns ZIP bytes.
    """
    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as zip_file:
        for index, image in enumerate(images, start=1):
            img_buffer = BytesIO()
            image.save(img_buffer, format="PNG")

            zip_file.writestr(
                f"ai_image_{index}.png",
                img_buffer.getvalue()
            )

    zip_buffer.seek(0)
    return zip_buffer.getvalue()

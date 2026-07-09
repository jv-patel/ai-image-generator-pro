from io import BytesIO
from zipfile import ZipFile


def image_to_bytes(image):
    """
    Convert PIL Image to PNG bytes.
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def create_zip(images):
    """
    Create a ZIP file containing all generated images.
    """
    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as zip_file:

        for index, image in enumerate(images, start=1):

            image_buffer = BytesIO()
            image.save(image_buffer, format="PNG")

            zip_file.writestr(
                f"ai_image_{index}.png",
                image_buffer.getvalue(),
            )

    zip_buffer.seek(0)
    return zip_buffer.getvalue()

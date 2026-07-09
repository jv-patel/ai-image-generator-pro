import requests
from io import BytesIO
from PIL import Image


API_URL = "https://text-to-img.apis-bj-devs.workers.dev/"


class AIImageGenerator:

    def __init__(self):
        self.session = requests.Session()

    def generate_images(self, prompt):
        """
        Generate AI images from a text prompt.
        Returns a list of PIL Images.
        """

        response = self.session.get(
            API_URL,
            params={"prompt": prompt},
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            raise Exception("Image generation failed.")

        result = data.get("result", [])

        image_urls = []

        if result:

            if isinstance(result[0], str):
                image_urls = result

            elif isinstance(result[0], dict):

                for item in result:
                    if "url" in item:
                        image_urls.append(item["url"])

        if not image_urls:
            raise Exception("No images received from API.")

        images = []

        for url in image_urls:

            img = self.session.get(url, timeout=60)

            img.raise_for_status()

            image = Image.open(BytesIO(img.content))

            images.append(image)

        return images

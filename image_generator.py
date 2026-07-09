import requests
from io import BytesIO
from PIL import Image


class AIImageGenerator:
    """
    AI Image Generator Backend
    """

    API_URL = "https://text-to-img.apis-bj-devs.workers.dev/"

    def __init__(self):
        self.session = requests.Session()

    def generate(
        self,
        prompt: str,
        style: str = "Default",
        image_count: int = 4,
        aspect_ratio: str = "1:1",
    ):
        """
        Generate AI images.
        Returns a list of PIL Image objects.
        """

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        final_prompt = prompt.strip()

        if style != "Default":
            final_prompt = f"{prompt}, {style} style"

        response = self.session.get(
            self.API_URL,
            params={"prompt": final_prompt},
            timeout=90,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            raise Exception("Image generation failed.")

        result = data.get("result", [])

        urls = []

        if result:

            if isinstance(result[0], str):
                urls = result

            elif isinstance(result[0], dict):
                urls = [
                    item["url"]
                    for item in result
                    if "url" in item
                ]

        if not urls:
            raise Exception("No images received.")

        images = []

        for url in urls[:image_count]:

            img = self.session.get(url, timeout=60)

            img.raise_for_status()

            image = Image.open(
                BytesIO(img.content)
            )

            images.append(image)

        return images

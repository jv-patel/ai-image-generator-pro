import requests
from io import BytesIO
from PIL import Image


class AIImageGenerator:

    API_URL = "https://text-to-img.apis-bj-devs.workers.dev/"

    def __init__(self):
        self.session = requests.Session()

    def generate(
        self,
        prompt,
        style="Default",
        image_count=1,
    ):
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        final_prompt = prompt

        if style != "Default":
            final_prompt += f", {style} style"

        response = self.session.get(
            self.API_URL,
            params={"prompt": final_prompt},
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            raise Exception("Failed to generate image.")

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
            raise Exception("No images returned by the API.")

        images = []

        for url in urls[:image_count]:

            img = self.session.get(url, timeout=60)
            img.raise_for_status()

            images.append(
                Image.open(BytesIO(img.content))
            )

        return images

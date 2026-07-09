import requests
from io import BytesIO
from PIL import Image


class AIImageGenerator:
    """
    AI Image Generator Backend V2
    """

    CURRENT_API = "https://text-to-img.apis-bj-devs.workers.dev/"

    def __init__(self):
        self.session = requests.Session()
        self.timeout = 90

    def _download_image(self, url):
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))

    def _generate_current_api(self, prompt):
        response = self.session.get(
            self.CURRENT_API,
            params={"prompt": prompt},
            timeout=self.timeout,
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

        return urls

    def generate(
        self,
        prompt,
        style="Default",
        image_count=4,
        aspect_ratio="1:1",
        provider="Current API",
    ):

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        final_prompt = prompt.strip()

        if style != "Default":
            final_prompt += f", {style} style"

        # Future-ready
        if aspect_ratio != "1:1":
            final_prompt += f", aspect ratio {aspect_ratio}"

        if provider == "Current API":
            urls = self._generate_current_api(final_prompt)
        else:
            raise Exception("Provider not supported yet.")

        if not urls:
            raise Exception("No images received.")

        images = []

        for url in urls[:image_count]:
            images.append(self._download_image(url))

        return images

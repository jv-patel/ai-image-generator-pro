import streamlit as st
from image_generator import AIImageGenerator
from utils import image_to_bytes, create_zip

st.set_page_config(
    page_title="AI Image Generator Pro",
    page_icon="🎨",
    layout="wide",
)

st.markdown("""
<style>

.stApp{
background:#0f172a;
}

.main-title{
text-align:center;
font-size:50px;
font-weight:bold;
color:white;
}

.subtitle{
text-align:center;
color:#cbd5e1;
margin-bottom:25px;
}

div.stButton > button{
width:100%;
height:52px;
border-radius:12px;
font-size:18px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"<h1 class='main-title'>🎨 AI Image Generator Pro</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p class='subtitle'>Generate beautiful AI images using text prompts.</p>",
unsafe_allow_html=True
)

with st.sidebar:

    st.header("⚙️ Settings")

    style = st.selectbox(
        "Style",
        [
            "Default",
            "Realistic",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Cyberpunk"
        ]
    )

    image_count = st.selectbox(
        "Number of Images",
        [1,2,4]
    )

generator = AIImageGenerator()

prompt = st.text_area(
    "Enter Prompt",
    placeholder="Example: A futuristic city at sunset..."
)

if st.button("✨ Generate Images"):

    if not prompt.strip():

        st.warning("Please enter a prompt.")

    else:

        try:

            with st.spinner("Generating Images..."):

                images = generator.generate(
                    prompt=prompt,
                    style=style,
                    image_count=image_count
                )

            st.success("Images generated successfully!")

            cols = st.columns(2)

            for i, image in enumerate(images):

                with cols[i % 2]:

                    st.image(
                        image,
                        use_container_width=True
                    )

                    st.download_button(
                        label=f"📥 Download Image {i+1}",
                        data=image_to_bytes(image),
                        file_name=f"ai_image_{i+1}.png",
                        mime="image/png",
                        use_container_width=True
                    )

            st.divider()

            st.download_button(
                "📦 Download All Images (ZIP)",
                data=create_zip(images),
                file_name="ai_images.zip",
                mime="application/zip",
                use_container_width=True
            )

        except Exception as e:

            st.error(str(e))

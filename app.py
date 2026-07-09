import streamlit as st
from image_generator import AIImageGenerator
from utils import image_to_bytes, create_zip

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="AI Image Generator Pro",
    page_icon="🎨",
    layout="wide"
)

# ---------------------------------
# Custom CSS
# ---------------------------------
st.markdown("""
<style>

.stApp{
    background-color:#0f172a;
}

.main-title{
    text-align:center;
    color:white;
    font-size:48px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}

div.stButton > button{
    width:100%;
    height:52px;
    border-radius:10px;
    font-weight:bold;
    font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Header
# ---------------------------------
st.markdown(
    "<h1 class='main-title'>🎨 AI Image Generator Pro</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Generate AI Images from your text prompts.</p>",
    unsafe_allow_html=True
)

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    style = st.selectbox(
        "Art Style",
        [
            "Default",
            "Realistic",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Cyberpunk",
            "Pixel Art"
        ]
    )

    image_count = st.selectbox(
        "Number of Images",
        [1, 2, 4]
    )

    st.info(
        "💡 Use detailed prompts for better quality."
    )

# ---------------------------------
# Backend
# ---------------------------------
generator = AIImageGenerator()

prompt = st.text_area(
    "Enter Prompt",
    height=160,
    placeholder="Example: A futuristic cyberpunk city at sunset, ultra realistic, 8K"
)

generate = st.button(
    "✨ Generate Images",
    use_container_width=True
    
)
# ---------------------------------
# Generate Images
# ---------------------------------
if generate:

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")

    else:

        try:

            with st.spinner("🎨 Generating images... Please wait..."):

                images = generator.generate(
                    prompt=prompt,
                    style=style,
                    image_count=image_count,
                )

            st.success(f"✅ Successfully generated {len(images)} image(s)!")

            st.divider()

            st.subheader("🖼️ Generated Images")

            columns = st.columns(2)

            for index, image in enumerate(images):

                with columns[index % 2]:

                    st.image(
                        image,
                        use_container_width=True
                    )

                    st.download_button(
                        label=f"📥 Download Image {index + 1}",
                        data=image_to_bytes(image),
                        file_name=f"ai_image_{index + 1}.png",
                        mime="image/png",
                        use_container_width=True,
                    )

            st.divider()

            zip_file = create_zip(images)

            st.download_button(
                label="📦 Download All Images (ZIP)",
                data=zip_file,
                file_name="ai_images.zip",
                mime="application/zip",
                use_container_width=True,
            )

        except Exception as e:

            st.error(f"❌ {str(e)}")

# ---------------------------------
# Footer
# ---------------------------------
st.divider()

st.caption("🎨 AI Image Generator Pro")
st.caption("Built with ❤️ using Python + Streamlit")

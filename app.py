import streamlit as st
from image_generator import AIImageGenerator
from utils import image_to_bytes, create_zip

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Image Generator Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    text-align:center;
    font-size:54px;
    font-weight:700;
    color:white;
    margin-bottom:0px;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}

div.stButton > button{
    width:100%;
    height:55px;
    border-radius:14px;
    font-size:18px;
    font-weight:bold;
}

textarea{
    border-radius:12px !important;
}

hr{
    margin-top:30px;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Logo
# -----------------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown(
        "<h1 class='main-title'>🎨 AI Image Generator Pro</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Generate stunning AI images from text prompts.</p>",
        unsafe_allow_html=True
    )

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("⚙️ Settings")

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
        [1,2,4]
    )

    st.divider()

    st.info(
        "💡 Tip:\n\n"
        "Use detailed prompts for better results."
    )

# -----------------------------
# Backend
# -----------------------------
generator = AIImageGenerator()

prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example:\nA futuristic cyberpunk city at sunset, ultra realistic, 8K",
    height=160
)

generate = st.button(
    "✨ Generate Images",
    use_container_width=True
    # -----------------------------
# Generate Images
# -----------------------------
if generate:

    if not prompt.strip():

        st.warning("⚠️ Please enter a prompt.")

    else:

        try:

            with st.spinner("🎨 Generating AI images..."):

                images = generator.generate(
                    prompt=prompt,
                    style=style,
                    image_count=image_count,
                )

            st.success(f"✅ Successfully generated {len(images)} image(s)!")

            st.divider()

            st.subheader("🖼️ Generated Images")

            cols = st.columns(2)

            for index, image in enumerate(images):

                with cols[index % 2]:

                    st.image(
                        image,
                        use_container_width=True
                    )

                    st.download_button(
                        label=f"📥 Download Image {index+1}",
                        data=image_to_bytes(image),
                        file_name=f"ai_image_{index+1}.png",
                        mime="image/png",
                        use_container_width=True,
                    )

            st.divider()

            st.download_button(
                label="📦 Download All Images (ZIP)",
                data=create_zip(images),
                file_name="ai_images.zip",
                mime="application/zip",
                use_container_width=True,
            )

        except Exception as e:

            st.error(f"❌ Error: {e}")

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.markdown(
    """
    <div style="text-align:center;color:gray;padding:20px;">
        <h4>🎨 AI Image Generator Pro</h4>
        <p>Built with ❤️ using Python & Streamlit</p>
        <p>© 2026 Jeel Patel</p>
    </div>
    """,
    unsafe_allow_html=True,
    )
)

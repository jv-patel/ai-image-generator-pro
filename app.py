import streamlit as st
from image_generator import AIImageGenerator

st.set_page_config(
    page_title="AI Image Generator Pro",
    page_icon="🎨",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.stApp{
    background:#0f172a;
}

.title{
    text-align:center;
    color:white;
    font-size:45px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}

div.stButton > button{
    width:100%;
    border-radius:10px;
    height:50px;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>🎨 AI Image Generator Pro</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Generate beautiful AI images from your imagination.</div>",
    unsafe_allow_html=True
)

generator = AIImageGenerator()

prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example: A futuristic cyberpunk city at sunset..."
)

generate = st.button("✨ Generate Images")

if generate:

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:

        try:

            with st.spinner("🎨 Generating AI Images..."):

                images = generator.generate_images(prompt)

            st.success(f"✅ Generated {len(images)} image(s)!")

            cols = st.columns(2)

            for index, image in enumerate(images):

                with cols[index % 2]:

                    st.image(
                        image,
                        use_container_width=True
                    )

                    from io import BytesIO

                    buffer = BytesIO()

                    image.save(buffer, format="PNG")

                    st.download_button(
                        label=f"📥 Download Image {index+1}",
                        data=buffer.getvalue(),
                        file_name=f"ai_image_{index+1}.png",
                        mime="image/png",
                        use_container_width=True,
                    )

        except Exception as e:

            st.error(f"❌ {e}")

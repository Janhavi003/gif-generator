import streamlit as st
import tempfile
from gif_utils import images_to_gif, video_to_gif

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="GIF Generator",
    layout="centered",
)

# ================= CLEAN CSS =================
st.markdown(
    """
    <style>
    .main { padding-top: 2rem; }

    .title {
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 2.5rem;
    }

    .step {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .hint {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 0.6rem;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= HEADER =================
st.markdown('<div class="title"> GIF Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Convert images or videos into optimized GIFs using Python</div>',
    unsafe_allow_html=True,
)

# ================= MODE =================
mode = st.radio(
    "Conversion Mode",
    ["🖼️ Images → GIF", "🎬 Video → GIF"],
    horizontal=True,
)

st.divider()

# =================================================
# ================= IMAGE → GIF ===================
# =================================================
if mode == "🖼️ Images → GIF":

    st.markdown('<div class="step">Step 1 · Upload Images</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Large images are automatically resized for optimal GIF size</div>',
        unsafe_allow_html=True,
    )

    uploaded_images = st.file_uploader(
        "Upload images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    # Image preview grid
    if uploaded_images:
        cols = st.columns(3)
        for i, img in enumerate(uploaded_images):
            with cols[i % 3]:
                st.image(img, width="stretch")

    st.divider()

    st.markdown('<div class="step">Step 2 · GIF Settings</div>', unsafe_allow_html=True)
    duration = st.slider(
        "Frame duration (milliseconds)",
        100, 1000, 300, step=100
    )

    generate = st.button("✨ Generate GIF", use_container_width=True)

    # RESULT
    if generate and uploaded_images:
        with st.spinner("Generating optimized GIF..."):
            gif_path = images_to_gif(uploaded_images, duration)

        st.divider()
        st.markdown('<div class="step">Result</div>', unsafe_allow_html=True)

        st.image(gif_path, width="stretch")

        with open(gif_path, "rb") as f:
            st.download_button(
                "⬇️ Download GIF",
                f,
                file_name="images.gif",
                mime="image/gif",
                use_container_width=True,
            )

    elif generate:
        st.warning("Please upload at least one image.")

# =================================================
# ================= VIDEO → GIF ===================
# =================================================
else:
    st.markdown('<div class="step">Step 1 · Upload Video</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Supported formats: MP4, MOV, AVI</div>',
        unsafe_allow_html=True,
    )

    video_file = st.file_uploader(
        "Upload video",
        type=["mp4", "mov", "avi"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown('<div class="step">Step 2 · GIF Settings</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        fps = st.slider("FPS", 5, 20, 10)
    with col2:
        width = st.slider("Width (px)", 200, 800, 480)
    with col3:
        max_duration = st.slider("Max duration (sec)", 1, 10, 5)

    convert = st.button("🎬 Convert to GIF", use_container_width=True)

    # RESULT
    if convert and video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        with st.spinner("Converting & optimizing GIF..."):
            gif_path = video_to_gif(
                video_path,
                fps=fps,
                resize_width=width,
                max_duration=max_duration,
            )

        st.divider()
        st.markdown('<div class="step">Result · Video vs GIF</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.video(video_file)
        with col2:
            st.image(gif_path, width="stretch")

        with open(gif_path, "rb") as f:
            st.download_button(
                "⬇️ Download GIF",
                f,
                file_name="video.gif",
                mime="image/gif",
                use_container_width=True,
            )

    elif convert:
        st.warning("Please upload a video.")

# ================= FOOTER =================
st.markdown(
    '<div class="footer">Built with Python · Streamlit · Pillow · MoviePy</div>',
    unsafe_allow_html=True,
)

from PIL import Image

# ---------------- MOVIEPY COMPATIBILITY ----------------
try:
    # MoviePy 2.x
    from moviepy import VideoFileClip
except ImportError:
    # MoviePy 1.x (Streamlit Cloud often installs this)
    from moviepy.editor import VideoFileClip


# ---------------- IMAGE → GIF ----------------
def images_to_gif(
    uploaded_images,
    duration=300,
    output_path="images.gif",
    max_width=500
):
    frames = []

    for image in uploaded_images:
        img = Image.open(image).convert("RGB")

        # Auto resize large images
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        frames.append(img)

    if not frames:
        raise ValueError("No images provided")

    # Single image → duplicate for looping GIF
    if len(frames) == 1:
        frames = frames * 2

    # Ensure same frame size
    base_size = frames[0].size
    frames = [img.resize(base_size, Image.LANCZOS) for img in frames]

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True
    )

    return output_path


# ---------------- VIDEO → GIF ----------------
def video_to_gif(
    video_path,
    output_path="video.gif",
    fps=10,
    resize_width=480,
    max_duration=5
):
    clip = VideoFileClip(video_path)

    # Trim video (MoviePy 2.x & 1.x compatible)
    try:
        clip = clip[:max_duration]
    except TypeError:
        clip = clip.subclip(0, max_duration)

    # Resize video
    try:
        clip = clip.resized(width=resize_width)  # MoviePy 2.x
    except AttributeError:
        clip = clip.resize(width=resize_width)   # MoviePy 1.x

    clip.write_gif(output_path, fps=fps)
    clip.close()

    return output_path

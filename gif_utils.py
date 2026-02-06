from PIL import Image
from moviepy import VideoFileClip


def images_to_gif(uploaded_images, duration=300, output_path="images.gif", max_width=500):
    frames = []
    for image in uploaded_images:
        img = Image.open(image).convert("RGB")
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        frames.append(img)
    if not frames:
        raise ValueError("No images provided")
    if len(frames) == 1:
        frames = frames * 2
    base_size = frames[0].size
    frames = [img.resize(base_size, Image.LANCZOS) for img in frames]
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)
    return output_path


def video_to_gif(video_path, output_path="video.gif", fps=10, resize_width=480, max_duration=5):
    clip = VideoFileClip(video_path)
    if clip.duration > max_duration:
        clip = clip[:max_duration]
    if resize_width:
        clip = clip.resized(width=resize_width)
    clip.write_gif(output_path, fps=fps)
    clip.close()
    return output_path

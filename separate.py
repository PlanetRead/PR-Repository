from moviepy.video.io.VideoFileClip import VideoFileClip

def split_video(video_path, chunk_length=60):
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    
    for i in range(0, duration, chunk_length):
        start_time = i
        end_time = min(i + chunk_length, duration)
        chunk = video.subclip(start_time, end_time)
        chunk_name = f"{video_path.split('.')[0]}_chunk_{i//chunk_length + 1}.mp4"
        chunk.write_videofile(chunk_name, codec="libx264")
        
    video.close()

# Example usage:
video_path = "C:/Users/user/Desktop/separating audio/Sito Marjaani-Part 10 - 5 Min .mp4"
split_video(video_path)

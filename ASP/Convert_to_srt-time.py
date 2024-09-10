def convert_to_srt_time(time_seconds):
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    milliseconds = int((time_seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Example usage:
time_seconds = 123.456
srt_time = convert_to_srt_time(time_seconds)
print(srt_time)

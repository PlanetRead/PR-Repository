def trim_audio(input_file_path, output_file_path, start_time, end_time):
    # Load the video file
    audio = AudioSegment.from_wav(input_file_path)
    # Trim the video
    trimmed_audio = audio[start_time * 1000:end_time * 1000]
    # Save the trimmed video
    trimmed_audio.export(output_file_path, format="wav")

# Example usage:
input_file_path = 'input.wav'
output_file_path = 'trimmed_output.wav'
start_time = 10  # in seconds
end_time = 20    # in seconds
trim_audio(input_file_path, output_file_path, start_time, end_time)

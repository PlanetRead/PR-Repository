def mp3_to_wav(mp3, wav):
    audio = AudioSegment.from_mp3(mp3)
    audio.export(wav, format="wav")

# Example usage:
mp3_file_path = 'input.mp3'
wav_file_path = 'output.wav'
mp3_to_wav(mp3_file_path, wav_file_path)

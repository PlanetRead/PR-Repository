def write_new_srt(sentence_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, (start_time, end_time, sentence) in enumerate(sentence_data, start=1):
            file.write(f"{index}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{sentence}\n\n")

# Example usage:
sentence_data = [('00:00:00,000', '00:00:05,000', 'Hello World')]
output_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
write_new_srt(sentence_data, output_file_path)

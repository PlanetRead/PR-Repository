def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', re.DOTALL)
    matches = pattern.findall(content)
    words_data = []
    for match in matches:
        index, start_time, end_time, word = match
        words_data.append((start_time, end_time, word.strip()))
    return words_data

# Example usage:
srt_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
words_data = parse_srt(srt_file_path)

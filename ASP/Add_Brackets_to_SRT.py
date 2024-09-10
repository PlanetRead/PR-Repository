def add_brackets_to_srt(srt_path, bracket_lines):
    subs = pysrt.open(srt_path, encoding='utf-8')
    for line_number in bracket_lines:
        if line_number - 1 < len(subs):
            subs[line_number - 1].text = f"[{subs[line_number - 1].text}]"
    subs.save(srt_path, encoding='utf-8')

# Example usage:
srt_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
bracket_lines = [2, 4]
add_brackets_to_srt(srt_file_path, bracket_lines)

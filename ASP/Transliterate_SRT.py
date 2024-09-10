def transliterate_srt(input_file, output_file, source_script, target_script='ITRANS'):
    with open(input_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    subtitle_pattern = re.compile(r'(\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n)(.+?)(?=\n\n|\Z)', re.DOTALL)

    transliterated_content = ''
    
    for match in subtitle_pattern.finditer(srt_content):
        header = match.group(1)
        text = match.group(2)
        
        transliterated_lines = []
        for line in text.split('\n'):
            transliterated_line = transliterate.process(source_script, target_script, line)
            fin=''
            for i in transliterated_line:
                if i == '.' or i=='^' or i=='~':
                    continue
                else:
                    fin+=i
            transliterated_line = fin.lower()
            transliterated_lines.append(transliterated_line)
        
        transliterated_text = '\n'.join(transliterated_lines)
        transliterated_content += header + transliterated_text + '\n\n'
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(transliterated_content)

# Example usage:
input_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/input.srt'
output_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
source_script = 'TAMIL'
transliterate_srt(input_file_path, output_file_path, source_script)

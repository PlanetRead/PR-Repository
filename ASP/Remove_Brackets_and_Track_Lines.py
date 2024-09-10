def remove_brackets_and_track_lines(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    new_lines = []
    bracket_lines = []
    for i, line in enumerate(lines):
        if '[' in line and ']' in line:
            bracket_lines.append(i + 1)
            new_line = line.replace('[', '').replace(']', '')
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    
    return bracket_lines

# Example usage:
txt_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/input.txt'
bracket_lines = remove_brackets_and_track_lines(txt_file_path)
print(bracket_lines)

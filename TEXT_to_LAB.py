def txt_to_lab(txt, lab):
    with open(txt, 'r', encoding='utf-8') as txt_file, open(lab, 'w', encoding='utf-8') as lab_file:
        for line in txt_file:
            lab_file.write(line)

# Example usage:
txt_file_path = 'input.txt'
lab_file_path = 'output.lab'
txt_to_lab(txt_file_path, lab_file_path)
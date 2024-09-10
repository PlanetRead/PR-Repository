def add_multiple_files_to_zip(files_to_add):
    with zipfile.ZipFile(archived, 'a') as zip_ref:
        for file in files_to_add:
            zip_ref.write(file)

# Example usage:
archived = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.zip'
files_to_add = ['file1.txt', 'file2.txt']
add_multiple_files_to_zip(files_to_add)

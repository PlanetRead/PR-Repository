def create_or_empty_zip(zip_filename, files_to_add):    
    # Create a new empty zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Add specified files to the zip file
        for file in files_to_add:
            if os.path.exists(file) and os.access(file, os.R_OK):
                zipf.write(file, os.path.basename(file))

# Example usage:
zip_filename = 'output.zip'
files_to_add = ['file1.txt', 'file2.txt']
create_or_empty_zip(zip_filename, files_to_add)

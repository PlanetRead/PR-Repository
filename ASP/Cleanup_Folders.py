def cleanup_folders():
    specific_folder = 'C:/Users/Administrator/Documents/MFA/forced_alignment'
    if os.path.exists(specific_folder):
        shutil.rmtree(specific_folder)
    if os.path.exists(upload):
        shutil.rmtree(upload)

# Example usage:
cleanup_folders()

import requests

# Define the API endpoint
url = "http://localhost:8000/align/"

# Paths to the test WAV and TXT files
wav_file_path = r"C:\Users\abina\OneDrive\Desktop\test\028_AK5_PUN_BB_C.wav"
txt_file_path = r"C:\Users\abina\OneDrive\Desktop\test\028_AK5_PUN_BB_C.txt"

# Open the files in binary mode
with open(wav_file_path, "rb") as wav_file, open(txt_file_path, "rb") as txt_file:
    # Define the files to be uploaded
    files = {
        "wav_file": wav_file,
        "txt_file": txt_file
    }
    
    # Send the POST request
    response = requests.post(url, files=files)
    
    # Print the response from the API
    print(response.json())

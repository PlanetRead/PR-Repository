from fastapi import FastAPI, File, UploadFile
import os
import subprocess
import shutil

app = FastAPI()

# Define your paths
input_dir = "input_dir"
output_dir = "output_dir"
dictionary_path = r"H:\pretrained_models_tanishka\dictionary\punjabi_cv.dict"
acoustic_model_path = r"H:\pretrained_models_tanishka\acoustic\new_acoustic_model.zip"

# Ensure directories exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Command to activate the conda environment
activate_env = "conda activate aligner"

@app.post("/align/")
async def align_files(wav_file: UploadFile = File(...), txt_file: UploadFile = File(...)):
    # Save uploaded files
    wav_path = os.path.join(input_dir, wav_file.filename)
    txt_path = os.path.join(input_dir, txt_file.filename)
    
    with open(wav_path, "wb") as f:
        shutil.copyfileobj(wav_file.file, f)
    
    with open(txt_path, "wb") as f:
        shutil.copyfileobj(txt_file.file, f)

    # Run the MFA align command
    mfa_command = f'mfa align "{input_dir}" "{dictionary_path}" "{acoustic_model_path}" "{output_dir}" --beam 400'
    command = f"{activate_env} && {mfa_command}"
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

    return {"message": f"Alignment completed. TextGrid files saved in {output_dir}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Speech Recognition Model for Indic and Local Languages.

The model is trained on large databases of different languages and dilects of those in different regions of india, the model is trained on simple CPU , and the computational cost is lowest as compared to different SR models across the worlds, we aim to build the tool in all different languages all over the world so that there will be no linguistic barriers among us.


## Replicating the Development Environment

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

Requirements for the software and other tools to build, test and push 
- Windows 11 64-bit
- Lower version of windows also works fine

### Installing

A step by step series of examples that tell you how to get a development
environment running

[Download Miniconda3](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe/)

Navigate through the installation Steps in Windows Just Click on Next.
Open miniconda3 prompt in Windows and check the conda version

    conda --version
    #24.5.0

Create a Working Directory

    mkdir ASP-project
    cd ASP-project

Install Montreal Force Aligner

    conda create -n aligner -c conda-forge montreal-forced-aligner
    conda activate aligner

Install Pytorch CPU

    conda install pytorch torchvision torchaudio cpuonly -c pytorch

Install SpeechBrain

    pip install speechbrain    


Inside the aligner conda environment install python libraries

    pip install pysrt streamlit aksharamukha moviepy
    


## Running the tests

Download the pretrained models from google drive [link](https://drive.google.com/drive/folders/1tKWAEtgFSK5pngsP08mYECbLaH4-_ROt?usp=sharing)
This link will contain two extra folders named "forced_alignment" and "upload" download these two also they handle file handling temporarily.
Store them in the working directory you have created.

Inside the working directory 

    git clone https://github.com/Abinash-bit/MFA-V2.git

Now in appV2.py 
- Change the desired folder path
    


### Run appV2.py

    streamlit run appV2.py


## Yeah You are ready with the development set up



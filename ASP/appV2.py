import os
import re
import pysrt
import shutil
import base64
import zipfile
import streamlit as st
import subprocess as sp
from datetime import timedelta
from aksharamukha import transliterate
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

st.set_page_config(page_title='Generate Subtitles🎬', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.config.set_option("server.maxUploadSize", 5000)
st.config.set_option("server.maxMessageSize", 5000)
st.config.set_option("server.enableWebsocketCompression", 'true')

folder = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment'  # Use a temporary folder
if os.path.exists(folder):
    shutil.rmtree(folder) 
os.makedirs(folder)
upload = 'C:/Users/Administrator/Desktop/ASP-Project/upload'
if os.path.exists(upload):
    shutil.rmtree(upload) 
os.makedirs(upload)

def create_or_empty_zip(zip_filename, files_to_add):    
    # Create a new empty zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Add specified files to the zip file
        for file in files_to_add:
            if os.path.exists(file) and os.access(file, os.R_OK):
                zipf.write(file, os.path.basename(file))

def trim_audio(input_file_path, output_file_path, start_time, end_time):
    # Load the video file
    audio = AudioSegment.from_wav(input_file_path)
    # Trim the video
    trimmed_audio = audio[start_time * 1000:end_time * 1000]
    # Save the trimmed video
    trimmed_audio.export(output_file_path, format="wav")

def mp4_to_wav(mp4, wav):
    video = VideoFileClip(mp4)
    video.audio.write_audiofile(wav, codec='pcm_s16le')

def mp3_to_wav(mp3, wav):
    audio = AudioSegment.from_mp3(mp3)
    audio.export(wav, format="wav")

def txt_to_lab(txt, lab):
    with open(txt, 'r', encoding='utf-8') as txt_file, open(lab, 'w', encoding='utf-8') as lab_file:
        for line in txt_file:
            lab_file.write(line)

def english(path, textgrid):
    st.write("<h7 class = 'stLang'>Running Alignment for English...</h7>", unsafe_allow_html=True)
    sp.run(['conda', 'run', '--name', 'aligner', 'mfa', 'align', path, "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/dictionary/english_us_arpa.dict", "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/acoustic/english_us_arpa.zip", path], shell=True, check=True)
    if not os.path.exists(textgrid):
        raise FileNotFoundError(f"{textgrid} not found after alignment process.")
    with open(textgrid, 'r', encoding='utf-8') as file:
        out = file.read()
    st.write("<h7 class = 'stLang'>Alignment Complete.</h7>", unsafe_allow_html=True)

    return out

def tamil(path, textgrid):
    st.write("<h7 class = 'stLang'>Running Alignment for Tamil...</h7>", unsafe_allow_html=True)
    align_command = ['conda', 'run', '--name', 'aligner', 'mfa', 'align', path, 
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/dictionary/tamil_cv.dict",
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/acoustic/tamil_cv.zip",
                     path, '--beam', '400', '--clean']
    sp.run(align_command, shell=True, check=True)
    if not os.path.exists(textgrid):
        raise FileNotFoundError(f"{textgrid} not found after alignment process.")
    with open(textgrid, 'r', encoding='utf-8') as file:
        out = file.read()

    st.write("<h7 class = 'stLang'>Alignment Complete.</h7>", unsafe_allow_html=True)

    return out

def hindi(path,textgrid):
    st.write("<h7 class='stLang'>Running Alignment for Hindi...</h7>", unsafe_allow_html=True)
    align_command = ['conda', 'run', '--name', 'aligner', 'mfa', 'align', path, 
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models/acoustic/hindi_cv.dict",
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models/acoustic/my_hindi.zip",
                     path, '--beam', '400']
    
    sp.run(align_command, shell=True, check=True)
    if not os.path.exists(textgrid):
        raise FileNotFoundError(f"{textgrid} not found after alignment process.")
    with open(textgrid, 'r', encoding='utf-8') as file:
        out = file.read()

    st.write("<h7 class = 'stLang'>Alignment Complete.</h7>", unsafe_allow_html=True)

    return out

def punjabi(path,textgrid):
    st.write("<h7 class = 'stLang'>Running Alignment for Punjabi...</h7>", unsafe_allow_html=True)
    align_command = ['conda', 'run', '--name', 'aligner', 'mfa', 'align', path, 
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/dictionary/punjabi_cv.dict",
                     "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/acoustic/new_acoustic_model.zip",
                     path, '--beam', '400']
    try:
        sp.run(align_command, shell=True, check=True)
    except sp.CalledProcessError:
        st.error('The voice in the file does not match.')
        return None  # Return None to indicate failure
    if not os.path.exists(textgrid):
        raise FileNotFoundError(f"{textgrid} not found after alignment process.")
    with open(textgrid, 'r', encoding='utf-8') as file:
        out = file.read()

    st.write("<h7 class = 'stLang'>Alignment Complete.</h7>", unsafe_allow_html=True)

    return out

def parse_textgrid(textgrid_data):
    intervals = []
    words_tier_pattern = re.compile(r'item \[\d+\]:\s*class = "IntervalTier"\s*name = "words"[\s\S]*?intervals: size = \d+\s([\s\S]*?)item \[\d+\]:', re.MULTILINE)
    interval_pattern = re.compile(r"intervals \[\d+\]:\s*xmin = ([\d.]+)\s*xmax = ([\d.]+)\s*text = \"(.*?)\"", re.DOTALL)
    words_tier = words_tier_pattern.search(textgrid_data)
    if words_tier:
        for match in interval_pattern.finditer(words_tier.group(1)):
            xmin = float(match.group(1))
            xmax = float(match.group(2))
            text = match.group(3).strip()
            if text:
                intervals.append((xmin, xmax, text))
    return intervals

def convert_to_srt_time(time_seconds):
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    milliseconds = int((time_seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def write_srt(intervals, srt_path):
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        for index, (start, end, text) in enumerate(intervals, start=1):
            srt_file.write(f"{index}\n")
            srt_file.write(f"{convert_to_srt_time(start)} --> {convert_to_srt_time(end)}\n")
            srt_file.write(f"{text}\n\n")

def textgrid_to_srt(textgrid_content, srt_path):
    intervals = parse_textgrid(textgrid_content)
    write_srt(intervals, srt_path)

def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', re.DOTALL)
    matches = pattern.findall(content)
    words_data = []
    for match in matches:
        index, start_time, end_time, word = match
        words_data.append((start_time, end_time, word.strip()))
    return words_data

def parse_lab(lab_file):
    with open(lab_file, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def generate_sentence_timestamps(words_data, sentences):
    word_index = 0
    sentence_data = []
    total_words = len(words_data)
    for sentence in sentences:
        words = sentence.split()
        num_words = len(words)
        if num_words == 0:
            continue
        if word_index + num_words > total_words:
            remaining_words = total_words - word_index
            if remaining_words > 0:
                start_time = words_data[word_index][0]
                end_time = words_data[-1][1]
                partial_sentence = ' '.join([words[i] for i in range(remaining_words)])
                sentence_data.append((start_time, end_time, partial_sentence))
            break
        start_time = words_data[word_index][0]
        end_time = words_data[word_index + num_words - 1][1]
        sentence_data.append((start_time, end_time, sentence))
        word_index += num_words
    return sentence_data

def write_new_srt(sentence_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, (start_time, end_time, sentence) in enumerate(sentence_data, start=1):
            file.write(f"{index}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{sentence}\n\n")

def add_timedelta_to_subriptime(subrip_time, tdelta):
    total_milliseconds = int(tdelta.total_seconds() * 1000)
    new_milliseconds = subrip_time.ordinal + total_milliseconds
    return pysrt.SubRipTime.from_ordinal(new_milliseconds)

def adjust_srt_timestamps(input_srt_path, output_srt_path, start_time_seconds):
    subs = pysrt.open(input_srt_path, encoding='utf-8')
    start_time_delta = timedelta(seconds=start_time_seconds)
    for sub in subs:
        sub.start = add_timedelta_to_subriptime(sub.start, start_time_delta)
        sub.end = add_timedelta_to_subriptime(sub.end, start_time_delta)
    subs.save(output_srt_path, encoding='utf-8')

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

def time_in_sec(format):
    list1 = format.split(':')
    list2 = list1[2].split(',')
    time_in_seconds = (float(str(list1[0]))*3600)+(float(str(list1[1]))*60)+float(str(list2[0]))
    return time_in_seconds

def combine_srt_files(file1, file2, output_file):
    subs1 = pysrt.open(file1, encoding='utf-8')
    subs2 = pysrt.open(file2, encoding='utf-8')
    
    if len(subs1) != len(subs2):
        raise ValueError("SRT files do not have the same number of subtitles.")
    
    combined_subs = pysrt.SubRipFile()
    for sub1, sub2 in zip(subs1, subs2):
        if sub1.start != sub2.start or sub1.end != sub2.end:
            raise ValueError("Subtitles do not have matching timestamps.")
        
        combined_text = f"{sub1.text}\n{sub2.text}"
        combined_sub = pysrt.SubRipItem(index=sub1.index, start=sub1.start, end=sub1.end, text=combined_text)
        combined_subs.append(combined_sub)
    
    combined_subs.save(output_file, encoding='utf-8')

def add_multiple_files_to_zip(files_to_add):
    with zipfile.ZipFile(archived, 'a') as zip_ref:
        for file in files_to_add:
            zip_ref.write(file)

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

def add_brackets_to_srt(srt_path, bracket_lines):
    subs = pysrt.open(srt_path, encoding='utf-8')
    for line_number in bracket_lines:
        if line_number - 1 < len(subs):
            subs[line_number - 1].text = f"[{subs[line_number - 1].text}]"
    subs.save(srt_path, encoding='utf-8')

def alignment(mp4, txt, language, start=0, stop=0):
    st.write("<h7 class = 'stLang'>Performing Alignment...</h7>", unsafe_allow_html=True)
    progress_bar.progress(10)  # Update progress bar

    with open(mp4_path, 'wb') as f:
        f.write(mp4.getvalue())
    with open(txt_path, 'wb') as f:
        f.write(txt.getvalue())

    progress_bar.progress(20)  # Update progress bar

    if mp4_path.endswith('.mp4'):
        mp4_to_wav(mp4_path, wav_path)
    elif mp4_path.endswith('.mp3'):
        mp3_to_wav(mp4_path, wav_path)
    elif mp4_path.endswith('.wav'):
        # If the file is already a WAV, just copy it to the destination
        shutil.copyfile(mp4_path, wav_path)
    else:
        raise ValueError("Unsupported file format. Please upload an MP4, MP3, or WAV file.")

    progress_bar.progress(30)

    if start != 0 and stop != 0:
        trimmed_wav = os.path.join(upload, 'trimmed.wav')
        trim_audio(wav_path, trimmed_wav, start, stop)
        progress_bar.progress(40)

    bracket_lines = remove_brackets_and_track_lines(txt_path)
    st.write(f"Lines with brackets removed: {bracket_lines}")

    txt_to_lab(txt_path, lab_path)
    progress_bar.progress(50)

    if language == 'English':
        textgrid_content = english(folder, textgrid_path)
    elif language == 'Tamil':
        textgrid_content = tamil(folder, textgrid_path)
        source_lang = 'TAMIL'
    elif language == 'Hindi':
        textgrid_content = hindi(folder, textgrid_path)
        source_lang = 'DEVANAGARI'
    elif language == 'Punjabi':
        textgrid_content = punjabi(folder, textgrid_path)
        source_lang = 'GURMUKHI'

    progress_bar.progress(70)
    
    if language in ['English', 'Tamil', 'Hindi', 'Punjabi']:
        if textgrid_content:
            textgrid_to_srt(textgrid_content, unaligned_path)
        else:
            raise ValueError("TextGrid content is empty.")
    
    progress_bar.progress(80)
        
    st.write("<h7 class = 'stLang'>Generating Subtitles :)</h7>", unsafe_allow_html=True)
    words_data = parse_srt(unaligned_path)
    sentences = parse_lab(lab_path)
    sentence_data = generate_sentence_timestamps(words_data, sentences)
    write_new_srt(sentence_data, finalsrt_path)

    progress_bar.progress(90)
    adjust_srt_timestamps(finalsrt_path, alignedsrt_path, start)

    add_brackets_to_srt(alignedsrt_path, bracket_lines)

    progress_bar.progress(100)
    st.write("<h7 class = 'stLang'>Alignment Successful!</h7>", unsafe_allow_html=True)

    transliterate_srt(alignedsrt_path, trans_srt_path, source_lang)

    combine_srt_files(alignedsrt_path,trans_srt_path, combined_file)

    files_to_add = [alignedsrt_path, trans_srt_path, combined_file]
    create_or_empty_zip(archived, files_to_add)

    # Store the content in session state
    st.session_state.srt_content = open(alignedsrt_path, 'r', encoding='utf-8').read()
    st.session_state.transliterated_content = open(trans_srt_path, 'r', encoding='utf-8').read()
    st.session_state.combined_content = open(combined_file, 'r', encoding='utf-8').read()
    st.session_state.zip_content = open(archived, "rb").read()

def cleanup_folders():
    specific_folder = 'C:/Users/Administrator/Documents/MFA/forced_alignment'
    if os.path.exists(specific_folder):
        shutil.rmtree(specific_folder)
    if os.path.exists(upload):
        shutil.rmtree(upload)

st.markdown('<h1 class="stTitle">Align and Generate Your Subtitles!</h1>', unsafe_allow_html=True)
st.write('<h5 class="stLang">Select the Language of your video</h5>', unsafe_allow_html=True)
lang = st.selectbox('', ['English', 'Tamil', 'Hindi', 'Punjabi'])
st.write('<h5 class="stLang">Select your Video</h5>', unsafe_allow_html=True)
mp4_file = st.file_uploader('', type=['mp4', 'mp3', 'wav'])

trim_option = st.checkbox('Do you want to trim the audio?')

if trim_option:
    st.write('<h5 class="stLang">Enter the starting timestamp in the format HH:MM:SS,mmm</h5>', unsafe_allow_html=True)
    starting_time = st.text_input("")
    st.write('<h5 class="stLang">Enter the ending timestamp in the format HH:MM:SS,mmm</h5>', unsafe_allow_html=True)
    ending_time = st.text_input(" ")
else:
    starting_time = "00:00:00,000"
    ending_time = "00:00:00,000"

st.write('<h5 class="stLang">Select your Script</h5>', unsafe_allow_html=True)
txt_file = st.file_uploader('', type=['txt'])
submit_button = st.button(label='Generate your SRT')
if submit_button:
    if lang and mp4_file and txt_file:
        try:
            nom = mp4_file.name.split('.')
            filename = nom[0]+'.srt'
            transfilename = nom[0] + '_transliterated.srt'
            combfilename = nom[0] + '_combined.srt'
            zipp = nom[0]+'.zip'

            wav_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '.wav'
            lab_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '.lab'

            textgrid_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '.TextGrid'

            unaligned_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/movie_unaligned.srt'
            finalsrt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/movie_aligned.srt'

            alignedsrt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '.srt'
            trans_srt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '_transliterated.srt'
            combined_file = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/' + nom[0] + '_combined.srt'

            archived = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/zipped_output.zip'
            progress_bar = st.progress(0)  # Initialize progress bar
            st.write("<h7 class = 'stLang'>Files Uploaded!</h7>", unsafe_allow_html=True)
            mp4_path = os.path.join(upload, mp4_file.name)
            txt_path = os.path.join(upload, txt_file.name)

            alignment(mp4_file, txt_file, lang, time_in_sec(starting_time), time_in_sec(ending_time))
            
            st.download_button(
                label="Download ZIPPED File containing both SRT file",
                data=st.session_state.zip_content,
                file_name=zipp,
                mime="application/zip")

            st.text_area('Generated SRT File:', value=st.session_state.srt_content, height=400)
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            cleanup_folders()

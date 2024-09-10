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

    combine_srt_files(alignedsrt_path, trans_srt_path, combined_file)

    files_to_add = [alignedsrt_path, trans_srt_path, combined_file]
    create_or_empty_zip(archived, files_to_add)

    # Store the content in session state
    st.session_state.srt_content = open(alignedsrt_path, 'r', encoding='utf-8').read()
    st.session_state.transliterated_content = open(trans_srt_path, 'r', encoding='utf-8').read()
    st.session_state.combined_content = open(combined_file, 'r', encoding='utf-8').read()
    st.session_state.zip_content = open(archived, "rb").read()

# Example usage:
mp4_file = st.file_uploader('Upload MP4 file', type=['mp4', 'mp3', 'wav'])
txt_file = st.file_uploader('Upload TXT file', type=['txt'])
language = st.selectbox('Select Language', ['English', 'Tamil', 'Hindi', 'Punjabi'])
start_time = st.text_input('Enter start time (HH:MM:SS,mmm)')
stop_time = st.text_input('Enter stop time (HH:MM:SS,mmm)')
submit_button = st.button('Generate SRT')

if submit_button:
    if mp4_file and txt_file:
        mp4_path = os.path.join(upload, mp4_file.name)
        txt_path = os.path.join(upload, txt_file.name)
        wav_path = os.path.join(upload, 'output.wav')
        lab_path = os.path.join(upload, 'output.lab')
        textgrid_path = os.path.join(upload, 'output.TextGrid')
        unaligned_path = os.path.join(upload, 'unaligned.srt')
        finalsrt_path = os.path.join(upload, 'final.srt')
        alignedsrt_path = os.path.join(upload, 'aligned.srt')
        trans_srt_path = os.path.join(upload, 'transliterated.srt')
        combined_file = os.path.join(upload, 'combined.srt')
        archived = os.path.join(upload, 'output.zip')
        progress_bar = st.progress(0)
        alignment(mp4_file, txt_file, language, time_in_sec(start_time), time_in_sec(stop_time))
        st.download_button(
            label="Download ZIPPED File containing both SRT file",
            data=st.session_state.zip_content,
            file_name='output.zip',
            mime="application/zip")
        st.text_area('Generated SRT File:', value=st.session_state.srt_content, height=400)

def english(path, textgrid):
    st.write("<h7 class = 'stLang'>Running Alignment for English...</h7>", unsafe_allow_html=True)
    sp.run(['conda', 'run', '--name', 'aligner', 'mfa', 'align', path, 
            "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/dictionary/english_us_arpa.dict", 
            "C:/Users/Administrator/Desktop/ASP-Project/pretrained_models_tanishka/acoustic/english_us_arpa.zip", 
            path], shell=True, check=True)
    if not os.path.exists(textgrid):
        raise FileNotFoundError(f"{textgrid} not found after alignment process.")
    with open(textgrid, 'r', encoding='utf-8') as file:
        out = file.read()
    st.write("<h7 class = 'stLang'>Alignment Complete.</h7>", unsafe_allow_html=True)
    return out

# Example usage:
path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment'
textgrid_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.TextGrid'
english(path, textgrid_path)
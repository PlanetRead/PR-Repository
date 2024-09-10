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

# Example usage:
file1_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/file1.srt'
file2_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/file2.srt'
output_file_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/combined.srt'
combine_srt_files(file1_path, file2_path, output_file_path)

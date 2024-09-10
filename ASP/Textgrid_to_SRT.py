def textgrid_to_srt(textgrid_content, srt_path):
    intervals = parse_textgrid(textgrid_content)
    write_srt(intervals, srt_path)

# Example usage:
textgrid_content = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.TextGrid'
srt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
textgrid_to_srt(textgrid_content, srt_path)

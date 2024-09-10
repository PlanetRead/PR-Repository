def write_srt(intervals, srt_path):
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        for index, (start, end, text) in enumerate(intervals, start=1):
            srt_file.write(f"{index}\n")
            srt_file.write(f"{convert_to_srt_time(start)} --> {convert_to_srt_time(end)}\n")
            srt_file.write(f"{text}\n\n")

# Example usage:
intervals = [(0.0, 2.5, "Hello"), (2.5, 5.0, "World")]
srt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
write_srt(intervals, srt_path)

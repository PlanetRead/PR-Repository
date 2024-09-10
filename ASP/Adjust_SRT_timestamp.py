def adjust_srt_timestamps(input_srt_path, output_srt_path, start_time_seconds):
    subs = pysrt.open(input_srt_path, encoding='utf-8')
    start_time_delta = timedelta(seconds=start_time_seconds)
    for sub in subs:
        sub.start = add_timedelta_to_subriptime(sub.start, start_time_delta)
        sub.end = add_timedelta_to_subriptime(sub.end, start_time_delta)
    subs.save(output_srt_path, encoding='utf-8')

# Example usage:
input_srt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/input.srt'
output_srt_path = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.srt'
start_time_seconds = 10
adjust_srt_timestamps(input_srt_path, output_srt_path, start_time_seconds)

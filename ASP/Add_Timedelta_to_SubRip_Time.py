def add_timedelta_to_subriptime(subrip_time, tdelta):
    total_milliseconds = int(tdelta.total_seconds() * 1000)
    new_milliseconds = subrip_time.ordinal + total_milliseconds
    return pysrt.SubRipTime.from_ordinal(new_milliseconds)

# Example usage:
subrip_time = pysrt.SubRipTime(0, 0, 0, 0)
tdelta = timedelta(seconds=10)
new_time = add_timedelta_to_subriptime(subrip_time, tdelta)
print(new_time)

def time_in_sec(format):
    list1 = format.split(':')
    list2 = list1[2].split(',')
    time_in_seconds = (float(str(list1[0]))*3600)+(float(str(list1[1]))*60)+float(str(list2[0]))
    return time_in_seconds

# Example usage:
time_format = '00:01:40,500'
seconds = time_in_sec(time_format)
print(seconds)

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

# Example usage:
textgrid_data = 'C:/Users/Administrator/Desktop/ASP-Project/forced_alignment/output.TextGrid'
intervals = parse_textgrid(textgrid_data)

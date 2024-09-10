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

# Example usage:
words_data = [('00:00:00,000', '00:00:02,500', 'Hello'), ('00:00:02,500', '00:00:05,000', 'World')]
sentences = ["Hello World"]
sentence_data = generate_sentence_timestamps(words_data, sentences)

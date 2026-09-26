class LZ77:
    def __init__(self, window_size=4096, lookahead_buffer_size=256):
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size
        self.tags = []

    def compress(self, data):
        self.tags = []
        i = 0
        while i < len(data):
            match = self.find_longest_match(data, i)
            if match:
                (best_match_distance, best_match_length) = match
                next_char = data[i + best_match_length] if (i + best_match_length) < len(data) else ''
                self.tags.append((best_match_distance, best_match_length, next_char))
                i += best_match_length + 1
            else:
                self.tags.append((0, 0, data[i]))
                i += 1
                

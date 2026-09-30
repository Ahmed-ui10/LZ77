def compress(text, window_size=8192, lookahead_size=4096):

    tags = []
    i = 0
    n = len(text)

    while i < n:

        best_position = 0
        best_length = 0

        search_start = max(0, i - window_size)

        max_length = min(lookahead_size, n - i)

        for j in range(search_start, i):

            length = 0
            distance = i - j

            while length < max_length:

                match_position = j + length

                if match_position >= i:
                    match_position = i + (length - distance)

                if text[i + length] != text[match_position]:
                    break

                length += 1

            if length > best_length:
                best_length = length
                best_position = distance

        if i + best_length < n:
            next_symbol = text[i + best_length]
        else:
            next_symbol = ""

        tags.append((best_position, best_length, next_symbol))

        i += best_length + 1

    return tags


def decompress(tags):
    """
    LZ77 Decompression

    Supports overlapping / repetitive sequences.
    """

    output = []

    for position, length, next_symbol in tags:

        if position > 0:

            start = len(output) - position

            for _ in range(length):
                output.append(output[start])

                start += 1

        if next_symbol != "":
            output.append(next_symbol)

    return "".join(output)

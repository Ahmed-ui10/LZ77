import struct

def _compress(text, window_size=8192, lookahead_size=4096):
    tags = []
    i = 0
    n = len(text)

    while i < n:
        best_position = 0
        best_length = 0

        search_start = max(0, i - window_size)

        max_length = min(lookahead_size, n - i)

        for j in range(search_start, i):
            distance = i - j
            length = 0

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


def compress_file(input_path, output_path,
                  window_size=8192, lookahead_size=4096):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    tags = _compress(text, window_size, lookahead_size)

    with open(output_path, "wb") as f:
        f.write(struct.pack("<I", len(tags)))
        for position, length, next_symbol in tags:
            f.write(struct.pack("<IH", position, length))
            if next_symbol:
                f.write(struct.pack("<B", 1))
                f.write(next_symbol.encode("utf-8")[:1].ljust(1, b"\x00"))
            else:
                f.write(struct.pack("<B", 0))
                f.write(b"\x00")

    return tags, text


def read_compressed_file(path):
    """Read binary file and return tags."""
    tags = []
    with open(path, "rb") as f:
        count_bytes = f.read(4)
        if len(count_bytes) < 4:
            return tags
        count = struct.unpack("<I", count_bytes)[0]

        for _ in range(count):
            pos_len = f.read(6)
            position, length = struct.unpack("<IH", pos_len)
            flag = struct.unpack("<B", f.read(1))[0]
            sym_byte = f.read(1)
            if flag == 1:
                next_symbol = sym_byte.decode("utf-8", errors="ignore")
            else:
                next_symbol = ""
            tags.append((position, length, next_symbol))
    return tags
from lz_compression import read_compressed_file

def _decompress(tags):
    """
    Decompress LZ77 tags.
    Handles repetitive / overlapped sequences because we append
    symbols one by one to the result list.
    """
    result = []

    for position, length, next_symbol in tags:
        if length > 0:
            start = len(result) - position
            for k in range(length):
                result.append(result[start + k])

        if next_symbol:
            result.append(next_symbol)

    return "".join(result)



def decompress_file(input_path, output_path):
    tags = read_compressed_file(input_path)
    text = _decompress(tags)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return tags, text
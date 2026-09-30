from LZ77 import compress, decompress
import ast


def main():

    print("=" * 40)
    print("       LZ77 Compression System")
    print("=" * 40)

    print("\nChoose an operation:")
    print("1. Compression")
    print("2. Decompression")

    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":

        text = input("\nEnter the text to compress: ")

        if text == "":
            print("Error: Text cannot be empty.")
            return

        tags = compress(text)

        print("\nOriginal Text:")
        print(text)

        print("\nGenerated LZ77 Tags:")

        for i, tag in enumerate(tags, 1):
            position, length, next_symbol = tag

            print(
                f'Tag {i}: <{position},{length},"{next_symbol}">'
            )

        
        original_size = len(text) * 8

        max_position = max(tag[0] for tag in tags)
        max_length = max(tag[1] for tag in tags)

        position_bits = max(1, max_position.bit_length())

        length_bits = max(1, max_length.bit_length())

        symbol_bits = 8

        tag_size = position_bits + length_bits + symbol_bits

        compressed_size = len(tags) * tag_size

        compression_ratio = original_size / compressed_size

        compressed_percentage = (
            compressed_size / original_size
        ) * 100

        saving_percentage = (
            (original_size - compressed_size)
            / original_size
        ) * 100


        print("\n" + "=" * 40)
        print("       Compression Statistics")
        print("=" * 40)

        print(f"Original Size       : {original_size} bits")
        print(f"Compressed Size     : {compressed_size} bits")

        print(f"Position Bits       : {position_bits} bits")
        print(f"Length Bits         : {length_bits} bits")
        print(f"Symbol Bits         : {symbol_bits} bits")

        print(f"Tag Size            : {tag_size} bits")
        print(f"Number of Tags      : {len(tags)}")

        print(
            f"\nCompression Ratio   : "
            f"{compression_ratio:.2f}:1"
        )

        print(
            f"Compressed Size     : "
            f"{compressed_percentage:.2f}%"
        )

        print(
            f"Space Saving        : "
            f"{saving_percentage:.2f}%"
        )

        print("\nCompression completed successfully.")

    elif choice == "2":

        print("\nEnter the LZ77 tags.")
        print("Example:")
        print(
            "[(0, 0, 'A'), "
            "(0, 0, 'B'), "
            "(2, 1, 'A')]"
        )

        tags_input = input("\nTags: ")

        try:
            tags = ast.literal_eval(tags_input)

            if not isinstance(tags, list):
                print("Error: Tags must be entered as a list.")
                return

            for tag in tags:

                if not isinstance(tag, tuple) or len(tag) != 3:
                    print(
                        "Error: Each tag must have the form "
                        "(position, length, next_symbol)."
                    )
                    return

                position, length, next_symbol = tag

                if not isinstance(position, int) or position < 0:
                    print(
                        "Error: Position must be "
                        "a non-negative integer."
                    )
                    return

                if not isinstance(length, int) or length < 0:
                    print(
                        "Error: Length must be "
                        "a non-negative integer."
                    )
                    return

                if not isinstance(next_symbol, str):
                    print(
                        "Error: Next symbol must be a string."
                    )
                    return

            text = decompress(tags)

            print("\nDecompressed Text:")
            print(text)

            print("\nDecompression completed successfully.")

        except (ValueError, SyntaxError):
            print("Error: Invalid tags format.")

    else:
        print("\nInvalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()

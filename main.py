import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from lz_compression import compress_file
from lz_decompression import decompress_file

77
BG_MAIN      = "#1e1e1e"
BG_PANEL     = "#252526"
BG_TEXT      = "#1a1a1a"
FG_TEXT      = "#d4d4d4"
FG_ACCENT    = "#4ec9b0"
FG_LABEL     = "#cccccc"

BTN_COMPRESS   = "#0e7c66"
BTN_DECOMPRESS = "#0e5a8a"
BTN_CLEAR      = "#8a2c2c"
BTN_FG         = "#ffffff"


class LZ77GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LZ77 Compression System")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_MAIN)

        self.compressed_file = None
        self.tags = []

        top = tk.Frame(root, pady=10, bg=BG_MAIN)
        top.pack(fill="x")

        tk.Button(top, text="🗜️ Compress",
                  width=18, command=self.do_compress,
                  bg=BTN_COMPRESS, fg=BTN_FG,
                  activebackground="#0a5c4c",
                  activeforeground="#ffffff",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2",
                  borderwidth=0).pack(side="left", padx=5)

        tk.Button(top, text="📤 Decompress",
                  width=18, command=self.do_decompress,
                  bg=BTN_DECOMPRESS, fg=BTN_FG,
                  activebackground="#0a4066",
                  activeforeground="#ffffff",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2",
                  borderwidth=0).pack(side="left", padx=5)

        tk.Button(top, text="🧹 Clear",
                  width=12, command=self.clear_all,
                  bg=BTN_CLEAR, fg=BTN_FG,
                  activebackground="#661f1f",
                  activeforeground="#ffffff",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2",
                  borderwidth=0).pack(side="left", padx=5)

        mid = tk.Frame(root, bg=BG_MAIN)
        mid.pack(fill="both", expand=True, padx=10, pady=5)

        mid.columnconfigure(0, weight=1)
        mid.columnconfigure(1, weight=1)
        mid.rowconfigure(0, weight=1)

        left = tk.Frame(mid, bg=BG_PANEL, bd=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        tk.Label(left, text="  Generated LZ77 Tags:",
                 anchor="w", bg=BG_PANEL, fg=FG_LABEL,
                 font=("Arial", 12, "bold"),
                 pady=6).pack(fill="x")

        self.tags_area = scrolledtext.ScrolledText(
            left, height=20,
            font=("Consolas", 10),
            bg=BG_TEXT, fg=FG_TEXT,
            insertbackground=FG_ACCENT,
            selectbackground="#264f78",
            relief="flat", borderwidth=0,
            padx=8, pady=8)
        self.tags_area.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        right = tk.Frame(mid, bg=BG_PANEL, bd=0)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        tk.Label(right, text="  Statistics:",
                 anchor="w", bg=BG_PANEL, fg=FG_LABEL,
                 font=("Arial", 12, "bold"),
                 pady=6).pack(fill="x")

        self.stats_area = scrolledtext.ScrolledText(
            right, height=20,
            font=("Consolas", 10),
            bg=BG_TEXT, fg=FG_ACCENT,
            insertbackground=FG_ACCENT,
            selectbackground="#264f78",
            relief="flat", borderwidth=0,
            padx=8, pady=8)
        self.stats_area.pack(fill="both", expand=True, padx=4, pady=(0, 4))

    def do_compress(self):
        input_path = filedialog.askopenfilename(
            title="Select a text file to compress",
            filetypes=[("Text files", "*.txt"),
                       ("All files", "*.*")]
        )
        if not input_path:
            return

        default_name = os.path.splitext(
            os.path.basename(input_path))[0] + ".bin"
        save_path = filedialog.asksaveasfilename(
            title="Save compressed file",
            defaultextension=".bin",
            initialfile=default_name,
            filetypes=[("Binary files", "*.bin"),
                       ("All files", "*.*")]
        )
        if not save_path:
            return

        try:
            tags, text = compress_file(input_path, save_path)
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed:\n{e}")
            return

        self.compressed_file = save_path
        self.tags = tags

        self.tags_area.delete("1.0", tk.END)
        for i, tag in enumerate(tags, 1):
            position, length, next_symbol = tag
            self.tags_area.insert(
                tk.END,
                f'Tag {i}: <{position},{length},"{next_symbol}">\n'
            )

        original_size = len(text) * 8
        max_position = max((t[0] for t in tags), default=0)
        max_length = max((t[1] for t in tags), default=0)
        position_bits = max(1, max_position.bit_length())
        length_bits = max(1, max_length.bit_length())
        symbol_bits = 8
        tag_size = position_bits + length_bits + symbol_bits
        compressed_size = len(tags) * tag_size

        if compressed_size == 0:
            compression_ratio = 0
            compressed_percentage = 0
            saving_percentage = 0
        else:
            compression_ratio = original_size / compressed_size
            compressed_percentage = (compressed_size / original_size) * 100
            saving_percentage = ((original_size - compressed_size)
                                 / original_size) * 100

        stats = (
            "=======================================\n"
            "       Compression Statistics\n"
            "=======================================\n"
            f"Original Size       : {original_size} bits\n"
            f"Compressed Size     : {compressed_size} bits\n"
            f"Position Bits       : {position_bits} bits\n"
            f"Length Bits         : {length_bits} bits\n"
            f"Symbol Bits         : {symbol_bits} bits\n"
            f"Tag Size            : {tag_size} bits\n"
            f"Number of Tags      : {len(tags)}\n\n"
            f"Compression Ratio   : {compression_ratio:.2f}:1\n"
            f"Compressed Size     : {compressed_percentage:.2f}%\n"
            f"Space Saving        : {saving_percentage:.2f}%\n\n"
            f"✅ Compressed file saved at:\n{save_path}\n"
        )

        self.stats_area.delete("1.0", tk.END)
        self.stats_area.insert(tk.END, stats)

        messagebox.showinfo("Success", "Compression completed successfully ✅")

    def do_decompress(self):
        path = filedialog.askopenfilename(
            title="Select a .bin file to decompress",
            filetypes=[("Binary files", "*.bin"),
                       ("All files", "*.*")]
        )
        if not path:
            return

        save_path = filedialog.asksaveasfilename(
            title="Save decompressed file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"),
                       ("All files", "*.*")]
        )
        if not save_path:
            return

        try:
            tags, text = decompress_file(path, save_path)
        except Exception as e:
            messagebox.showerror("Error", f"Decompression failed:\n{e}")
            return

        self.tags_area.delete("1.0", tk.END)
        for i, tag in enumerate(tags, 1):
            position, length, next_symbol = tag
            self.tags_area.insert(
                tk.END,
                f'Tag {i}: <{position},{length},"{next_symbol}">\n'
            )

        self.stats_area.delete("1.0", tk.END)
        self.stats_area.insert(
            tk.END,
            "=======================================\n"
            "       Decompression Statistics\n"
            "=======================================\n"
            f"Number of Tags      : {len(tags)}\n"
            f"Original Text Size  : {len(text)} chars\n\n"
            f"✅ Decompressed file saved at:\n{save_path}\n"
        )
        messagebox.showinfo("Success", "Decompression completed successfully ✅")

    def clear_all(self):
        self.compressed_file = None
        self.tags = []
        self.tags_area.delete("1.0", tk.END)
        self.stats_area.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    LZ77GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
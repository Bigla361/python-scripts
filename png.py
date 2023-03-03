"""
Simple PNG Implementation by Bigla361

Only supports reading the IHDR chunk
so far.
"""

import tkinter as tk
from tkinter import filedialog

# Open OS Open UI
def get_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

# Get data at a specific offset
def get_at_offsets(hex_input, offset, length):
    return hex_input[int(offset, 16) * 2:][:length * 2]

# Convert hex to ascii
def hex_to_ascii(hex_input):
    return bytearray.fromhex(hex_input).decode()

# Open a file
file = open(get_file(), 'rb')
file_hex = file.read().hex()

# Check PNG Magic
if not file_hex.startswith("89504e470d0a1a0a"):
    raise Exception("Input file isn't a PNG file.")

# Data
color_types = {
    0: "Greyscale",
    2: "Truecolour",
    3: "Indexed-colour",
    4: "Greyscale with alpha",
    6: "Truecolour with alpha"
}
allowed_bit_depth = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16}
}
interlace_methods = {
    0: "None",
    1: "Adam7 interlace"
}

plte_color_types = {
    3,
    2,
    6
}

# Get Chunks
chunks = []
chunkstart = '08'
while True:
    length = int(get_at_offsets(file_hex, chunkstart, 4), 16)
    name = hex_to_ascii(get_at_offsets(file_hex, hex(int(chunkstart, 16) + 4), 4))
    data = get_at_offsets(file_hex, hex(int(chunkstart, 16) + 8), length)
    chunks.append({
        "name": name,
        "data": data
    })
    if name == "IEND":
        break
    chunkstart = hex(int(chunkstart, 16) + length + 12)

# IHDR
height = int(get_at_offsets(chunks[0]['data'], '0', 4), 16)
width = int(get_at_offsets(chunks[0]['data'], '4', 4), 16)
bitdepth = int(get_at_offsets(chunks[0]['data'], '8', 1), 16)
colortype = int(get_at_offsets(chunks[0]['data'], '9', 1), 16)
compression = int(get_at_offsets(chunks[0]['data'], 'A', 1), 16)
filtermethod = int(get_at_offsets(chunks[0]['data'], 'B', 1), 16)
interlacemethod = int(get_at_offsets(chunks[0]['data'], 'C', 1), 16)

# Check Data
if not colortype in color_types:
    raise Exception("Invalid color type!")
if not bitdepth in allowed_bit_depth[colortype]:
    raise Exception("Unallowed bit depth!")
if not interlacemethod in interlace_methods:
    raise Exception("Invalid interlace method!")

# Print Data
print(f"Resulution: {height}x{width}")
print(f"Bit Depth: {bitdepth}")
print(f"Color Type: {color_types[colortype]}")
print(f"Compression Method: {compression}")
print(f"Filter Method: {filtermethod}")
print(f"Interlace Method: {interlace_methods[interlacemethod]}")

# Read Chunks
for chunk in chunks:
    # Image last-modification time
    if chunk['name'] == 'tIME':
        print("Last Modification Date:", int(get_at_offsets(chunk['data'], '0', 2)))

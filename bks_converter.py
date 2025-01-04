from PIL import Image
import argparse

def save_as_bks(image_path, output_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size
        pixel_data = list(img.getdata())

    pixel_data_flat = [channel for pixel in pixel_data for channel in pixel]
    compressed_data = rle_compress(pixel_data_flat)

    with open(output_path, 'wb') as bks_file:
        bks_file.write(width.to_bytes(4, 'little'))
        bks_file.write(height.to_bytes(4, 'little'))
        bks_file.write(len(compressed_data).to_bytes(4, 'little'))
        bks_file.write(compressed_data)


def load_bks(file_path, output_path):
    with open(file_path, 'rb') as bks_file:
        width = int.from_bytes(bks_file.read(4), 'little')
        height = int.from_bytes(bks_file.read(4), 'little')
        compressed_length = int.from_bytes(bks_file.read(4), 'little')
        compressed_data = bks_file.read(compressed_length)

    pixel_data_flat = rle_decompress(compressed_data)
    pixel_data = [
        tuple(pixel_data_flat[i:i + 3]) for i in range(0, len(pixel_data_flat), 3)
    ]

    img = Image.new("RGB", (width, height))
    img.putdata(pixel_data)
    img.save(output_path)

def rle_compress(data):
    compressed = bytearray()
    prev_byte = data[0]
    count = 1

    for byte in data[1:]:
        if byte == prev_byte and count < 255:
            count += 1
        else:
            compressed.append(count)
            compressed.append(prev_byte)
            count = 1
        prev_byte = byte

    compressed.append(count)
    compressed.append(prev_byte)
    return compressed

def rle_decompress(data):
    decompressed = []
    for i in range(0, len(data), 2):
        count = data[i]
        value = data[i + 1]
        decompressed.extend([value] * count)
    return decompressed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PNG or JPEG images to and from .bks format")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Mode: compress or decompress")
    parser.add_argument("input_path", help="Path to the input file (PNG/JPEG or .bks)")
    parser.add_argument("output_path", help="Path to the output file (.bks or PNG/JPEG)")

    args = parser.parse_args()

    if args.mode == "compress":
        save_as_bks(args.input_path, args.output_path)
    elif args.mode == "decompress":
        load_bks(args.input_path, args.output_path)

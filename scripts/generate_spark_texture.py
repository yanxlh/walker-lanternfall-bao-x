#!/usr/bin/env python3
"""Generate a 3x3 white cross with binary alpha; no external image assets."""
from pathlib import Path
import struct
import zlib


def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def main():
    output = Path(__file__).resolve().parents[1] / 'godot/assets/particles/spark.png'
    rows = b''.join(b'\x00' + b''.join(bytes((255, 255, 255, 255 if x == 1 or y == 1 else 0)) for x in range(3)) for y in range(3))
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 3, 3, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')
    output.write_bytes(png)
    print(output)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Script to modify the ButtonDot (menu overlay button) position in Android .data files
Usage: ./modify_button_position.py <filename> <new_x> <new_y> [--index INDEX]
"""

import struct
import sys
import shutil
from pathlib import Path

def find_button_coordinates(data, button_name="ButtonDot"):
    """Find all ButtonDot coordinate locations in the file"""
    button_utf16 = f"Button{button_name[6:]}".encode('utf-16-le')
    positions = []

    # Scan entire file for coordinate patterns near the button name
    for offset in range(0x200, len(data) - 100, 4):
        try:
            coords = struct.unpack('<iiii', data[offset:offset+16])
            x, y, w, h = coords

            # Look for button-like coordinates
            if (0 <= x <= 2000 and -200 <= y <= 2000 and
                20 <= w <= 200 and 20 <= h <= 200):

                # Check if ButtonDot is nearby (within 1KB)
                context_start = max(0, offset - 200)
                context_end = min(len(data), offset + 1000)
                context = data[context_start:context_end]

                if b'B\x00u\x00t\x00t\x00o\x00n\x00D\x00o\x00t\x00' in context:
                    positions.append({
                        'offset': offset,
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h
                    })
        except:
            pass

    return positions

def modify_position(filename, new_x, new_y, index=0, backup=True):
    """
    Modify the ButtonDot position in a .data file

    Args:
        filename: Path to the .data file
        new_x: New X coordinate
        new_y: New Y coordinate
        index: Which ButtonDot instance to modify (default 0 = first one)
        backup: Whether to create a backup file (default True)
    """
    filepath = Path(filename)

    if not filepath.exists():
        print(f"Error: File '{filename}' not found")
        return False

    # Read the file
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())

    # Find all ButtonDot positions
    positions = find_button_coordinates(data)

    if not positions:
        print(f"Error: No ButtonDot found in '{filename}'")
        return False

    print(f"\nFound {len(positions)} ButtonDot position(s) in '{filename}':")
    for i, pos in enumerate(positions):
        print(f"  [{i}] Offset {hex(pos['offset'])}: "
              f"X={pos['x']}, Y={pos['y']}, W={pos['width']}, H={pos['height']}")

    if index >= len(positions):
        print(f"\nError: Index {index} out of range (0-{len(positions)-1})")
        return False

    selected = positions[index]
    print(f"\nModifying position [{index}] at offset {hex(selected['offset'])}")
    print(f"  Old position: X={selected['x']}, Y={selected['y']}")
    print(f"  New position: X={new_x}, Y={new_y}")

    # Create backup
    if backup:
        backup_path = filepath.with_suffix('.data.bak')
        shutil.copy2(filepath, backup_path)
        print(f"  Backup created: {backup_path}")

    # Modify the coordinates
    offset = selected['offset']
    struct.pack_into('<ii', data, offset, new_x, new_y)

    # Write the modified file
    with open(filepath, 'wb') as f:
        f.write(data)

    print(f"\n✓ Successfully modified '{filename}'")

    # Verify the change
    with open(filepath, 'rb') as f:
        verify_data = f.read()
    new_coords = struct.unpack('<iiii', verify_data[offset:offset+16])
    print(f"  Verified: X={new_coords[0]}, Y={new_coords[1]}, "
          f"W={new_coords[2]}, H={new_coords[3]}")

    return True

def list_positions(filename):
    """List all ButtonDot positions in a file"""
    filepath = Path(filename)

    if not filepath.exists():
        print(f"Error: File '{filename}' not found")
        return

    with open(filepath, 'rb') as f:
        data = f.read()

    positions = find_button_coordinates(data)

    if not positions:
        print(f"No ButtonDot found in '{filename}'")
        return

    print(f"\nButtonDot positions in '{filename}':")
    for i, pos in enumerate(positions):
        print(f"  [{i}] Offset {hex(pos['offset'])}: "
              f"X={pos['x']}, Y={pos['y']}, W={pos['width']}, H={pos['height']}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <filename> <new_x> <new_y> [--index INDEX] [--no-backup]")
        print(f"  {sys.argv[0]} <filename> --list")
        print("\nExamples:")
        print(f"  {sys.argv[0]} MirrorAndroid.data 100 100")
        print(f"  {sys.argv[0]} AndroidAuto.data 500 200 --index 0")
        print(f"  {sys.argv[0]} MirrorAndroid.data --list")
        sys.exit(1)

    filename = sys.argv[1]

    # List mode
    if '--list' in sys.argv or '-l' in sys.argv:
        list_positions(filename)
        return

    # Modify mode
    if len(sys.argv) < 4:
        print("Error: Not enough arguments")
        print(f"Usage: {sys.argv[0]} <filename> <new_x> <new_y> [--index INDEX]")
        sys.exit(1)

    try:
        new_x = int(sys.argv[2])
        new_y = int(sys.argv[3])
    except ValueError:
        print("Error: X and Y coordinates must be integers")
        sys.exit(1)

    # Parse optional arguments
    index = 0
    backup = True

    if '--index' in sys.argv:
        idx_pos = sys.argv.index('--index')
        if idx_pos + 1 < len(sys.argv):
            try:
                index = int(sys.argv[idx_pos + 1])
            except ValueError:
                print("Error: Index must be an integer")
                sys.exit(1)

    if '--no-backup' in sys.argv:
        backup = False

    # Perform modification
    success = modify_position(filename, new_x, new_y, index, backup)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

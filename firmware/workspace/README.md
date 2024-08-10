# Firmware RE Workspace

## unpack.sh
This script unpacks a `firmware.bin` file into .img partitions and expands the main MINFS filesystem.
```
Example: ./unpack.sh firmware.bin extracted/

Input 1: The firmware .bin file to unpack (e.g. "firmware.bin")
Input 2: The destination directory (e.g. "extracted")
```

## repack.sh
This script builds the filesystem and repacks the resulting .img partitions back into a `firmware.bin` file.
```
Example: ./repack.sh original.bin output.bin extracted/

Input 1: The original reference firmware.bin file to pack back into
Input 2: The name of the .bin to be created (e.g. "output.bin")
Input 3: The source directory containing the minfs filesystem and .img files to pack
```

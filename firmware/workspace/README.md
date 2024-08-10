# Workspace

## unpack.sh
```
Example: ./unpack.sh firmware.bin extracted/

Input 1: The firmware .bin file to unpack (e.g. "firmware.bin")
Input 2: The destination directory (e.g. "extracted")
```

## repack.sh
```
Example: ./repack.sh original.bin output.bin extracted/

Input 1: The original reference firmware.bin file to pack back into
Input 2: The name of the .bin to be created (e.g. "output.bin")
Input 3: The source directory containing the minfs filesystem and .img files to pack
```

# How-To: Repack the firmware

This tutorial explains how to re-pack an unpacked or modified filesystem back into a `firmware.bin` file ready for flashing to the device.

## Instructions

Repacking the MINFS filesystem and unpacked .img files back into a .bin is simple. 

First place a copy of the unmodified, original `firmware.bin` in the `workspace` folder. This will be used by the script as a base. 

Next, run the `repack.sh` script, specifying the output file name and source directory containing your .img files and minfs filesystem like so:
```bash
# ./repack.sh [path/to/original/firmware.bin] [output.bin] [path/to/source/]
➜  ~ ./repack.sh firmware.bin output.bin extracted/
```
Expected output:
```
Section 1
    offset 0
    size 3112
    recsize 451
    recunpacksize 3112
    compressed 2
...
Section 2
    offset 2800
    size 120
    recsize 120
    recunpacksize 120
    compressed 0
Section 3
    offset 2920
    size 0
    recsize 0
    recunpacksize 0
    compressed 0
Section 5
    offset 2920
    size 80
    recsize 80
    recunpacksize 80
    compressed 0
-------------------------------------------------------------
make minfs image file [/b5300-reverse-engineering/firmware/workspace/minfs.img] succeeded
image config size  : [14614528]
image used   size  : [11234212]
DEntry count       : [     187]
DEntry length      : [   16860]
FData  length      : [11216804]
-------------------------------------------------------------
Attached GPT image to /dev/disk6
Embedding MINFS volume to gpt.img
Removing temporary minfs.img
Detaching /dev/disk6
"disk6" ejected.
Embedding GPT image to output.bin
```

The script will produce a new `output.bin` file containing your [modified partitions](./2-unpacking-firmware.md#structure-overview). You are now ready to [flash it to your device](./4-flashing-firmware.md).

### Explanation

The script first uses the minfs tool to make the MINFS filesystem (minfs.img). Next the script uses hdiutil to attach the gpt.img partition. The minfs.img image is then embedded into the GPT disk overwriting the previous. Finally, the new gpt.img is embedded in a duplicate of the original firmware.bin to produce the modified output.bin.

Note: Currently, `repack.sh` only supports modifying the minfs.img filesystem. If you wish to modify the FAT.img, you will need to slightly modify `repack.sh` to embed fat.img in partition s3 instead.

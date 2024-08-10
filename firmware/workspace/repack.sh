#!/usr/bin/env bash
set -e

if [ -z "$3" ]
then
    echo "Usage: ./repack.sh [original.bin] [output.bin] [source_directory]"
    exit 1
fi

../bin/minfs make $3/minfs minfs.img $3/minfs/rootfs_ini.tmp
cp "$1" "$2"

DISKNAME=`hdiutil attach "$3/gpt.img" -nomount | grep "GUID_partition_scheme" | cut -d' ' -f1`
echo "Attached GPT image to $DISKNAME"

echo "Embedding MINFS volume to gpt.img"
dd if="minfs.img" of="${DISKNAME}s2" status=progress

echo "Removing temporary minfs.img"
rm minfs.img

echo "Detaching $DISKNAME"
hdiutil detach "$DISKNAME"

echo "Embedding GPT image to $2"
dd if="$3/gpt.img" of="$1" bs=1024 seek=48 status=progress conv=notrunc

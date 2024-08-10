# How-To: Unpack the firmware

This tutorial explains how to unpack a dumped `firmware.bin` and recover the embedded filesystem.

## Prerequisites

- firmware.bin: [example](../firmware/examples/B5300/original/)
- repo submodules (git clone --recursive)

## Instructions

### Setup

I've provided the prebuilt tools for extraction in `firmware/bin`. If you're happy to use these [skip to here](#extraction). However, if you'd prefer to build them yourself, make sure the submodules are initialised and run the makefile:
```bash
# Clone the repository with its submodules
➜  ~ git clone --recursive git@github.com:dan-os/b5300-reverse-engineering.git

# Run the makefile in the firmware folder
➜  ~ cd firmware/
➜  ~ make clean && make all
```

### Extraction

Place a copy of your `firmware.bin` in `firmware/workspace`. Next, simply run the extraction script:
```bash
➜  ~ ./unpack.sh firmware.bin extracted
```

If all goes well, the unpacked contents of the dump will appear in a new `extracted` folder and should look something like this:
```bash
├── 1.img      # operating system
├── fat.img    # user save data
├── gpt.img    # gpt partition
├── minfs      # unpacked filesystem (minfs.img)
│   ├── apps/
│   ├── etc/
│   ├── mod/
│   ├── res/
│   ├── rootfs_ini.tmp
│   └── startup.sh
└── minfs.img  # main filesystem

17 directories, 176 files
```

You're now free to modify the contents of the filesystem. Once you're ready, [continue to repacking and flashing](3-repacking-firmware.md) your modified firmware.

### Explanation

To unpack the bin, the script extracts the GPT image and attaches it using hdiutil. It then extracts each partiton (os volume, minfs image and FAT image) and saves them as a .img. Finally, the script uses the minfs tool to dump the contents of minfs.img to produce the main filesystem (minfs/).

## Structure Overview

### gpt.img

This is the GPT partition that contains all other partitions.

### 1.img

This partition contains the core Melis4.0 operating system data.

### minfs.img

This partition contains the built MINFS filesystem. This is where the application logic lies and so likely is of most interest to you.

### fat.img

This partition contains device save data such as the active start screen image, current Config.ini file, and various application state data.

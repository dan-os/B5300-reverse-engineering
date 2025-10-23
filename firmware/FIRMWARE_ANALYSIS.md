# B5300 Firmware Analysis

## Overview

This document provides a comprehensive analysis of the B5300 car infotainment system firmware. The device runs MELIS RTOS on an Allwinner F133/D1s RISC-V processor.

**Firmware Version**: HZ-BX-MIPI-F1026-FM-1.4SDK-20240712-0947
**OS Version**: MELIS RTOS F133-20220107
**Architecture**: RISC-V (32-bit with RVC and double-float ABI)
**Device Type**: Car Infotainment Head Unit

## Firmware Structure

The firmware consists of multiple partitions and file systems:

```
firmware/
├── 1.img                    # Boot partition (sunxi-package format)
├── fat.img                  # User configuration partition (FAT16)
├── gpt.img                  # GPT partition table
└── minfs.img               # Main root filesystem
```

## Quick Reference

- [Partition Overview](./docs/PARTITIONS.md)
- [Boot Partition (1.img)](./docs/BOOT_PARTITION.md)
- [Configuration Partition (fat.img)](./docs/FAT_PARTITION.md)
- [Root Filesystem (minfs)](./docs/MINFS_PARTITION.md)
- [Hardware Configuration](./docs/HARDWARE_CONFIG.md)
- [Security Notes](./docs/SECURITY.md)

## Key Findings

### Device Capabilities

- **Display**: 1280x480 MIPI LCD (rotated 90°)
- **Connectivity**:
  - Apple CarPlay
  - Android Auto
  - Huawei HiCar
  - Bluetooth (Audio & Hands-free)
  - WiFi
- **Media**:
  - FM/AM Radio
  - Audio/Video/Photo Player
  - DVD Player support
- **Camera**: Front/Rear camera with DVR recording
- **Touchscreen**: Capacitive (he0801a068 controller)

### Architecture Details

- **Bootloader**: OpenSBI (RISC-V Supervisor Binary Interface)
- **Kernel**: MELIS RTOS (Allwinner's proprietary RTOS)
- **Main Application**: ELF binary (init.axf) with modular architecture
- **Modules**: Loadable .mod files for features (CarPlay, WiFi, etc.)

### Security Concerns

⚠️ **Default credentials found in configuration files:**
- Logo Password: `112233`
- Factory Password: `113266`

See [Security Notes](./docs/SECURITY.md) for details.

## Directory Structure

```
workspace/
├── extracted/
│   ├── 1_img_extracted/          # Boot partition contents
│   │   ├── melis.bin             # RTOS kernel (3.2 MB)
│   │   ├── melis-config          # Hardware config (50 KB)
│   │   ├── melis-lzma            # Compressed kernel
│   │   └── extraction_summary.txt
│   │
│   ├── minfs/                    # Root filesystem
│   │   ├── apps/                 # Applications
│   │   ├── mod/                  # Kernel modules
│   │   ├── etc/                  # System config
│   │   ├── res/                  # Resources
│   │   ├── auto.mod              # Auto-load module
│   │   └── startup.sh            # Boot script
│   │
│   ├── fat.img                   # Config partition (FAT16)
│   ├── gpt.img                   # Partition table (GPT)
│   └── minfs.img                 # Filesystem image
│
├── F133-20220117_HZ-BX-MIPI-F1026-FM-1.4SDK-20240712-0947.bin
└── example_fw.bin
```

## Next Steps

1. **Disassemble RTOS Kernel**: Use RISC-V tools to analyze melis.bin
2. **Reverse Engineer Modules**: Analyze .mod files (CarPlay, WiFi, etc.)
3. **Parse UI Data Files**: Understand .data format in apps/Data/
4. **Analyze Init Application**: Disassemble init.axf to understand boot flow
5. **Hardware Interface Analysis**: Map GPIO pins and peripheral connections

## Tools Required

- **RISC-V Toolchain**: `riscv64-unknown-elf-objdump`, `riscv64-unknown-elf-gdb`
- **Binary Analysis**: Ghidra, IDA Pro, Binary Ninja (with RISC-V support)
- **Filesystem Tools**: 7z, mtools, mount
- **Image Analysis**: binwalk, strings, hexdump

## References

- [Allwinner F133 Datasheet](https://linux-sunxi.org/F133)
- [OpenSBI Documentation](https://github.com/riscv-software-src/opensbi)
- [MELIS RTOS GitHub](https://github.com/lindenis-org)

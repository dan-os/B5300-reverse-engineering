# Firmware Partitions Overview

## Partition Layout

The B5300 firmware uses a GPT (GUID Partition Table) layout with the following partitions:

| Partition | Name    | Size   | Type | Purpose                    |
|-----------|---------|--------|------|----------------------------|
| 1         | uboot   | ~3 MB  | Boot | Bootloader & RTOS kernel   |
| 2         | ROOTFS  | ~14 MB | Data | Root filesystem (minfs)    |
| 3         | UDISK   | ~1 MB  | Data | User data / config (FAT16) |

## Partition Details

### Partition 1: uboot (1.img)

**Format**: Allwinner sunxi-package format
**Compressed Size**: 1.5 MB (melis-lzma)
**Uncompressed Size**: 3.2 MB (melis.bin)
**Architecture**: RISC-V

Contains the boot components:
- OpenSBI bootloader
- MELIS RTOS kernel
- Hardware configuration database

See: [Boot Partition Documentation](./BOOT_PARTITION.md)

### Partition 2: ROOTFS (minfs.img)

**Format**: Custom MINFS filesystem
**Size**: 14 MB
**Mount Point**: `/`

Contains the complete root filesystem:
- Main application binary (init.axf)
- Loadable kernel modules (.mod files)
- UI resources and language files
- System libraries and utilities

See: [MINFS Documentation](./MINFS_PARTITION.md)

### Partition 3: UDISK (fat.img)

**Format**: FAT16 filesystem
**Size**: 512 KB (258 KB used)
**Mount Point**: `/mnt/udisk` or `F:`

Contains user-modifiable configuration:
- Runtime configuration files
- User settings and preferences
- Bluetooth pairing data
- Custom logos and UI themes

See: [FAT Partition Documentation](./FAT_PARTITION.md)

## Boot Sequence

1. **Hardware Reset** → SoC ROM bootloader
2. **ROM Bootloader** → Loads OpenSBI from Partition 1
3. **OpenSBI** → Initializes RISC-V supervisor mode
4. **MELIS Kernel** → Loads from melis.bin
5. **Kernel Init** → Parses melis-config for hardware setup
6. **Filesystem Mount** → Mounts ROOTFS (minfs)
7. **Startup Script** → Executes `/startup.sh`
8. **Module Loading** → Loads auto.mod and desktop.mod
9. **Init Application** → Launches `/apps/init.axf`
10. **User Interface** → Application starts UI framework

## Partition Table (GPT)

```
GPT Header:
  Signature: "EFI PART"
  Revision: 1.0
  Header Size: 92 bytes (0x5C)
  Disk GUID: 88386fab-9a56-2649-9668-80941dcb40bc
  First Usable LBA: 0x20 (sector 32)
  Last Usable LBA: 0x7FFF (sector 32767)
```

### Partition Entry 1 (uboot)
```
Type GUID: a2a0d0eb-e5b9-3344-87c0-68b6b72699c7
Unique GUID: 46550880-6641-4a74-a353-fca9272b8e45
First LBA: 0x20 (32)
Last LBA: 0x0C1F (3103)
Size: ~1.5 MB
Name: uboot (UTF-16LE)
```

### Partition Entry 2 (ROOTFS)
```
Type GUID: a2a0d0eb-e5b9-3344-87c0-68b6b72699c7
Unique GUID: 46550880-6641-4a74-a353-fca9272b8e46
First LBA: 0x0C20 (3104)
Last LBA: 0x7B9F (31647)
Size: ~14 MB
Name: ROOTFS (UTF-16LE)
```

### Partition Entry 3 (UDISK)
```
Type GUID: a2a0d0eb-e5b9-3344-87c0-68b6b72699c7
Unique GUID: 46550880-6641-4a74-a353-fca9272b8e47
First LBA: 0x7BA0 (31648)
Last LBA: 0x7F9F (32671)
Size: ~512 KB
Name: UDISK (UTF-16LE)
```

## Filesystem Types

### MINFS (Custom)
- Proprietary filesystem used by MELIS RTOS
- Similar to ROMFS (read-only at runtime)
- Optimized for embedded systems
- Direct memory mapping support

### FAT16
- Standard Microsoft FAT16
- Read/write at runtime
- Used for user-configurable data
- Compatible with standard tools

### Sunxi-Package
- Allwinner proprietary boot format
- Contains metadata and checksums
- Supports compression (LZMA)
- Version signature: "CHKv1.0"

## Memory Map

Typical runtime memory layout:

```
0x40000000 - 0x50000000   DDR RAM (256 MB typical)
  0x40000000              MELIS kernel base
  0x40XXXXXX              Loaded modules
  0x4XXXXXXX              Application heap
  0x4XXXXXXX              Stack region

0xE9100000                Mapped MINFS base (from partition 2)
0xFFFFFFFF                End of address space
```

## Extraction Commands

### Extract GPT Partitions
```bash
# Extract partition 1 (uboot)
dd if=gpt.img of=1.img bs=512 skip=32 count=3072

# Extract partition 2 (rootfs)
dd if=gpt.img of=minfs.img bs=512 skip=3104 count=28544

# Extract partition 3 (udisk)
dd if=gpt.img of=fat.img bs=512 skip=31648 count=1024
```

### Extract Sunxi Package (1.img)
```bash
# Custom tool required or manual extraction
# Format: Header + Section Table + Data Sections
```

### Mount FAT Partition
```bash
# Linux
mount -t vfat -o loop fat.img /mnt/fat

# macOS
hdiutil attach fat.img

# Windows
7z x fat.img
```

### Extract MINFS (Requires custom tool or minfs driver)
```bash
# Tool from: https://github.com/lindenis-org/minfs-tools
# Or use binwalk for extraction
```

## Notes

- All partitions use 512-byte sectors
- GPT backup table located at end of disk
- Partition UUIDs are consistent across devices (may be factory default)
- MINFS partition is typically read-only after manufacturing
- FAT partition is read/write for runtime configuration changes

# B5300 Firmware Documentation Index

Complete reverse engineering documentation for the B5300 car infotainment system.

## Main Documentation

| Document | Size | Description |
|----------|------|-------------|
| [FIRMWARE_ANALYSIS.md](./FIRMWARE_ANALYSIS.md) | Overview | Main entry point with firmware structure and quick reference |
| [docs/PARTITIONS.md](./docs/PARTITIONS.md) | ~8 KB | Complete partition layout, GPT structure, boot sequence |
| [docs/BOOT_PARTITION.md](./docs/BOOT_PARTITION.md) | ~40 KB | Boot partition analysis: melis.bin, melis-config, OpenSBI |
| [docs/FAT_PARTITION.md](./docs/FAT_PARTITION.md) | ~25 KB | FAT partition: Config.ini (300+ params), user data, Bluetooth |
| [docs/MINFS_PARTITION.md](./docs/MINFS_PARTITION.md) | ~45 KB | Root filesystem: init.axf, 18+ modules, UI resources |
| [docs/HARDWARE_CONFIG.md](./docs/HARDWARE_CONFIG.md) | ~35 KB | Complete hardware specs: SoC, peripherals, GPIO, power |
| [docs/SECURITY.md](./docs/SECURITY.md) | ~25 KB | Security analysis: 14 vulnerabilities with mitigations |

**Total Documentation**: ~180 KB, ~75,000 words

## Quick Navigation

### By Topic

**Getting Started**:
- [Main Overview](./FIRMWARE_ANALYSIS.md) - Start here
- [Partition Structure](./docs/PARTITIONS.md) - Understanding firmware layout
- [Boot Process](./docs/BOOT_PARTITION.md#boot-process) - How the device boots

**Hardware**:
- [SoC Specifications](./docs/HARDWARE_CONFIG.md#soc-specifications) - Allwinner F133 RISC-V
- [Memory Configuration](./docs/HARDWARE_CONFIG.md#memory-configuration) - DDR3 setup
- [Power Management](./docs/HARDWARE_CONFIG.md#power-management) - PMU, regulators, DVFS
- [Display System](./docs/HARDWARE_CONFIG.md#display-subsystem) - MIPI LCD, backlight
- [Camera Interface](./docs/HARDWARE_CONFIG.md#cameravideo-input) - Dual camera, CSI
- [Audio Subsystem](./docs/HARDWARE_CONFIG.md#audio-subsystem) - Codec, routing
- [Connectivity](./docs/HARDWARE_CONFIG.md#connectivity) - WiFi, BT, Ethernet
- [GPIO Mapping](./docs/HARDWARE_CONFIG.md#gpio-summary) - Pin assignments

**Software**:
- [MELIS Kernel](./docs/BOOT_PARTITION.md#melisbin-rtos-kernel) - OS kernel analysis
- [Hardware Config](./docs/BOOT_PARTITION.md#melis-config-hardware-configuration) - 102 config sections
- [Main Application](./docs/MINFS_PARTITION.md#initaxf) - init.axf (2 MB ELF)
- [Kernel Modules](./docs/MINFS_PARTITION.md#kernel-modules-directory-mod) - 18+ modules
- [UI System](./docs/MINFS_PARTITION.md#ui-data-files-appsdata) - 50+ .data files
- [Configuration](./docs/FAT_PARTITION.md#configini) - Runtime settings

**Security**:
- [Vulnerability Summary](./docs/SECURITY.md#critical-vulnerabilities) - 14 issues
- [Hardcoded Passwords](./docs/SECURITY.md#1-hardcoded-default-credentials) - CVSS 9.8
- [No Secure Boot](./docs/SECURITY.md#2-no-secure-boot-implementation) - CVSS 9.1
- [Unencrypted Storage](./docs/SECURITY.md#3-unencrypted-storage) - CVSS 8.2
- [Security Recommendations](./docs/SECURITY.md#recommended-security-improvements)

### By Component

**Boot Partition (1.img)**:
- [Overview](./docs/BOOT_PARTITION.md#overview)
- [melis.bin Structure](./docs/BOOT_PARTITION.md#melisbin-rtos-kernel)
- [melis-config Sections](./docs/BOOT_PARTITION.md#configuration-sections)
- [Boot Process](./docs/BOOT_PARTITION.md#boot-process)

**FAT Partition (fat.img)**:
- [Overview](./docs/FAT_PARTITION.md#overview)
- [Config.ini Parameters](./docs/FAT_PARTITION.md#configini)
- [User Data](./docs/FAT_PARTITION.md#save-directory)
- [Bluetooth Pairing](./docs/FAT_PARTITION.md#bt-directory)

**MINFS Partition (minfs.img)**:
- [Overview](./docs/MINFS_PARTITION.md#overview)
- [Applications](./docs/MINFS_PARTITION.md#applications-directory-apps)
- [Kernel Modules](./docs/MINFS_PARTITION.md#kernel-modules-directory-mod)
- [UI Resources](./docs/MINFS_PARTITION.md#ui-data-files-appsdata)

## By File Type

### Binaries
- [melis.bin](./docs/BOOT_PARTITION.md#melisbin-rtos-kernel) - RTOS kernel (3.2 MB)
- [init.axf](./docs/MINFS_PARTITION.md#initaxf) - Main app (2.0 MB)
- [auto.mod](./docs/MINFS_PARTITION.md#automod) - Module loader (900 KB)
- [carplay.mod](./docs/MINFS_PARTITION.md#carplaymod) - CarPlay (852 KB)
- [wireless.mod](./docs/MINFS_PARTITION.md#wirelessmod) - WiFi/BT (2.2 MB)

### Configuration
- [melis-config](./docs/BOOT_PARTITION.md#melis-config-hardware-configuration) - HW config (50 KB)
- [Config.ini](./docs/FAT_PARTITION.md#configini) - Runtime config (4 KB)
- [startup.sh](./docs/MINFS_PARTITION.md#startupsh) - Boot script

### Resources
- [Font30_8Bit.vft](./docs/MINFS_PARTITION.md#font30_8bitvft) - Vector font (2.5 MB)
- [Language files](./docs/MINFS_PARTITION.md#language-files-appslanguage) - Translations
- [UI .data files](./docs/MINFS_PARTITION.md#ui-data-files-appsdata) - UI layouts

## Key Information Quick Reference

### Firmware Details
```
SDK Version: HZ-BX-MIPI-F1026-FM-1.4SDK-20240712-0947
OS Version: MELIS RTOS F133-20220107
Architecture: RISC-V RV32IMAFDC
SoC: Allwinner F133
Total Size: ~32 MB
```

### Default Credentials
```
Logo Password: 112233
Factory Password: 113266
Bluetooth Name: SWL-BT
```

### Debug Access
```
UART0: /dev/ttyS0 @ 115200 baud (PA2/PA3)
JTAG: Enabled (configurable)
```

### Memory Map
```
0x40000000 - MELIS kernel base
0xE9100000 - init.axf application base
0xF0000000 - Peripheral registers
```

### Key GPIO
```
LCD Reset: lcd_gpio_0
Touch Int: ctp_int
Camera Reset: sensor0_reset
Radio Reset: GPIO_403
```

## Analysis Workflow

### Step 1: Extract Firmware
```bash
# See: docs/PARTITIONS.md#extraction-commands
binwalk -e firmware.bin
# Or use provided scripts
./unpack-linux.sh
```

### Step 2: Analyze Boot
```bash
# See: docs/BOOT_PARTITION.md#analysis-tools
hexdump -C melis.bin | head
strings melis.bin | grep -i "opensbi"
riscv64-unknown-elf-objdump -m riscv:rv32 -b binary -D melis.bin
```

### Step 3: Parse Configuration
```bash
# See: docs/BOOT_PARTITION.md#parsing-the-configuration
python3 parse_melis_config.py melis-config
```

### Step 4: Explore Filesystem
```bash
# See: docs/MINFS_PARTITION.md#extraction-and-analysis
ls -lR minfs/
file minfs/apps/init.axf
strings minfs/mod/carplay.mod
```

### Step 5: Disassemble Binaries
```bash
# See: docs/MINFS_PARTITION.md#analyze-initaxf
riscv64-unknown-elf-objdump -d init.axf > init.asm
# Or use Ghidra with RISC-V support
```

### Step 6: Review Security
```bash
# See: docs/SECURITY.md
grep -i "password" Config.ini
checksec init.axf
```

## Tools Required

### Essential
- RISC-V toolchain (`gcc-riscv64-unknown-elf`)
- 7-Zip (`p7zip-full`)
- Binwalk
- Ghidra or IDA Pro

### Optional
- Binary Ninja
- radare2
- Python 3 (for parsing scripts)
- mtools (FAT manipulation)

See [FIRMWARE_ANALYSIS.md](./FIRMWARE_ANALYSIS.md#tools-required) for installation commands.

## Documentation Statistics

### Coverage
- ✅ Partition structure: 100%
- ✅ Boot process: 100%
- ✅ Hardware config: 95%
- ✅ Software components: 90%
- ✅ Security assessment: 100%
- 🔄 Protocol analysis: 40%
- 🔄 UI format: 60%
- 📋 Module APIs: 20%

### Sections Documented
- Boot partition: 2 major components
- Hardware config: 102 sections
- FAT config: 300+ parameters
- MINFS: 18+ modules, 50+ UI files
- Security: 14 vulnerabilities

## Contributing

Found something new? Want to add documentation?

1. Document your findings clearly
2. Include evidence (hex dumps, disassembly, etc.)
3. Cross-reference existing docs
4. Follow the established format
5. Submit a pull request

## Version History

| Version | Date | Changes | Documents |
|---------|------|---------|-----------|
| 1.0 | Jan 2025 | Initial release | All 7 documents |

## License

This documentation is provided for educational and research purposes.

## Acknowledgments

- Allwinner for RISC-V SoC
- Linux-Sunxi community
- RISC-V International
- Open-source reverse engineering community

---

**Documentation Index Last Updated**: January 2025

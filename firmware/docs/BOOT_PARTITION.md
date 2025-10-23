# Boot Partition (1.img) Documentation

## Overview

The boot partition contains the MELIS RTOS kernel and hardware configuration. It uses Allwinner's proprietary sunxi-package format.

**Location**: Partition 1 of gpt.img
**Format**: Sunxi-package (Allwinner proprietary)
**Compressed Size**: 1,485,866 bytes (~1.5 MB)
**Uncompressed Size**: 3,325,912 bytes (~3.2 MB)

## Contents

```
1.img (sunxi-package)
├── melis-lzma          # LZMA compressed kernel (1.5 MB)
└── melis-config        # Hardware configuration (50 KB)
```

When extracted:
```
1_img_extracted/
├── melis.bin           # Decompressed RTOS kernel (3.2 MB)
├── melis-lzma          # Compressed kernel
├── melis-lzma.lzma     # Copy of compressed kernel
├── melis-config        # Hardware configuration
└── extraction_summary.txt
```

## File Details

### melis.bin (RTOS Kernel)

**Type**: RISC-V binary firmware
**Size**: 3,325,912 bytes (3.2 MB)
**Architecture**: RISC-V 32-bit (RV32IMAFDC)
**Format**: Raw binary (not ELF)

#### Structure

| Offset    | Size    | Component                          |
|-----------|---------|-----------------------------------|
| 0x0000    | ~1 KB   | OpenSBI header and signature      |
| 0x0400    | ~3 MB   | MELIS RTOS kernel code            |
| Variable  | -       | Embedded resources and data       |

#### Header Analysis

```
Offset 0x0000:
  6f 00 00 40 6f 70 65 6e  73 62 69 00 00 00 00 00
  |o..@opensbi.........|

Offset 0x001C:
  43 48 4b 76 31 2e 30 00  00 00 00 00 00 00 00 40
  |CHKv1.0............@|

  Signature: "CHKv1.0" (Checksum version 1.0)
  Magic offset: 0x40 (indicates data start)
```

#### Key Components

1. **OpenSBI Bootloader** (0x0000-0x03FF)
   - RISC-V Supervisor Binary Interface
   - Provides M-mode runtime services
   - Initializes hardware before OS boot
   - Standard interface for RISC-V OS booting

2. **MELIS Kernel Code** (0x0400+)
   - RTOS scheduler and task management
   - Device drivers for Allwinner F133 peripherals
   - Memory management unit (MMU) configuration
   - Interrupt handlers and exception vectors
   - System call interface

3. **Embedded Data**
   - Default device tree or hardware tables
   - Built-in fonts or resources
   - Error messages and debug strings

#### RISC-V Instruction Examples

```assembly
# Sample from offset 0x400
0x0400:  33 04 05 00    add   s0, a0, zero     # Register operations
0x0404:  b3 84 05 00    add   s1, a1, zero
0x0408:  33 09 06 00    add   s2, a2, zero
0x040C:  ef 00 c0 5f    jal   ra, 0x5fc0       # Function call
```

#### Analysis Tools

```bash
# Disassemble with RISC-V toolchain
riscv64-unknown-elf-objdump -m riscv:rv32 -b binary \
  --adjust-vma=0x40000000 -D melis.bin > melis.asm

# Load in Ghidra
- Processor: RISCV
- Variant: RV32GC
- Endianness: Little
- Base address: 0x40000000

# Extract strings
strings -n 8 melis.bin > melis_strings.txt

# Analyze with binwalk
binwalk melis.bin
```

### melis-config (Hardware Configuration)

**Type**: Binary configuration database
**Size**: 51,200 bytes (50 KB)
**Format**: Custom binary structure with named sections

#### Structure

```
Header (16 bytes):
  0x00000000: 66 00 00 00    Section count or magic (102)
  0x00000004: 00 C8 00 00    Total size (51,200 bytes)
  0x00000008: 01 00 00 00    Version or flags
  0x0000000C: 02 00 00 00    Format identifier

Section Directory (48 bytes per entry):
  Offset 0x10+: Section entries

  Entry format:
    0x00-0x1F: Section name (32 bytes, null-terminated ASCII)
    0x20-0x23: Type/flags (4 bytes)
    0x24-0x27: Data offset (4 bytes)
    0x28-0x2B: Data size (4 bytes)
    0x2C-0x2F: Reserved (4 bytes)
```

#### Configuration Sections

The file contains 102 configuration sections organized by subsystem:

##### Boot Configuration (8 sections)
- `product` - Product identification strings
- `platform` - Platform/SoC information
- `target` - Target board configuration
- `card_boot` - SD card boot parameters
- `card0_boot_para` - SD card 0 detailed config
- `card2_boot_para` - SD card 2 detailed config
- `boot_clock` - Boot clock frequencies
- `storage_type` - Boot storage device type

##### Power Management (12 sections)
- `power_sply` - Power supply configuration
- `pm_para` - Power management parameters
- `pmu1_para` - PMU chip 1 configuration
- `pmu2_para` - PMU chip 2 configuration (if present)
- `pmu1_regu` - PMU voltage regulators
- `dcdc1_vol` through `dcdc5_vol` - DC-DC converter voltages
- `aldo2_vol`, `aldo3_vol` - LDO voltages

**PMU Configuration Details:**
```
PMU Chip: AXP28 series (Allwinner X-Powers)
Regulators:
  - DCDC1-7: Main power rails
  - ALDO1-3: Analog LDOs
  - DLDO1-4: Digital LDOs
  - ELDO1-3: External LDOs
  - FLDO1-2: Fixed LDOs
  - GPIO0/1 LDOs: GPIO-controlled
```

##### Memory Configuration (6 sections)
- `dram_para` - DDR RAM parameters (24 parameters)
  - `dram_clk` - RAM frequency
  - `dram_type` - DDR3/DDR4/LPDDR3
  - `dram_zq` - ZQ calibration
  - `dram_odt_en` - On-die termination
  - `dram_para1/2` - Timing parameters
  - `dram_mr0-3` - Mode registers
  - `dram_tpr0-13` - Timing parameter registers
- `clock` - System clock tree (5 PLLs)
  - `pll4`, `pll6`, `pll8`, `pll9`, `pll10`
- `dvfs_table` - Dynamic voltage/frequency scaling

##### Display Subsystem (15 sections)
- `disp` - Display initialization (23 parameters)
  - `disp_init_enable` - Enable display init
  - `disp_mode` - Display mode selection
  - `screen0_output_type` - Primary screen type
  - `screen0_output_mode` - Resolution/refresh rate
  - `fb0_format`, `fb0_width`, `fb0_height` - Framebuffer config
- `lcd0` - LCD panel configuration (70+ parameters)
  - `lcd_driver_name` - Driver name string
  - `lcd_if` - Interface type (MIPI DSI/RGB/LVDS)
  - `lcd_x`, `lcd_y` - Resolution
  - `lcd_dclk_freq` - Pixel clock
  - `lcd_pwm_*` - Backlight PWM settings
  - `lcd_hbp`, `lcd_ht`, `lcd_hspw` - Horizontal timing
  - `lcd_vbp`, `lcd_vt`, `lcd_vspw` - Vertical timing
  - `lcd_dsi_*` - MIPI DSI parameters
  - `lcd_gpio_0` through `lcd_gpio_9` - Control GPIOs
- `hdmi` - HDMI output configuration
- `mipi_reg` - MIPI register values (25 registers)
- `vdpo0` - Video DAC output
- `pwm0-7` - PWM channels for backlight
- `spwm0` - Special PWM configuration
- `vcom` - LCD VCOM voltage

##### Camera/Video Input (14 sections)
- `vind0` - Video input subsystem
- `vind0/csi0` - Camera serial interface
- `vind0/sensor0` - Primary camera (20 parameters)
  - Model detected: OV5647 (rear camera)
  - Resolution support
  - Power rail configuration
- `vind0/sensor1` - Secondary camera (front)
- `vind0/flash0` - Camera flash/LED
- `vind0/actuator0` - Autofocus motor (AD5820)
- `vind0/vinc0-3` - Video input channels

##### Serial Communication (13 sections)
- `uart0` through `uart4` - UART configuration
  - `uart_debug_port` - Debug UART selection
  - `uart_debug_baudrate` - Baud rate (115200)
  - `uart_debug_tx/rx` - TX/RX GPIO pins
- `twi0` through `twi3` - I2C/TWI buses
  - `twi_port` - Bus number
  - `twi_scl`, `twi_sda` - GPIO assignments
- `spi0` - SPI bus configuration
  - `spi0_sclk`, `spi0_cs`, `spi0_mosi`, `spi0_miso`
  - `spi0_wp`, `spi0_hold` - Quad SPI pins
- `s_uart0` - Secure UART
- `s_rsb0` - Reduced Serial Bus (RSB)

##### Storage Configuration (10 sections)
- `spinor_para` - SPI NOR flash parameters
- `nand0_para` - NAND flash configuration (40+ parameters)
- `sdcard_global` - Global SD card settings
- `sdc0`, `sdc1` - SD/MMC controllers
  - `bus-width` - 1/4/8-bit mode
  - `card_high_speed` - High-speed mode
  - `sdc_d0-7`, `sdc_clk`, `sdc_cmd` - Pin assignments
  - `sdc_emmc_rst`, `sdc_ds` - eMMC specific
- `mmc0_para` through `mmc3_para` - MMC parameters

##### USB Configuration (9 sections)
- `usbc0`, `usbc1`, `usbc2` - USB controllers
  - `usb_port_type` - Host/Device/OTG
  - `usb_detect_type` - Detection method
  - `usb_id_gpio` - USB ID pin
  - `usb_drv_vbus_gpio` - VBUS control
  - `usb_speed_mode` - High-speed/Full-speed
- `usb_feature` - USB device features
  - `vendor_id`, `mass_storage_id`, `adb_id`
  - `manufacturer_name` - "USB Developer"
  - `product_name` - "Android"
  - `serial_number` - "20080411"
- `msc_feature` - Mass storage configuration
- `serial_feature` - USB serial configuration

##### Audio Configuration (4 sections)
- `sndcodec` - Audio codec chip
- `cpudai` - CPU digital audio interface
- `codec` - Codec detailed settings (12 parameters)
  - `digital_vol`, `lineout_vol` - Volume levels
  - `mic1gain`, `mic2gain`, `mic3gain` - Mic gains
  - `adcgain` - ADC gain
  - `adcdrc_cfg`, `dacdrc_cfg` - DRC settings
  - `pa_ctl_level` - PA control
  - `gpio-spk` - Speaker GPIO
- `s_cir0` - Secure infrared remote

##### Network Configuration (4 sections)
- `gmac0` - Gigabit Ethernet MAC
  - `phy-mode` - "rgmii" (RGMII interface)
  - Pin assignments (24 pins)
  - `tx-delay`, `rx-delay` - RGMII delays
- `wifi_para` - WiFi module configuration
- `bt_para` - Bluetooth configuration
- `3g_para` - 3G modem configuration

##### Input Devices (7 sections)
- `ctp_para` - Capacitive touchscreen (14 parameters)
  - Controller: he0801a068
  - `ctp_screen_max_x`, `ctp_screen_max_y`
  - `ctp_int_port`, `ctp_wakeup` - Interrupt GPIO
- `rtp_para` - Resistive touchscreen
- `tkey_para` - Touch key/button
- `gpadc` - General purpose ADC (for buttons)
  - Channel configuration
  - Key voltage thresholds
- `ir_code` - Infrared remote codes

##### Sensors (4 sections)
- `gsensor_para` - Accelerometer/G-sensor
- `gps_para` - GPS module
- `compass_para` - Magnetometer/compass
- `gy_para` - Gyroscope

##### JTAG Debug (1 section)
- `jtag_para` - JTAG debug interface
  - `jtag_enable` - Enable flag
  - `jtag_ms`, `jtag_ck`, `jtag_do`, `jtag_di` - JTAG pins
- `s_jtag0` - Secure JTAG

##### Application Configuration (5 sections)
- `app_para` - Application parameters
- `backlayer` - Background layer config
- `version` - Version strings
- `machine` - Machine type identifier
- `Vdevice` - Virtual device configuration

##### Miscellaneous (10 sections)
- `tvout_para`, `tvin_para` - TV input/output
- `motor_para` - Motor control (for DVD or camera)
- `mixture_para` - Mixed signal configuration
- `adc_power` - ADC power configuration
- `eraseflag` - Erase flag for factory reset
- `debug_mode` - Debug mode enable
- `standby_mode` - Standby/sleep configuration

#### Parsing the Configuration

```python
import struct

def parse_melis_config(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # Parse header
    magic = struct.unpack('<I', data[0:4])[0]
    total_size = struct.unpack('<I', data[4:8])[0]

    print(f"Magic: 0x{magic:08x}")
    print(f"Total Size: {total_size} bytes")

    # Parse section directory
    offset = 0x10
    sections = []

    while offset < len(data):
        # Section name (32 bytes)
        name_bytes = data[offset:offset+32]
        name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')

        if not name:
            break

        # Section metadata
        type_val = struct.unpack('<I', data[offset+32:offset+36])[0]
        data_offset = struct.unpack('<I', data[offset+36:offset+40])[0]

        sections.append({
            'name': name,
            'type': type_val,
            'offset': data_offset
        })

        print(f"{name:30s} @ 0x{data_offset:08x}")

        offset += 48

    return sections

# Usage
sections = parse_melis_config('melis-config')
```

#### GPIO Pin Mapping Examples

From configuration analysis:

```
UART0 (Debug Console):
  TX: GPIO_PA2
  RX: GPIO_PA3
  Baud: 115200

LCD MIPI Interface:
  Reset: lcd_gpio_0
  Power: lcd_gpio_1
  Backlight Enable: lcd_gpio_2
  PWM Backlight: pwm6

Touch Screen:
  Interrupt: GPIO (from ctp_int_port)
  Reset/Wakeup: GPIO (from ctp_wakeup)

Camera:
  Sensor0 Reset: sensor0_reset GPIO
  Sensor0 Power Down: sensor0_pwdn GPIO
  Flash Enable: flash0_en GPIO

Radio:
  Reset: GPIO_403 (radioResetGpio)

SD Card:
  Detect: sdc_det GPIO
  Data 0-3: sdc_d0 through sdc_d3
  Clock: sdc_clk
  Command: sdc_cmd
```

## Boot Process

1. **Hardware Reset**
   - SoC internal ROM bootloader executes
   - Searches for boot media (SD/SPI/NAND)

2. **Boot Media Located**
   - ROM loads first partition (1.img) from boot0 location
   - Verifies "CHKv1.0" signature

3. **Decompress Kernel**
   - LZMA decompression of melis-lzma → melis.bin
   - Decompressed to DDR RAM at base address 0x40000000

4. **OpenSBI Initialization**
   - OpenSBI (offset 0x0) begins execution
   - Initializes M-mode (machine mode)
   - Sets up timers, interrupts, and CSRs
   - Configures memory protection

5. **Hardware Configuration**
   - Parses melis-config sections
   - Configures clocks (PLLs)
   - Initializes DRAM controller
   - Sets up power management (PMU)

6. **Device Initialization**
   - Initializes peripherals based on config:
     - UART (debug console at 115200 baud)
     - Display (MIPI LCD initialization)
     - Storage (SD/SPI/NAND)
     - USB controllers
     - Network (WiFi/BT/Ethernet)

7. **MELIS Kernel Start**
   - Jumps to kernel entry point (offset 0x400)
   - RTOS scheduler initialization
   - Creates system threads
   - Mounts root filesystem (MINFS)

8. **User Space Transition**
   - Executes /startup.sh
   - Loads kernel modules from /mod/
   - Launches /apps/init.axf

## Firmware Updates

The boot partition can be updated by:

1. **Via UDISK partition**
   - Copy new firmware to FAT partition
   - Trigger update flag in configuration
   - Reboot initiates update process

2. **Via USB/UART**
   - Phoenix Suite (Allwinner tool)
   - LiveSuit (Linux alternative)
   - Custom update protocol

3. **Via OTA (if supported)**
   - Download firmware package
   - Verify signature/checksum
   - Write to inactive partition (A/B scheme)
   - Reboot to new partition

## Security Considerations

⚠️ **Security Notes:**

1. **No Secure Boot** - No signature verification detected
2. **Unencrypted** - Kernel and config are plaintext
3. **JTAG Enabled** - Debug interface may be accessible
4. **Known Checksums** - "CHKv1.0" simple checksum scheme

## Backup and Restoration

```bash
# Backup boot partition
dd if=/dev/mmcblk0p1 of=boot_backup.img bs=512

# Restore boot partition (DANGEROUS!)
dd if=boot_backup.img of=/dev/mmcblk0p1 bs=512
```

## References

- OpenSBI: https://github.com/riscv-software-src/opensbi
- Allwinner Boot Process: https://linux-sunxi.org/Boot_Process
- MELIS RTOS: https://github.com/lindenis-org/lindenis-v833-RTOS-melis-4.0

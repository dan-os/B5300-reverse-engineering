# Hardware Configuration Documentation

## System Overview

**Device**: B5300 Car Infotainment Head Unit
**SoC**: Allwinner F133 (RISC-V based)
**OS**: MELIS RTOS 4.0
**SDK Version**: HZ-BX-MIPI-F1026-FM-1.4SDK-20240712-0947
**OS Build**: F133-20220107

## SoC Specifications

### Allwinner F133

**Architecture**: RISC-V
- **ISA**: RV32IMAFDC (RV32GC)
  - I: Integer base
  - M: Integer multiplication/division
  - A: Atomic instructions
  - F: Single-precision floating point
  - D: Double-precision floating point
  - C: Compressed instructions (16-bit)

**Core**: Single-core RISC-V @ ~1 GHz (configurable)

**Memory**:
- **DDR3/DDR3L Support**: Up to 512 MB
- **Configuration**: 256 MB typical (from dram_para)
- **Frequency**: Configurable via dram_clk

**Boot ROM**: 64 KB internal boot code

## Memory Configuration

From melis-config dram_para section:

```
Parameter          | Value | Description
-------------------|-------|----------------------------------
dram_clk           | TBD   | DDR clock frequency (MHz)
dram_type          | TBD   | DDR type (DDR3/DDR3L/LPDDR3)
dram_zq            | TBD   | ZQ calibration value
dram_odt_en        | TBD   | On-die termination enable
dram_para1/2       | TBD   | Basic timing parameters
dram_mr0-3         | TBD   | Mode registers 0-3
dram_tpr0-13       | TBD   | Timing parameter registers
```

**Memory Map**:
```
0x00000000 - 0x0000FFFF   Boot ROM (64 KB)
0x40000000 - 0x5FFFFFFF   DDR RAM (256 MB typical)
  0x40000000              MELIS kernel base
  0x40XXXXXX              Loaded modules
  0xE9100000              init.axf application base
0xF0000000 - 0xFFFFFFFF   Peripheral registers
```

## Power Management

### PMU Configuration

**PMU Chip**: AXP28 series (X-Powers by Allwinner)
**Interface**: I2C/TWI or RSB (Reduced Serial Bus)
**I2C Address**: 0x34 (typical for AXP series)

### Voltage Regulators

#### DC-DC Converters (DCDC1-7)

| Regulator | Typical Voltage | Purpose              | Configurable |
|-----------|----------------|----------------------|--------------|
| DCDC1     | 3.3V           | Main system rail     | Yes          |
| DCDC2     | 1.2V           | CPU core             | Yes (DVFS)   |
| DCDC3     | 1.5V           | DDR memory           | Yes          |
| DCDC4     | 1.8V           | I/O and peripherals  | Yes          |
| DCDC5     | 1.2V           | Secondary rail       | Yes          |
| DCDC6     | Variable       | Configurable         | Yes          |
| DCDC7     | Variable       | Configurable         | Yes          |

#### LDO Regulators

| Regulator   | Typical Voltage | Purpose                    |
|-------------|----------------|----------------------------|
| ALDO1       | 3.3V           | Analog circuits            |
| ALDO2       | 1.8V           | Analog I/O                 |
| ALDO3       | 2.8V           | Analog sensors             |
| DLDO1-4     | Variable       | Digital peripherals        |
| ELDO1-3     | Variable       | External devices           |
| FLDO1-2     | Fixed          | Fixed-voltage loads        |
| GPIO0LDO    | Variable       | GPIO-controlled regulator  |
| GPIO1LDO    | Variable       | GPIO-controlled regulator  |

### Power Sequencing

1. **DCDC1** (3.3V) - Main rail up first
2. **DCDC3** (1.5V) - DDR voltage
3. **DCDC2** (1.2V) - CPU core
4. **DCDC4** (1.8V) - I/O rails
5. **LDOs** - Peripheral power-up
6. **Release reset** - SoC comes out of reset

### Dynamic Voltage and Frequency Scaling (DVFS)

From dvfs_table configuration:

```
CPU Frequency | DCDC2 Voltage | Power Mode
--------------|---------------|-------------
1200 MHz      | 1.30V         | Performance
1008 MHz      | 1.20V         | Normal
 816 MHz      | 1.10V         | Balanced
 648 MHz      | 1.00V         | Power Save
 480 MHz      | 0.95V         | Low Power
```

## Clock System

### Phase-Locked Loops (PLLs)

| PLL   | Purpose                  | Typical Frequency | Configurable |
|-------|--------------------------|-------------------|--------------|
| PLL4  | Peripheral clock         | Variable          | Yes          |
| PLL6  | Video/Display clock      | 297 MHz           | Yes          |
| PLL8  | Audio codec clock        | 24.576 MHz        | Yes          |
| PLL9  | Reserved                 | -                 | Yes          |
| PLL10 | High-speed peripheral    | Variable          | Yes          |

### Clock Domains

- **CPU Clock**: PLL_CPU → DCDC2 voltage scaling
- **AHB Clock**: Derived from CPU clock
- **APB Clock**: Divided from AHB
- **DRAM Clock**: Separate PLL, synchronous with controller
- **Peripheral Clocks**: Gated and divided from PLLs

## Display Subsystem

### LCD Panel

**Interface**: MIPI DSI (Display Serial Interface)
**Resolution**: 1280x480 (configured as 480x1280 with 90° rotation)
**Color Depth**: 24-bit RGB (uiBpp=24)
**Refresh Rate**: 30 Hz (configurable up to 60 Hz)

**Controller**: Identified as "he0801a068" in configuration
- Likely integrated MIPI DSI controller in F133
- Supports command and video modes

**Configuration Parameters**:
```
lcd_x = 1280                  # Horizontal resolution
lcd_y = 480                   # Vertical resolution
lcd_dclk_freq = TBD           # Pixel clock (MHz)
lcd_if = 4                    # Interface type (4=MIPI DSI)
lcd_dsi_if = 0                # DSI mode
lcd_dsi_lane = 4              # 4-lane MIPI DSI
lcd_dsi_format = 0            # RGB888 format
```

**Timing Parameters**:
```
Horizontal:
  lcd_hbp  = TBD              # Horizontal back porch
  lcd_ht   = TBD              # Horizontal total
  lcd_hspw = TBD              # Hsync pulse width

Vertical:
  lcd_vbp  = TBD              # Vertical back porch
  lcd_vt   = TBD              # Vertical total
  lcd_vspw = TBD              # Vsync pulse width
```

**MIPI Register Configuration**:
25 register values (reg0-reg24) in mipi_reg section:
- DSI protocol configuration
- PHY timing parameters
- Lane configuration
- Escape clock settings

**GPIO Control**:
```
lcd_gpio_0 = Reset signal
lcd_gpio_1 = Power enable
lcd_gpio_2 = Backlight enable
lcd_gpio_3-9 = Additional control signals
```

### Backlight Control

**Method**: PWM (Pulse Width Modulation)
**Channel**: PWM6
**Frequency**: Configurable (typical 1-10 kHz)
**Polarity**: Configurable (normal/inverted)

**Configuration**:
```
lcd_pwm_used = 1              # PWM backlight enabled
lcd_pwm_ch = 6                # PWM channel 6
lcd_pwm_freq = TBD            # PWM frequency (Hz)
lcd_pwm_pol = 0               # Polarity (0=normal, 1=inverted)
```

**Brightness Control**:
```
backLightMode = 2             # 0=manual, 1=auto, 2=day/night
backLightDay = 80             # Day brightness (%)
backLightNight = 40           # Night brightness (%)
backLightGain = 50            # Overall gain
backLightMinValue = 5         # Minimum brightness
```

### HDMI Output (if equipped)

**Configuration**:
```
hdmi_used = TBD               # HDMI enabled
hdmi_power = GPIO             # HDMI power control
hdmi_hdcp_enable = TBD        # HDCP 1.x support
hdmi_hdcp22_enable = TBD      # HDCP 2.2 support
hdmi_cec_support = TBD        # CEC support
ddc_scl, ddc_sda = GPIOs      # DDC I2C pins
```

### Video DAC Output (VDPO)

For composite video output (CVBS):
```
vdpo0 configuration:
  - Protocol: PAL/NTSC
  - Resolution: 720x480 (NTSC) or 720x576 (PAL)
  - Output pins: vo_d0-d15, vo_clk, vo_de, vo_hs, vo_vs
```

## Camera/Video Input

### Camera Serial Interface (CSI)

**Interface**: MIPI CSI-2
**Lanes**: Configurable (typically 2 or 4 lane)
**Supported Sensors**: OV5647, TP2804, others

**CSI0 Configuration**:
```
csi0_used = 1
csi0_pck  = GPIO              # Pixel clock
csi0_hsync = GPIO             # Horizontal sync
csi0_vsync = GPIO             # Vertical sync
csi0_d0 - csi0_d7 = GPIOs     # Data lanes 0-7
```

### Camera Sensors

#### Sensor 0 (Rear Camera)

**Model**: OV5647 (detected)
- **Resolution**: 5MP (2592x1944)
- **Interface**: MIPI CSI-2
- **Formats**: RAW10, RAW8
- **Frame Rate**: 30 fps @ 1080p

**Configuration**:
```
sensor0_mname = "ov5647"      # Model name
sensor0_twi_cci_id = 0        # I2C bus ID
sensor0_twi_addr = 0x36       # I2C address
sensor0_mclk_id = 0           # Master clock ID
sensor0_pos = "rear"          # Position
sensor0_isp_used = 1          # ISP processing
```

**Power Rails**:
```
sensor0_iovdd = "iovdd-csi"   # I/O voltage (1.8V)
sensor0_avdd = "avdd-csi"     # Analog voltage (2.8V)
sensor0_dvdd = "dvdd-csi-18"  # Digital voltage (1.8V)
```

**Control GPIOs**:
```
sensor0_reset = GPIO          # Reset pin
sensor0_pwdn = GPIO           # Power down pin
sensor0_power_en = GPIO       # Power enable
```

#### Sensor 1 (Front Camera)

Similar configuration to Sensor 0, position = "front"

### Camera Flash

**Model**: LED flash controlled by GPIO
**Configuration**:
```
flash0_type = 2               # Type (2=LED)
flash0_en = GPIO              # Enable pin
flash0_mode = GPIO            # Mode control
flash0_flvdd = "vcc-flash"    # Flash voltage rail
```

### Autofocus Actuator

**Model**: AD5820 (voice coil motor driver)
**Interface**: I2C
**Configuration**:
```
actuator0_name = "ad5820_act"
actuator0_slave = 0x0C        # I2C address
actuator0_af_pwdn = GPIO      # Power down
actuator0_afvdd = "afvcc-csi" # AF motor voltage
```

## Audio Subsystem

### Audio Codec

**Chip**: Internal codec in F133 or external (audioChip=3)
**Interface**: I2S (Inter-IC Sound)

**Codec Configuration**:
```
digital_vol = TBD             # Digital volume
lineout_vol = TBD             # Line output volume
mic1gain = TBD                # Microphone 1 gain
mic2gain = TBD                # Microphone 2 gain
mic3gain = TBD                # Microphone 3 gain
adcgain = TBD                 # ADC gain
```

**Dynamic Range Compression**:
```
adcdrc_cfg = TBD              # ADC DRC configuration
dacdrc_cfg = TBD              # DAC DRC configuration
```

**High-Pass Filter**:
```
adchpf_cfg = TBD              # ADC HPF configuration
dachpf_cfg = TBD              # DAC HPF configuration
```

**Speaker Control**:
```
pa_ctl_level = TBD            # Power amplifier control level
pa_msleep_time = TBD          # PA startup delay (ms)
gpio-spk = GPIO               # Speaker enable GPIO
```

### Audio Routing

**Channels**:
```
Channel A (0-15):
  0  = Main audio output
  1  = AUX input 1
  2  = AUX input 2
  11 = AUX input 3
```

**Volume Gains** (per source):
```
armVolGain = 88%              # ARM/amplifier gain
radioVolGain = 88%            # Radio gain
btVolGain = 90%               # Bluetooth gain
mediaVolGain = 88%            # Media player gain
carplayVolGain = 88%          # CarPlay gain
dvdVolGain = 88%              # DVD gain
auxVolGain = 88%              # AUX gain
```

**Volume Range**:
```
maxVolume = 22                # Maximum volume level (0-30)
minVolDB = -39                # Minimum volume in dB
```

## Connectivity

### WiFi

**Standard**: 802.11 a/b/g/n (possibly ac)
**Bands**: 2.4 GHz, 5 GHz (androidWifiMode=2 suggests 5GHz support)
**Mode**: Station (client) and AP (hotspot)

**Configuration**:
```
wifi_used = 1
wifi_sdc_id = TBD             # SDIO interface ID
wifi_usbc_id = TBD            # USB interface ID (if USB WiFi)
wifi_mod_sel = TBD            # Module selection
wifi_power = GPIO             # Power control
```

**Chip**: Likely Realtek RTL8xxx or Broadcom BCM43xxx

### Bluetooth

**Standard**: Bluetooth 4.2 or 5.0 (BR/EDR + BLE)
**Profiles**:
- A2DP: Advanced Audio Distribution Profile
- AVRCP: Audio/Video Remote Control Profile
- HFP: Hands-Free Profile
- PBAP: Phone Book Access Profile
- MAP: Message Access Profile

**Configuration**:
```
btModule = 1                  # Module type
btSerialName = TBD            # UART interface
btLocalName = "SWL-BT"        # Device name
btCmdMicGain = "AT#VN030606"  # Mic gain AT command
```

**Chip**: Likely integrated with WiFi (combo chip)

### Ethernet (GMAC)

**Interface**: RGMII (Reduced Gigabit Media Independent Interface)
**Speed**: 10/100/1000 Mbps
**PHY**: External PHY chip connected via RGMII

**Configuration**:
```
gmac0_used = 1
phy-mode = "rgmii"
tx-delay = TBD                # TX delay (0-7)
rx-delay = TBD                # RX delay (0-31)
```

**Pin Configuration** (24 pins):
```
Data:
  gmac_rxd0-3 = GPIOs         # RX data lanes
  gmac_txd0-3 = GPIOs         # TX data lanes
Control:
  gmac_rxck = GPIO            # RX clock
  gmac_rxctl = GPIO           # RX control
  gmac_txck = GPIO            # TX clock
  gmac_txctl = GPIO           # TX control
  gmac_clkin = GPIO           # Input clock
Management:
  gmac_mdc = GPIO             # Management data clock
  gmac_mdio = GPIO            # Management data I/O
```

## Serial Communication

### UART (Universal Asynchronous Receiver/Transmitter)

**Ports**: UART0 - UART4
**UART0** (Debug Console):
```
uart_debug_port = 0           # UART0 for debug
uart_debug_baudrate = 115200  # Baud rate
uart_debug_tx = GPIO_PA2      # TX pin
uart_debug_rx = GPIO_PA3      # RX pin
```

**Other UARTs**:
- UART1: MCU communication (mcuSerialName=/dev/uart1)
- UART2-4: Available for peripherals

### I2C/TWI (Two-Wire Interface)

**Buses**: TWI0 - TWI3
**Speed**: Standard (100 kHz) or Fast (400 kHz)

**Usage**:
- TWI0: Camera sensors, touchscreen
- TWI1: Reserved
- TWI2: CarPlay chip (carplayI2cName=/dev/twi2)
- TWI3: Available

**Configuration per bus**:
```
twiX_scl = GPIO               # Clock pin
twiX_sda = GPIO               # Data pin
```

### SPI (Serial Peripheral Interface)

**Port**: SPI0
**Mode**: Master
**Speed**: Up to 100 MHz

**Configuration**:
```
spi0_sclk = GPIO              # Clock
spi0_cs = GPIO                # Chip select
spi0_mosi = GPIO              # Master out, slave in
spi0_miso = GPIO              # Master in, slave out
```

**Quad SPI Support** (for SPI NOR flash):
```
spi0_wp = GPIO                # Write protect
spi0_hold = GPIO              # Hold signal
```

**Usage**: SPI NOR flash for boot (spinor_para configuration)

### RSB (Reduced Serial Bus)

**Purpose**: Communication with PMU (AXP28)
**Pins**:
```
s_rsb_sck = GPIO              # Clock
s_rsb_sda = GPIO              # Data
```

**Advantages over I2C**:
- Higher speed
- Lower pin count
- Designed for PMU communication

## Storage

### SD/MMC Controllers

**Controllers**: SDC0, SDC1
**Modes**: 1-bit, 4-bit, 8-bit (MMC)
**Speed**: High-speed (50 MHz), SDR104 (200 MHz)

**SDC0** (SD Card):
```
sdc0_used = 1
bus-width = 4                 # 4-bit mode
card_high_speed = 1           # High-speed enabled
sdc0_d0 - sdc0_d3 = GPIOs     # Data pins
sdc0_clk = GPIO               # Clock
sdc0_cmd = GPIO               # Command
```

**SDC1** (eMMC):
```
sdc1_used = 1
bus-width = 8                 # 8-bit mode
sdc1_d0 - sdc1_d7 = GPIOs     # Data pins
sdc_emmc_rst = GPIO           # eMMC reset
sdc_ds = GPIO                 # Data strobe (HS400)
```

### SPI NOR Flash

**Interface**: SPI or Quad SPI
**Capacity**: Typically 16-32 MB
**Usage**: Boot partition (1.img)

**Configuration**:
```
spi_sclk = GPIO
spi_cs = GPIO
spi0_mosi = GPIO
spi0_miso = GPIO
spi0_wp = GPIO                # Write protect
spi0_hold = GPIO              # Hold
```

### NAND Flash (if equipped)

**Interface**: Parallel NAND
**Configuration**: nand0_para section (40+ parameters)

```
nand0_used = TBD
nand0_we = GPIO               # Write enable
nand0_ale = GPIO              # Address latch enable
nand0_cle = GPIO              # Command latch enable
nand0_ce0 = GPIO              # Chip enable 0
nand0_nre = GPIO              # Read enable
nand0_rb0 = GPIO              # Ready/busy 0
nand0_d0 - nand0_d7 = GPIOs   # Data bus
nand0_ndqs = GPIO             # Data strobe
```

## USB

### USB Controllers

**Controllers**: USBC0, USBC1, USBC2
**USB Version**: USB 2.0 High-Speed (480 Mbps)

**USBC0** (OTG - On-The-Go):
```
usb_port_type = OTG           # Host/Device/OTG
usb_detect_type = GPIO        # Detection method
usb_id_gpio = GPIO            # USB ID pin
usb_det_vbus_gpio = GPIO      # VBUS detection
usb_drv_vbus_gpio = GPIO      # VBUS control
usb_speed_mode = 2            # High-speed
```

**Usage**:
- CarPlay/Android Auto (usbIphoneLink=1, usbAndroidLink=2)
- USB Mass Storage
- ADB (Android Debug Bridge)

**USBC1, USBC2** (Host):
```
usb_port_type = Host          # Host-only
usb_drv_vbus_gpio = GPIO      # VBUS power control
```

**Usage**:
- USB drives for media playback
- USB WiFi/Bluetooth dongles

### USB Device Features

**Mass Storage**:
```
vendor_id = TBD
mass_storage_id = TBD
luns = 1                      # Logical units
```

**ADB**:
```
adb_id = TBD
manufacturer_name = "USB Developer"
product_name = "Android"
serial_number = "20080411"
```

## Input Devices

### Touchscreen

**Type**: Capacitive
**Controller**: he0801a068
**Interface**: I2C
**Resolution**: 1280x480 (matches display)

**Configuration**:
```
ctp_used = 1
ctp_twi_id = 0                # I2C bus
ctp_twi_addr = 0x??           # I2C address
ctp_screen_max_x = 1280
ctp_screen_max_y = 480
ctp_int_port = GPIO           # Interrupt pin
ctp_wakeup = GPIO             # Wakeup/reset pin
```

**Calibration**:
```
bTouchXYSwap = 0              # Swap axes
bTouchXReverse = 1            # Mirror X
bTouchYReverse = 0            # Mirror Y
touchCalibData = ""           # Additional calibration
```

### Hardware Buttons (ADC-based)

**Interface**: GPADC (General Purpose ADC)
**Channels**: Multiple channels for button matrix

**Configuration**:
```
channel_num = 4
channel_select = bitmask
channel_data_select = TBD
```

**Button Voltage Thresholds**:
```
key0_vol = 21                 # Button 0 ADC value
key0_val = 224                # Key code

key1_vol = 27
key1_val = TBD

key2_vol = 39
key2_val = TBD

key3_vol = 59
key3_val = TBD
```

### Infrared Remote

**Interface**: CIR (Consumer Infrared)
**Protocol**: Configurable (NEC, RC5, etc.)

**Configuration**:
```
s_cir0_used = 1
ir_protocol_used = TBD        # Protocol selection
ir_power_key_code0 = TBD      # Power button code
ir_addr_code0 = TBD           # Device address
```

**Supported Keys**:
- Power, Home, Return, Menu
- Setup, Volume Up/Down, Mute
- Navigation (Up, Down, Left, Right, Enter)

## Peripherals

### Radio Tuner

**Module Type**: radioModule=2
**Interface**: I2C
**Reset GPIO**: GPIO_403 (radioResetGpio)

**Bands**:
- FM: 87.5 - 108.0 MHz (configurable per region)
- AM: 522 - 1620 kHz (if enabled)

**Features**:
- RDS (Radio Data System) - optional
- Seek/scan with adjustable thresholds
- Stereo/mono switching
- FM transmitter mode (bRadioTransmit=1)

**China Region Presets**:
```
FM1: 88.6, 89.5, 91.5, 93.0, 93.9, 95.1 MHz
FM2: Same presets
FM3: Same presets
Step: 100 kHz
Range: 87.5 - 108.0 MHz
```

### MCU (Microcontroller)

**Type**: External MCU (mcuChip=2)
**Interface**: UART1 (/dev/uart1)
**Purpose**:
- Steering wheel control integration
- Vehicle signal monitoring (brake, illumination)
- CAN bus interface
- Power management

### CAN Bus (if equipped)

**Configuration**:
```
bArmCan = 0                   # Currently disabled
carType = 0                   # Vehicle type
canSerialName = ""            # CAN interface
```

When enabled:
- Read vehicle data (speed, RPM, fuel, etc.)
- Climate control integration
- Steering wheel buttons
- Reverse camera trigger

### Sensors

**G-Sensor (Accelerometer)**:
```
gsensor_twi_id = TBD          # I2C bus
gsensor_twi_addr = 0x??       # I2C address
gsensor_int1 = GPIO           # Interrupt 1
gsensor_int2 = GPIO           # Interrupt 2
```

**GPS Module**:
```
gps_used = TBD
```

**Compass (Magnetometer)**:
```
compass_twi_id = TBD
compass_twi_addr = 0x??
compass_int = GPIO
```

**Gyroscope**:
```
gy_twi_id = TBD
gy_twi_addr = 0x??
gy_int1, gy_int2 = GPIOs
```

## GPIO Summary

### GPIO Banks

Allwinner F133 typically has GPIO banks:
- **PA**: General purpose I/O (PA0-PA31)
- **PB**: General purpose I/O (PB0-PB31)
- **PC**: General purpose I/O (PC0-PC31)
- **PD**: General purpose I/O (PD0-PD31)
- **PE**: General purpose I/O (PE0-PE31)
- **PF**: Typically reserved for special functions
- **PG**: General purpose I/O (limited pins)
- **PH**: General purpose I/O (limited pins)

### Key GPIO Assignments

```
Function              | GPIO        | Direction | Notes
----------------------|-------------|-----------|------------------
UART0 TX (Debug)      | PA2         | Output    | 115200 baud
UART0 RX (Debug)      | PA3         | Input     | 115200 baud
LCD Reset             | lcd_gpio_0  | Output    | Active low
LCD Power             | lcd_gpio_1  | Output    | Active high
Backlight Enable      | lcd_gpio_2  | Output    | Active high
Touch Interrupt       | ctp_int     | Input     | Falling edge
Touch Reset           | ctp_wakeup  | Output    | Active low
Camera Reset          | sensor0_rst | Output    | Active low
Camera Power Down     | sensor0_pwdn| Output    | Active high
Radio Reset           | GPIO_403    | Output    | Active low (typo? should be 4,03 = PD3)
Speaker Enable        | gpio-spk    | Output    | Active high
USB VBUS Control      | usb_drv_*   | Output    | Active high
SD Card Detect        | sdc_det     | Input     | Active low
```

## Boot Configuration

### Boot Modes

1. **SD Card Boot**: Boot from SD card (card0)
2. **eMMC Boot**: Boot from eMMC (card1)
3. **SPI NOR Boot**: Boot from SPI flash
4. **USB Boot**: Fel mode for firmware update

### Boot Sequence

1. **SoC Reset**: Power-on or hardware reset
2. **Boot ROM**: Internal ROM code executes
3. **Boot Media Detection**:
   - Check SD card (if card detect low)
   - Check SPI NOR flash
   - Check eMMC
   - Fall back to USB FEL mode
4. **Load Boot0**: First-stage bootloader (SPL)
5. **Load U-Boot/OpenSBI**: From partition 1
6. **Initialize DRAM**: Using dram_para
7. **Configure PMU**: Set voltages
8. **Setup Clocks**: Configure PLLs
9. **Load Kernel**: Decompress and load melis.bin
10. **Start MELIS**: Jump to kernel entry point

### Boot Pins

```
Boot Mode Select: Typically configured via resistors
- SD card priority
- SPI flash priority
- FEL mode (USB download)
```

## Performance Characteristics

### CPU Performance

- **Clock Speed**: Up to 1.2 GHz
- **DMIPS**: ~1800 DMIPS (estimated)
- **CoreMark**: ~2.5 CoreMark/MHz (RV32GC typical)

### Memory Bandwidth

- **DDR3 @800MHz**: ~6.4 GB/s theoretical
- **Actual**: ~3-4 GB/s (single-channel)

### Video Performance

- **H.264 Decode**: 1080p @ 60 fps
- **H.265 Decode**: 1080p @ 30 fps
- **JPEG Decode**: 8000x8000 @ 30 fps

### Display Performance

- **Maximum Resolution**: 1920x1080 @ 60 Hz
- **Configured**: 1280x480 @ 30 Hz
- **Layers**: Multiple hardware layers for compositing

## Power Consumption

### Typical Power Budget

```
Operating Mode     | Current | Power @ 12V | Notes
-------------------|---------|-------------|-------------------
Active (full)      | 1.5 A   | 18 W        | Display on, playing media
Active (idle)      | 0.8 A   | 9.6 W       | Display on, no media
Standby            | 0.1 A   | 1.2 W       | Display off, RAM retained
Sleep              | 20 mA   | 240 mW      | RAM powered, RTC active
Deep Sleep         | 5 mA    | 60 mW       | RTC only
```

### Power Rails

```
Rail        | Voltage | Max Current | Purpose
------------|---------|-------------|------------------
VCC_12V     | 12V     | 2A          | Main input
VCC_5V      | 5V      | 1.5A        | USB, peripherals
VCC_3V3     | 3.3V    | 1A          | Digital logic
VCC_1V8     | 1.8V    | 500mA       | I/O
VCC_1V2     | 1.2V    | 1.5A        | CPU core
VCC_DRAM    | 1.5V    | 800mA       | DDR3 memory
```

## Thermal Management

- **No Active Cooling**: Passive heatsink only
- **Operating Temperature**: -20°C to +70°C (typical automotive)
- **Storage Temperature**: -40°C to +85°C
- **Thermal Shutdown**: ~85°C junction temperature

## Physical Interfaces

### Connectors

1. **Power Input**: 12V automotive (with reverse polarity protection)
2. **Display**: MIPI DSI flex cable
3. **USB**: 2-3x USB Type-A host ports
4. **USB**: 1x Micro-USB device (for CarPlay/updates)
5. **Camera**: MIPI CSI flex cables (front/rear)
6. **Audio**: Speaker outputs, microphone input
7. **Radio**: Antenna connectors (FM/AM/GPS)
8. **Video**: Composite video input (rear camera)
9. **Ethernet**: RJ45 connector (if equipped)
10. **SD Card**: Micro SD slot
11. **CAN Bus**: Connector for vehicle integration
12. **Steering Wheel**: Connector for button inputs

## References

- Allwinner F133 Datasheet: https://linux-sunxi.org/F133
- RISC-V Specifications: https://riscv.org/specifications/
- AXP Power Management: https://linux-sunxi.org/AXP
- MIPI DSI Specification: MIPI Alliance
- USB 2.0 Specification: USB-IF

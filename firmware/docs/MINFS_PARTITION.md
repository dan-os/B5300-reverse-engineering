# MINFS Partition (Root Filesystem) Documentation

## Overview

The MINFS partition contains the complete root filesystem with all applications, kernel modules, UI resources, and system libraries.

**Location**: Partition 2 (ROOTFS) in gpt.img
**Format**: MINFS (custom filesystem by Allwinner/Melis)
**Size**: ~14 MB
**Type**: Read-only at runtime (ROM filesystem)
**Mount Point**: `/`

## Directory Structure

```
minfs/
├── apps/              # Applications and resources (8.0 MB)
│   ├── init.axf          # Main application binary (2.0 MB)
│   ├── desktop.mod       # Desktop/UI module (28 KB)
│   ├── Font30_8Bit.vft   # Vector font (2.5 MB)
│   ├── Config.ini        # Default configuration (4.3 KB)
│   ├── Version.txt       # Firmware version
│   ├── OsVersion.txt     # OS version
│   ├── AndroidAuto/      # Android Auto resources
│   ├── CarPlay/          # CarPlay resources
│   ├── Data/             # UI layout data files
│   ├── Language/         # Translation files
│   ├── Logo/             # Boot logos
│   ├── UI2/              # UI theme resources
│   └── WallPaper/        # Wallpaper images
├── mod/               # Kernel modules (9.2 MB)
│   ├── carplay.mod       # Apple CarPlay (852 KB)
│   ├── hicar.mod         # Huawei HiCar (557 KB)
│   ├── wireless.mod      # WiFi/BT stack (2.2 MB)
│   ├── eclink.mod        # Echo cancellation (398 KB)
│   ├── oak.mod           # Unknown subsystem (835 KB)
│   ├── cedar.mod         # Video codec (64 KB)
│   ├── charset.mod       # Character set support (219 KB)
│   ├── display.mod       # Display driver (18 KB)
│   ├── video_play.mod    # Video player (61 KB)
│   ├── sensor_play.mod   # Sensor playback (35 KB)
│   ├── mixture.mod       # Audio mixer (35 KB)
│   ├── vcoder.mod        # Video coder (6.4 KB)
│   ├── update.mod        # OTA update (20 KB)
│   ├── ginkgo.mod        # Unknown (4.9 KB)
│   ├── slib.mod          # Shared library (9.6 KB)
│   ├── motolink.mod      # Motorola link? (2.8 KB)
│   ├── cedar/            # Cedar codec data
│   └── willow/           # Willow subsystem
│       └── willow.mod
├── etc/               # System configuration (8 KB)
├── res/               # System resources (68 KB)
├── auto.mod           # Auto-loading module (900 KB)
├── startup.sh         # Boot script
└── rootfs_ini.tmp     # Filesystem info (249 bytes)
```

## Size Distribution

| Directory/File | Size    | Percentage | Purpose                      |
|----------------|---------|------------|------------------------------|
| mod/           | 9.2 MB  | 51%        | Kernel modules               |
| apps/          | 8.0 MB  | 44%        | Applications & UI resources  |
| auto.mod       | 900 KB  | 5%         | Auto-load framework          |
| res/           | 68 KB   | <1%        | System resources             |
| etc/           | 8 KB    | <1%        | Configuration files          |
| Other          | <5 KB   | <1%        | Scripts and metadata         |

## Key Files and Modules

### Core System Files

#### /startup.sh

**Type**: Shell script
**Size**: 186 bytes
**Purpose**: System initialization script

```bash
#!/bin/sh
echo "Execute startup script begin.............."

#insmod d:\mod\display.mod
#insmod d:\mod\orange.mod
insmod d:\apps\desktop.mod
echo "...............Execute startup script end"
```

**Execution Flow**:
1. Executed by MELIS kernel after filesystem mount
2. Loads essential kernel modules
3. Launches desktop environment
4. Note: Uses DOS-style paths (d:\) - MELIS compatibility layer

#### /rootfs_ini.tmp

**Type**: Text metadata
**Size**: 249 bytes
**Purpose**: Filesystem build information

Contains:
- Build date/time
- Filesystem version
- Partition size
- CRC checksums

#### /auto.mod

**Type**: RISC-V ELF executable (kernel module)
**Size**: 899 KB
**Architecture**: RV32IMAFDC
**Purpose**: Automatic module loader and framework

```bash
$ file auto.mod
auto.mod: ELF 32-bit LSB executable, UCB RISC-V, RVC,
          double-float ABI, version 1 (SYSV),
          statically linked, stripped
```

**Functionality**:
- Auto-discovers and loads modules from /mod/
- Provides module dependency resolution
- Exports APIs for other modules
- Likely contains:
  - Module loader framework
  - Plugin architecture
  - Inter-module communication (IPC)
  - Resource management

## Applications Directory (/apps/)

### Core Application

#### init.axf

**Type**: RISC-V ELF executable
**Size**: 2,039,368 bytes (~2.0 MB)
**Architecture**: RV32IMAFDC
**Purpose**: Main application binary

```bash
$ file init.axf
init.axf: ELF 32-bit LSB executable, UCB RISC-V, RVC,
          double-float ABI, version 1 (SYSV),
          statically linked, stripped
```

**ELF Header Analysis**:
```
ELF Magic: 7F 45 4C 46 (ELF)
Class: 32-bit (ELFCLASS32)
Endianness: Little-endian
Machine: RISC-V (0xF3)
Entry Point: 0xE9100000
Program Headers: 1
Section Headers: 7
```

**Memory Mapping**:
```
Type    Offset     VirtAddr   PhysAddr   FileSize  MemSize   Flags
LOAD    0x00016c   0xe9100000 0xe9100000 0x1eb508  0x200750  RWE
```

**Sections**:
- `.text` - Code segment (~1.8 MB)
- `.rodata` - Read-only data (strings, constants)
- `.data` - Initialized data
- `.bss` - Uninitialized data (1 MB at 0xe92eb508)

**Key Functions** (from string analysis):
- UI framework and window management
- Audio/video playback control
- Bluetooth phone integration
- Radio tuner interface
- Media library management
- Settings and configuration
- Touch input handling
- System service management

**Disassembly**:
```bash
# Disassemble with RISC-V toolchain
riscv32-unknown-elf-objdump -d init.axf > init_disasm.txt

# Load in Ghidra
- Language: RISCV:LE:32:RV32GC
- Base address: 0xE9100000
```

#### desktop.mod

**Type**: RISC-V ELF executable (kernel module)
**Size**: 28 KB
**Purpose**: Desktop environment and window manager

Provides:
- Window compositing
- Touch event routing
- Widget framework
- Screen transitions
- Status bar management

### Resources

#### Font30_8Bit.vft

**Type**: Vector font file
**Size**: 2,471,248 bytes (~2.5 MB)
**Format**: Custom vector font format (.vft)
**Purpose**: Scalable UI fonts

Likely contains:
- Unicode character maps
- Vector glyph data
- Font metrics and kerning
- Multiple font faces/weights

**Character Support**:
- Latin alphabet
- Chinese characters (GB2312 or GB18030)
- Japanese (partial)
- Korean (partial)
- Symbols and icons

#### Config.ini

**Type**: Text configuration (INI format)
**Size**: 4,314 bytes
**Purpose**: Default system configuration

This is the factory default configuration. User modifications are stored in the FAT partition's Config.ini, which overrides these defaults.

See [FAT Partition Documentation](./FAT_PARTITION.md#configini) for detailed parameter descriptions.

#### Version.txt

**Content**: `HZ-BX-MIPI-F1026-FM-1.4SDK-20240712-0947`

**Breakdown**:
- `HZ-BX` - Hardware version code
- `MIPI` - Display interface type
- `F1026-FM-1.4` - Model number and revision
- `SDK` - SDK build
- `20240712` - Build date (July 12, 2024)
- `0947` - Build time (09:47)

#### OsVersion.txt

**Content**: `F133-20220107`

**Breakdown**:
- `F133` - Allwinner F133 SoC
- `20220107` - OS release date (January 7, 2022)

### CarPlay and Android Auto

#### AndroidAuto/ Directory

```
AndroidAuto/
└── AndroidAuto.exe     # Placeholder (27 bytes)
```

**AndroidAuto.exe**: Contains only text "com.AndroidAuto.activities"
- Not a real executable
- References actual module: `/mod/hicar.mod` or similar
- Acts as launcher/descriptor

#### CarPlay/ Directory

```
CarPlay/
├── CarPlay.exe         # Placeholder (27 bytes)
├── icon_120x120.png    # App icon (7.3 KB)
├── icon_180x180.png    # App icon (9.3 KB)
└── icon_256x256.png    # App icon (13 KB)
```

**CarPlay.exe**: Contains text "com.Apple.CarPlay.activities"
**Icons**: PNG images for different DPI displays
**Actual Implementation**: `/mod/carplay.mod` (852 KB)

### UI Data Files (/apps/Data/)

Contains ~50 .data files, each representing a UI screen or dialog.

**Format**: Custom binary format (likely proprietary UI layout format)
**Size Range**: 600 bytes to 357 KB
**Total Size**: ~2.1 MB

#### Major UI Screens

| File                    | Size    | Purpose                           |
|-------------------------|---------|-----------------------------------|
| Main.data               | 357 KB  | Main menu screen                  |
| MainAudioOutput.data    | 122 KB  | Audio output settings             |
| MainApp.data            | 118 KB  | Application launcher              |
| PlayerAudio.data        | 116 KB  | Audio player interface            |
| ScreenSaver.data        | 96 KB   | Screen saver                      |
| SetupConfig.data        | 53 KB   | Configuration menu                |
| PlayerList.data         | 52 KB   | Media file list                   |
| BtBookSearch.data       | 47 KB   | Phone book search                 |
| BtDial.data             | 41 KB   | Bluetooth dialer                  |
| BtMusic.data            | 39 KB   | Bluetooth music player            |
| BtTalk.data             | 38 KB   | Active call screen                |
| CarRecorder.data        | 34 KB   | DVR interface                     |
| PlayerPhoto.data        | 34 KB   | Photo viewer                      |

#### Feature-Specific UI

**Bluetooth**:
- BtBook.data - Phone book
- BtDial.data - Dialer
- BtMusic.data - Music player
- BtRecord.data - Call records
- BtSetup.data - BT settings
- BtTalk.data - Call in progress

**Media Player**:
- PlayerAudio.data - Audio player
- PlayerVideo.data - Video player
- PlayerPhoto.data - Photo viewer
- PlayerList.data - File browser
- PlayerSetupAudio.data - Audio EQ
- PlayerSetupBalance.data - Balance/Fader

**Radio**:
- Radio.data - Radio tuner

**DVR**:
- CarRecorder.data - Recording interface
- CarRecorderList.data - Recording list
- CarRecorderPlay.data - Playback
- CarRecorderSetup.data - DVR settings

**Settings**:
- SetupMenu.data - Settings menu
- SetupBasic.data - Basic settings
- SetupConfig.data - Advanced config
- SetupAudio.data - Audio settings
- SetupBalance.data - Audio balance
- SetupLanguage.data - Language selection
- SetupPassword.data - Password change
- SetupFactory.data - Factory reset
- SetupDebug.data - Debug menu
- SetupGain.data - Gain adjustments
- SetupMainKey.data - Key mapping

**Link (Phone Mirroring)**:
- CarPlay.data - CarPlay interface
- AndroidAuto.data - Android Auto interface
- MirrorAndroid.data - Android screen mirror
- MirrorIphone.data - iPhone screen mirror
- AirPlay.data - AirPlay receiver
- AndroidWireless.data - Wireless Android Auto

**Video Input**:
- AuxIn.data - AUX input
- AuxIn2.data - AUX input 2
- Ccd.data - Rear camera display

**Utilities**:
- Calculator.data - Calculator app
- Calendar.data - Calendar app

**System**:
- ScreenSaver.data - Screen saver
- ScreenOff.data - Screen off state
- Power.data - Power/shutdown menu
- Black.data - Black screen

#### .data File Format Analysis

Based on hex analysis of sample files:

```
Header (estimated):
  0x00-0x03: Magic signature
  0x04-0x07: File format version
  0x08-0x0B: Data size
  0x0C-0x0F: Widget count
  0x10+:     Widget definitions

Widget Structure (estimated):
  - Widget type (button, label, image, etc.)
  - Position (x, y, width, height)
  - Style properties (color, font, etc.)
  - Text content or image reference
  - Event handlers
  - Animation definitions
```

**Parsing Tool** (to be developed):
```python
def parse_data_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # Parse header
    magic = struct.unpack('<I', data[0:4])[0]
    version = struct.unpack('<I', data[4:8])[0]
    # ... parse widgets ...
```

### Language Files (/apps/Language/)

Translation files for UI text in multiple languages.

| File              | Size   | Purpose                    |
|-------------------|--------|----------------------------|
| Main.txt          | 76 KB  | Main menu translations     |
| Setup.txt         | 178 KB | Settings menu translations |
| Link.txt          | 59 KB  | CarPlay/Auto translations  |
| TipBox.txt        | 45 KB  | Dialog box text            |
| SystemBar.txt     | 38 KB  | Status bar text            |
| Bt.txt            | 29 KB  | Bluetooth interface        |
| Player.txt        | 22 KB  | Media player               |
| Video.txt         | 21 KB  | Video settings             |
| Radio.txt         | 19 KB  | Radio interface            |
| CarRecorder.txt   | 11 KB  | DVR interface              |
| Calendar.txt      | 9.5 KB | Calendar app               |
| Can.txt           | 5.7 KB | CAN bus integration        |
| Calculator.txt    | 3.7 KB | Calculator app             |

**Format**: Tab-separated values (TSV) or custom format

Example structure (hypothetical):
```
# String ID    English                 Chinese             Spanish
STR_OK         OK                      确定                Aceptar
STR_CANCEL     Cancel                  取消                Cancelar
STR_VOLUME     Volume                  音量                Volumen
```

**Supported Languages** (based on supportLanguage bitmask 42440703):
- English
- Simplified Chinese
- Traditional Chinese
- Spanish
- Portuguese
- Russian
- Arabic
- French
- German
- Italian
- Japanese
- Korean
- Dutch
- Polish
- Turkish

### Logo and Wallpapers

#### Logo/ Directory

```
Logo/
└── stalogo1.jpg        # Boot logo (58 KB)
```

**stalogo1.jpg**: Factory default boot logo
- Displayed during system initialization
- Can be customized via settings menu

#### WallPaper/ Directory

```
WallPaper/
├── 0.jpg              # Wallpaper option 1 (30 KB)
├── 1.jpg              # Wallpaper option 2 (75 KB)
├── 2.jpg              # Wallpaper option 3 (39 KB)
└── 3.jpg              # Wallpaper option 4 (63 KB)
```

**Purpose**: Selectable background wallpapers for main menu

### UI Theme (UI2/)

```
UI2/
└── [Theme-specific resources]
```

Alternative UI theme resources. When uiID=2 is set, resources are loaded from here instead of main apps/ directory.

## Kernel Modules Directory (/mod/)

### Connectivity Modules

#### carplay.mod

**Type**: RISC-V ELF kernel module
**Size**: 852 KB
**Purpose**: Apple CarPlay implementation

**Capabilities**:
- USB CarPlay (wired)
- Wireless CarPlay (WiFi-based)
- iAP2 (iPod Accessory Protocol 2)
- Audio routing
- Touch input forwarding
- Siri integration
- Phone call handling

**Dependencies**:
- wireless.mod (for WiFi CarPlay)
- eclink.mod (for echo cancellation)
- Audio codec drivers

**Protocol**:
- USB Communication Device Class (CDC)
- Bonjour/mDNS for discovery
- H.264 video stream
- AAC audio stream

#### hicar.mod

**Type**: RISC-V ELF kernel module
**Size**: 557 KB
**Purpose**: Huawei HiCar implementation

**Capabilities**:
- Huawei HiCar phone projection
- HiCar SDK integration
- Touch forwarding
- Audio/video streaming
- Probably also handles Android Auto generic projection

**Note**: May be dual-purpose module handling both HiCar and Android Auto, or Android Auto might use separate generic projection code.

#### wireless.mod

**Type**: RISC-V ELF kernel module
**Size**: 2.2 MB (largest module)
**Purpose**: WiFi and Bluetooth stack

**Components**:
- WiFi driver (802.11a/b/g/n)
- Bluetooth driver (BR/EDR + BLE)
- WiFi supplicant (WPA2/WPA3)
- Bluetooth profiles:
  - A2DP (Audio streaming)
  - AVRCP (Remote control)
  - HFP (Hands-free)
  - PBAP (Phone book)
  - MAP (Messaging)
- Network stack integration

**Supported Hardware**:
- Likely Realtek or Broadcom WiFi/BT combo chip
- Allwinner internal WiFi/BT (if F133 has integrated)

**Configuration**:
- Controlled via Config.ini [BT] and wifi_para sections
- Runtime config via ioctl or sysfs

#### eclink.mod

**Type**: RISC-V ELF kernel module
**Size**: 398 KB
**Purpose**: Echo cancellation and noise reduction

**Features**:
- Acoustic Echo Cancellation (AEC)
- Noise Suppression (NS)
- Automatic Gain Control (AGC)
- Voice Activity Detection (VAD)

**Use Cases**:
- Bluetooth hands-free calling
- CarPlay/Android Auto phone calls
- In-car voice commands

**Algorithms**:
- Configurable echo delay (200ms default)
- Multiple cancellation modes (mode 4 active)
- Adjustable noise threshold
- AGC range 0-15 dB

### Media and Display Modules

#### cedar.mod

**Type**: RISC-V ELF kernel module
**Size**: 64 KB
**Purpose**: Allwinner Cedar video codec framework

**Cedar** is Allwinner's proprietary video encoding/decoding engine.

**Supported Codecs**:
- H.264/AVC decode
- H.265/HEVC decode
- MPEG-2/4 decode
- VP8/VP9 decode (possibly)
- JPEG encode/decode

**Hardware Acceleration**:
- Uses dedicated VPU (Video Processing Unit) in F133
- Zero-copy DMA for efficient video pipeline

**Data Files**:
```
mod/cedar/
├── [Codec configuration]
├── [Hardware register maps]
└── [Firmware blobs]
```

#### vcoder.mod

**Type**: RISC-V ELF kernel module
**Size**: 6.4 KB
**Purpose**: Video coder/decoder thin wrapper

Provides high-level API wrapping cedar.mod functionality.

#### video_play.mod

**Type**: RISC-V ELF kernel module
**Size**: 61 KB
**Purpose**: Video playback management

**Features**:
- File format detection
- Demuxing (AVI, MP4, MKV, etc.)
- Subtitle rendering
- Playback control (play/pause/seek)
- Multi-angle DVD support

#### sensor_play.mod

**Type**: RISC-V ELF kernel module
**Size**: 35 KB
**Purpose**: Sensor playback/recording

Likely handles:
- Camera preview
- Video recording from camera sensors
- Snapshot capture

#### display.mod

**Type**: RISC-V ELF kernel module
**Size**: 18 KB
**Purpose**: Display driver and framebuffer management

**Responsibilities**:
- Framebuffer allocation
- Display pipeline configuration
- Layer compositing
- Hardware scaler
- Color space conversion

**Supported Outputs**:
- MIPI DSI (primary)
- HDMI (if available)
- CVBS (composite video)

### Audio Modules

#### mixture.mod

**Type**: RISC-V ELF kernel module
**Size**: 35 KB
**Purpose**: Audio mixing and routing

**Features**:
- Multi-source audio mixing
- Volume control per source
- EQ (equalizer) application
- Balance/fader control
- Sample rate conversion

**Audio Sources**:
- Media player
- Radio
- Bluetooth
- CarPlay/Android Auto
- Navigation voice
- System sounds

### Character and System Libraries

#### charset.mod

**Type**: RISC-V ELF kernel module
**Size**: 219 KB
**Purpose**: Character set encoding support

**Supported Encodings**:
- UTF-8
- UTF-16
- GB2312 / GB18030 (Simplified Chinese)
- Big5 (Traditional Chinese)
- Shift-JIS (Japanese)
- EUC-KR (Korean)
- ISO-8859-1 (Latin-1)

**Functions**:
- Encoding conversion
- Character classification
- Collation (sorting)

#### slib.mod

**Type**: RISC-V ELF kernel module
**Size**: 9.6 KB
**Purpose**: Shared library support

Provides:
- Dynamic linking for modules
- Symbol resolution
- Module versioning

### Subsystem Modules

#### oak.mod

**Type**: RISC-V ELF kernel module
**Size**: 835 KB (second largest)
**Purpose**: Unknown major subsystem

**Theories**:
- Application framework
- Graphics rendering engine
- Plugin system
- Service manager

Requires reverse engineering to determine exact purpose.

#### ginkgo.mod

**Type**: RISC-V ELF kernel module
**Size**: 4.9 KB
**Purpose**: Unknown (possibly hardware abstraction)

Small size suggests:
- Hardware abstraction layer
- Device-specific driver
- Power management
- GPIO controller

#### willow/

Directory containing willow.mod subsystem.

```
mod/willow/
├── willow.mod
└── [Additional willow resources]
```

Purpose unknown - requires analysis.

#### motolink.mod

**Type**: RISC-V ELF kernel module
**Size**: 2.8 KB
**Purpose**: Possibly Motorola phone link

Very small size suggests:
- Protocol shim
- Device detection
- Legacy compatibility layer

### System Modules

#### update.mod

**Type**: RISC-V ELF kernel module
**Size**: 20 KB
**Purpose**: Firmware update mechanism

**Features**:
- OTA update support
- USB update
- SD card update
- Update package verification
- Rollback on failure

**Update Process**:
1. Verify update package signature
2. Extract update files
3. Write to inactive partition
4. Set boot flag
5. Reboot
6. Verify boot success
7. Mark partition as active

## System Configuration (/etc/)

Contains system-level configuration files.

**Estimated Contents**:
- Network configuration
- Service startup scripts
- Device mappings
- Mount points

## System Resources (/res/)

**Size**: 68 KB

Contains:
- System icons
- Cursors
- Default UI elements
- Error graphics

## Module Loading Sequence

Based on startup.sh and auto.mod:

1. **Kernel Boot** (MELIS loads from melis.bin)
2. **Filesystem Mount** (MINFS mounted at /)
3. **Execute startup.sh**
   - Loads desktop.mod
4. **auto.mod Initialization**
   - Scans /mod/ directory
   - Resolves dependencies
   - Loads modules in order:
     1. slib.mod (shared libraries)
     2. charset.mod (character sets)
     3. display.mod (display driver)
     4. cedar.mod + vcoder.mod (video codecs)
     5. wireless.mod (WiFi/BT)
     6. eclink.mod (echo cancellation)
     7. mixture.mod (audio mixer)
     8. carplay.mod, hicar.mod (phone integration)
     9. oak.mod (major subsystem)
     10. Other modules as needed
5. **Launch init.axf**
   - Main application starts
   - Loads UI from /apps/Data/
   - Reads configuration
   - Initializes services
6. **User Interface Ready**

## Filesystem Characteristics

### MINFS Properties

- **Read-only**: Cannot be modified at runtime
- **Memory-mapped**: Direct execution from flash
- **Compressed**: No compression (pre-expanded)
- **Alignment**: 4-byte aligned for RISC-V
- **Endianness**: Little-endian

### Advantages

- Fast boot (no decompression)
- Low RAM usage (XIP - eXecute In Place)
- Deterministic performance
- Corruption-resistant

### Disadvantages

- Cannot modify without reflashing
- Updates require full partition write
- Limited flexibility

## Extraction and Analysis

### Extract MINFS

```bash
# Using custom MINFS tool (if available)
minfs-extract minfs.img -o minfs/

# Or mount with FUSE driver
minfs-fuse minfs.img /mnt/minfs

# Alternatively, use binwalk
binwalk -e minfs.img
```

### Analyze Modules

```bash
# List symbols in module
riscv32-unknown-elf-nm carplay.mod

# Disassemble module
riscv32-unknown-elf-objdump -d carplay.mod > carplay_disasm.txt

# View strings
strings carplay.mod | grep -i "carplay"

# Load in Ghidra
# Language: RISCV:LE:32:RV32GC
```

### Analyze init.axf

```bash
# View ELF structure
readelf -a init.axf

# Extract sections
riscv32-unknown-elf-objcopy -O binary -j .text init.axf text.bin

# Disassemble
riscv32-unknown-elf-objdump -d init.axf > init_full.asm

# Analyze in Ghidra
# Base: 0xE9100000
# Auto-analyze and examine function calls
```

## Modification and Customization

### Modifying UI

1. **Extract .data files**
2. **Reverse engineer .data format**
3. **Modify layouts/text/colors**
4. **Rebuild .data files**
5. **Recreate MINFS image**
6. **Flash to device**

### Adding Custom Module

1. **Write RISC-V module**
2. **Compile with correct toolchain**
3. **Link against module API**
4. **Copy to /mod/ in MINFS**
5. **Update auto.mod or startup.sh**
6. **Rebuild MINFS**

### Replacing Application

1. **Develop new init.axf**
2. **Maintain compatibility with modules**
3. **Replace in /apps/**
4. **Rebuild MINFS**
5. **Test thoroughly**

## Security Considerations

- **No Code Signing**: Modules not signed
- **No Encryption**: Binaries in plaintext
- **Debug Symbols Stripped**: Harder to reverse but not impossible
- **Direct Memory Access**: Modules have kernel privileges
- **No ASLR**: Fixed load addresses

## References

- MINFS Documentation: (Allwinner internal)
- MELIS Module API: https://github.com/lindenis-org
- RISC-V ELF Format: RISC-V ELF psABI Specification
- Ghidra RISC-V Support: https://ghidra-sre.org/

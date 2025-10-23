# FAT Partition (fat.img) Documentation

## Overview

The FAT partition contains user-modifiable configuration, settings, and runtime data. This partition is read/write and persists user preferences across reboots.

**Location**: Partition 3 (UDISK) in gpt.img
**Format**: FAT16 filesystem
**Size**: 512 KB (524,288 bytes)
**Used Space**: 258,048 bytes (~50%)
**Free Space**: 169,472 bytes
**Mount Point**: `/mnt/udisk` or `F:`
**Cluster Size**: 512 bytes
**Sector Size**: 512 bytes

## Directory Structure

```
fat.img (F:/)
├── Config.ini              # Main runtime configuration (4,314 bytes)
├── config_checksum.bin     # Configuration checksum (4 bytes)
├── stalogo.jpg            # Startup logo image (59,181 bytes)
├── Save/                  # User data and preferences
│   ├── SetupSave.bin      # System settings (1,048 bytes)
│   ├── boot.bin           # Boot flags (10 bytes)
│   ├── RadioSave.bin      # Radio presets (108 bytes)
│   ├── SdSave.dat         # SD card state (832 bytes)
│   ├── VideoSave.bin      # Video settings (152 bytes)
│   ├── LinkSave.bin       # CarPlay/Auto settings (28 bytes)
│   └── BT/               # Bluetooth pairing data
│       └── 00B8B64F537F.pr # Paired device (MAC: 00:B8:B6:4F:53:7F)
├── UI1/                   # UI Theme 1
│   └── Config.ini         # Theme 1 config (4,521 bytes)
└── UI2/                   # UI Theme 2
    └── Config.ini         # Theme 2 config (4,314 bytes)
```

## File Details

### Config.ini

**Type**: Text configuration file (INI format)
**Size**: 4,314 bytes
**Purpose**: Main runtime configuration and device settings
**Encoding**: ASCII

This is the primary configuration file that controls all device behavior and features.

#### File Structure

The file is organized into 17 sections:

```ini
[SETUP]      # User preferences and UI settings
[CONFIG]     # System configuration and capabilities
[DEBUG]      # Debug and logging options
[MCU]        # Microcontroller interface
[CAN]        # CAN bus configuration (automotive)
[ARM]        # ARM audio management
[AUDIO]      # Audio chip configuration
[STARTUP]    # Boot behavior
[RADIO]      # FM/AM radio settings
[CHINA]      # Region-specific radio frequencies
[DVD]        # DVD player settings
[BT]         # Bluetooth configuration
[MEDIA]      # Media player settings
[TV]         # TV input configuration
[VIDEO]      # Video input/output settings
[LINK]       # CarPlay/Android Auto/HiCar
[BACKLIGHT]  # Display backlight control
[TOUCH]      # Touchscreen calibration
[MIC]        # Microphone configuration
[MAINKEY]    # Hardware button mapping
[SCREENKEY]  # Touchscreen button regions
[SCREEN]     # Display orientation
[PANELKEY1]  # Panel button voltage mapping
```

#### Critical Settings

##### User Preferences [SETUP]
```ini
b12Hour=0                  # 24-hour time format (0) or 12-hour (1)
bBeepOn=1                  # System beep enabled
bBrakeWarn=0              # Brake warning disabled
bScreenSave=1             # Screen saver enabled
bVideoOutput=0            # Video output disabled
bDateShow=1               # Show date on screen
bAnyKeyPowerUp=1          # Any key can wake device
bBackOff=0                # Rear camera stays on
bEnableFrontCamera=0      # Front camera disabled

bright=51                  # Brightness (0-100)
contrast=52               # Contrast (0-100)
hue=50                    # Hue (0-100)
saturation=55             # Saturation (0-100)

language=0                # Language ID (0=first in list)
animationType=0           # Boot animation type
idleReturnTime=1000       # Idle timeout (ms)
vcomVoltage=100           # LCD VCOM voltage
avddVoltage=50            # LCD AVDD voltage

bBackMute=1               # Mute when in reverse
colorLampMode=0           # Color lamp mode
wheelType=0               # Steering wheel button type
```

##### System Configuration [CONFIG]
```ini
bArmBeep=0                # ARM audio beep
bBackToMain=0             # Back button returns to main
bBackToSource=1           # Back button returns to source
bCapacitiveScreen=0       # Capacitive (0) vs Resistive (1)
bFontBold=0               # Use bold fonts
bEnableAddFont=0          # Additional font support
bToastAsTip=1             # Show toast notifications

mainID=0                  # Main menu ID
maxVolume=22              # Maximum volume level (0-30)
uiType=2                  # UI theme type
uiBpp=24                  # Bits per pixel (16/24/32)
photoConvertMode=1        # Photo conversion mode
usb0Speed=2               # USB0 speed (2=high-speed)
usb1Speed=2               # USB1 speed
screenResolution=2        # Screen resolution ID

supportLanguage=42440703  # Bitmask of supported languages
sourceValid=7286893       # Bitmask of enabled sources
saleArea=0                # Sales region code
arrowKeyMode=-1           # Arrow key behavior
maxVideoValue=100         # Max video level
saveMethod=3              # Save method (3=immediate)
brakeDetectGpio=-1        # Brake detect GPIO (-1=disabled)
illDetectGpio=-1          # Illumination detect GPIO

defaultSource=Radio       # Default source on boot
defaultInterface=         # Default interface

# Security
logoPassword=112233       # Logo change password ⚠️
factoryPaswword=113266    # Factory reset password ⚠️

logoCardName=F:           # Logo storage location
brakeActiveLevel=1        # Brake signal active level
bSavePowerOff=0          # Save state on power off
bUseSoftReset=0          # Use soft reset
defaultDateTime=20240101  # Default date if RTC fails
uiID=2                    # Active UI theme ID
```

##### Debug Options [DEBUG]
```ini
bPrintLog=1               # Enable logging
bPrintMem=1               # Print memory usage
bPrintTouch=0             # Log touch events
bPrintThreadCpuLoad=0     # Log thread CPU usage
bUseLogBuffer=0           # Use log buffer
```

##### MCU Interface [MCU]
```ini
mcuChip=2                 # MCU chip type
mcuSerialName=/dev/uart1  # MCU communication port
```

##### Radio Configuration [RADIO]
```ini
bArmRadio=1               # Enable ARM radio control
radioChannelA=0           # Audio channel
radioVolGain=88           # Volume gain (%)
radioMaxDac=799072        # Maximum DAC value
radioModule=2             # Radio module type
radioArea=0               # Region (0=China)
fmStopValue=20            # FM scan stop threshold
amStopValue=35            # AM scan stop threshold
stOpenValue=20            # Stereo threshold
fmAdjChannel=58           # FM adjacent channel rejection
fmMultipath=10            # FM multipath detection
fmDetuning=5              # FM detuning compensation
amDetuning=10             # AM detuning compensation
bAmEnable=0               # AM band enabled
bAmLocEnable=0            # AM local mode
bHaveRds=0                # RDS support
bRdsEnDefault=0           # RDS enabled by default
radioButtonType=0         # Button behavior
bRadioBackgroundRun=1     # Run in background
bRadioSoundAtCarPlay=0    # Radio audio during CarPlay

radioResetGpio=403        # Radio reset GPIO
rdsInterruptGpio=-1       # RDS interrupt GPIO
radioI2cName=             # Radio I2C bus
bRadioTransmit=1          # FM transmitter mode
```

##### Radio Frequencies [CHINA]
```ini
# Format: Default,Min,Preset1-7,Step,Band,FreqMin,FreqMax
FM1=8860,8860,8950,9150,9300,9390,9510,10,5,8750,10800
FM2=8860,8860,8950,9150,9300,9390,9510,10,5,8750,10800
FM3=8860,8860,8950,9150,9300,9390,9510,10,5,8750,10800
AM1=522,522,522,603,999,1620,522,9,9
AM2=522,522,522,603,999,1620,522,9,9
```

##### Bluetooth Configuration [BT]
```ini
btModule=1                # BT module type
btmChannelA=0             # BT music audio channel
btVolume=15               # BT volume level
btVolGain=90              # BT volume gain (%)
btmVolGain=90             # BT music gain (%)
bBtMusicNeedConnect=0     # Music requires connection
btSerialName=             # BT serial port
btCmdMicGain=AT#VN030606  # BT mic gain command
btLocalName=SWL-BT        # BT device name
```

##### Media Player [MEDIA]
```ini
bEnableLicenseMedia=0     # License validation required
bMediaBackgroundPlay=0    # Play in background
bMediaSoftDecode=1        # Software decoding
bDecodeHDPhoto=1          # HD photo decode
mediaMaxVol=100           # Max media volume
mediaVolGain=88           # Media volume gain (%)
mediaChannelA=0           # Audio channel
mediaBright=46            # Video brightness
mdiaConstast=47           # Video contrast (typo in original)
mediaHue=50               # Video hue
mediaSaturation=91        # Video saturation

usbDiskName=              # USB disk device name
usbDisk2Name=             # USB disk 2 device name
sdCardName=               # SD card device name
sdCard2Name=              # SD card 2 device name
```

##### CarPlay/Android Auto [LINK]
```ini
bEchoCancel=1             # Echo cancellation
echoDelayTime=200         # Echo delay (ms)
echoCancelMode=4          # EC algorithm mode
bNoiseCancel=1            # Noise cancellation
noiseCancelMode=3         # NC algorithm mode
bAutoGainCtrl=0           # Automatic gain control
minAgcGain=0              # Min AGC gain
maxAgcGain=15             # Max AGC gain
noiseThreshold=150        # Noise threshold
micGain=65                # Microphone gain

usbIphoneLink=1           # iPhone USB connection type
usbAndroidLink=2          # Android USB connection type
carplayVolGain=88         # CarPlay volume gain
carplayVolume=10          # CarPlay volume level
carplayIconLabel=         # CarPlay icon label
carplayI2cName=/dev/twi2  # CarPlay chip I2C bus

linkVideoWidth=1280       # Link video width
linkVideoHeight=480       # Link video height
androidWifiMode=2         # Android WiFi mode (2=5GHz)
```

##### Display Backlight [BACKLIGHT]
```ini
backLightGain=50          # Backlight gain
bBackLightReverse=0       # Reverse PWM polarity
bBackLightPowerCtrl=1     # Power control enabled
backLightMinValue=5       # Minimum brightness
backLightMode=2           # Mode (0=manual, 1=auto, 2=day/night)
backLightDay=80           # Day brightness
backLightNight=40         # Night brightness
backLight=80              # Current brightness
```

##### Touchscreen [TOUCH]
```ini
bTouchXYSwap=0            # Swap X and Y axes
bTouchXReverse=1          # Reverse X axis
bTouchYReverse=0          # Reverse Y axis
touchCalibData=           # Calibration data (if needed)
```

##### Screen Configuration [SCREEN]
```ini
rotateAngle=90            # Screen rotation (0/90/180/270)
refreshRate=30            # Display refresh rate (Hz)
```

##### Hardware Keys [MAINKEY]
```ini
# ADC voltage values for hardware buttons
key0=21                   # Button 0 ADC value
key1=27                   # Button 1 ADC value
key2=39                   # Button 2 ADC value
key3=59                   # Button 3 ADC value
```

### config_checksum.bin

**Type**: Binary checksum
**Size**: 4 bytes
**Purpose**: Integrity check for Config.ini

Simple CRC32 or checksum of Config.ini to detect corruption.

### stalogo.jpg

**Type**: JPEG image
**Size**: 59,181 bytes (~58 KB)
**Dimensions**: Likely 1280x480 or 480x1280
**Purpose**: Boot splash screen / startup logo

This image is displayed during boot. Can be customized by:
1. Replacing the file with same name
2. Using password (112233) to access logo change menu
3. Copying new logo from USB to F:/

### Save/ Directory

Contains persistent user data that survives factory reset (depending on saveMethod).

#### SetupSave.bin

**Type**: Binary data structure
**Size**: 1,048 bytes
**Purpose**: Serialized system settings

Likely structure:
```c
struct SetupSave {
    uint32_t magic;           // 0x00: Magic number for validation
    uint32_t version;         // 0x04: Save format version
    uint32_t checksum;        // 0x08: CRC32 of data

    // User preferences (copied from Config.ini at save time)
    uint8_t brightness;       // 0x0C: Brightness level
    uint8_t contrast;         // 0x0D: Contrast level
    uint8_t hue;              // 0x0E: Hue value
    uint8_t saturation;       // 0x0F: Saturation value
    uint8_t language;         // 0x10: Language ID
    uint8_t volume;           // 0x11: Current volume

    // More settings...
    uint8_t reserved[1024];   // Reserved for future use
};
```

#### boot.bin

**Type**: Binary flags
**Size**: 10 bytes
**Purpose**: Boot state and flags

Possible contents:
```c
struct BootFlags {
    uint8_t boot_count;       // Number of boots
    uint8_t safe_mode;        // Safe mode flag
    uint8_t update_pending;   // Firmware update pending
    uint8_t factory_reset;    // Factory reset requested
    uint8_t flags[6];         // Additional flags
};
```

#### RadioSave.bin

**Type**: Binary radio presets
**Size**: 108 bytes
**Purpose**: Saved radio stations

Likely format:
```c
struct RadioSave {
    uint32_t magic;           // Magic: 'RDIO'
    uint16_t fm_presets[18];  // FM1/2/3: 6 stations each = 18
    uint16_t am_presets[12];  // AM1/2: 6 stations each = 12
    uint8_t last_band;        // Last selected band
    uint8_t last_preset;      // Last preset index
    uint16_t last_freq;       // Last frequency
    uint32_t checksum;        // CRC32
};
```

#### SdSave.dat

**Type**: Binary SD card cache
**Size**: 832 bytes
**Purpose**: SD card file listing cache

Speeds up media library scanning by caching directory structure.

#### VideoSave.bin

**Type**: Binary video settings
**Size**: 152 bytes
**Purpose**: Video playback preferences

Stores:
- Last played file path
- Playback position
- Zoom mode
- Brightness/contrast overrides

#### LinkSave.bin

**Type**: Binary link settings
**Size**: 28 bytes
**Purpose**: CarPlay/Android Auto state

Stores:
- Last connected device
- Connection preferences
- Audio routing

#### BT/ Directory

Contains Bluetooth pairing records.

##### 00B8B64F537F.pr

**Filename Format**: MAC address with colons removed + ".pr"
**Type**: Binary pairing record
**Size**: 197 bytes
**MAC Address**: 00:B8:B6:4F:53:7F

Pairing record structure:
```c
struct BTDeviceRecord {
    uint8_t mac_addr[6];      // Device MAC address
    char device_name[32];     // Device name
    uint8_t link_key[16];     // Pairing link key
    uint8_t device_type;      // Device type (phone/headset/etc)
    uint8_t trusted;          // Trusted device flag
    uint32_t last_seen;       // Last connection timestamp
    uint8_t services[8];      // Supported services bitmask
    uint8_t reserved[128];    // Reserved
};
```

### UI1/ and UI2/ Directories

Multiple UI theme support. Each contains a Config.ini with theme-specific overrides.

**UI Theme Selection**: Controlled by `uiID` in main Config.ini

Differences between themes might include:
- Color schemes
- Button layouts
- Icon sets
- Animation styles
- Language-specific layouts

## File Access

### Reading Files

```bash
# Mount FAT partition (Linux)
sudo mount -t vfat -o loop fat.img /mnt/fat
cat /mnt/fat/Config.ini

# Extract with 7-Zip (All platforms)
7z x fat.img
cat Config.ini

# Direct read with Python
import struct
with open('Save/SetupSave.bin', 'rb') as f:
    data = f.read()
    # Parse structure...
```

### Modifying Configuration

```bash
# 1. Extract partition
7z x fat.img

# 2. Edit Config.ini
nano Config.ini

# 3. Rebuild FAT image (requires mtools or mkfs.vfat)
# Option A: Using mtools
mcopy -i fat_new.img Config.ini ::Config.ini

# Option B: Rebuild from scratch
mkfs.vfat -F 16 -S 512 -s 1 -n "UDISK" fat_new.img 512
mount -o loop fat_new.img /mnt/fat
cp -r extracted_files/* /mnt/fat/
umount /mnt/fat
```

### Common Modifications

#### Change Default Source
```ini
[CONFIG]
defaultSource=BtMusic    # Change from Radio to Bluetooth
```

#### Enable AM Radio
```ini
[RADIO]
bAmEnable=1              # Enable AM band
bAmLocEnable=1           # Enable local stations
```

#### Adjust Volume Limits
```ini
[CONFIG]
maxVolume=30             # Increase max volume (default: 22)

[STARTUP]
startUpDefVolume=20      # Higher startup volume
startUpMaxVolume=30      # Higher max startup volume
```

#### Change Boot Logo Password
```ini
[CONFIG]
logoPassword=999999      # Change from 112233
```

#### Enable Debug Logging
```ini
[DEBUG]
bPrintLog=1
bPrintTouch=1            # Log touch events
bPrintThreadCpuLoad=1    # Log CPU usage
```

## Configuration Backup

It's recommended to backup the FAT partition before modifications:

```bash
# Backup entire partition
dd if=/dev/mmcblk0p3 of=fat_backup.img bs=512

# Or just backup Config.ini
mount /dev/mmcblk0p3 /mnt/fat
cp /mnt/fat/Config.ini Config.ini.backup
```

## Factory Reset

Factory reset behavior depends on `saveMethod` in Config.ini:

- **Method 0**: Keep all user data
- **Method 1**: Reset config only
- **Method 2**: Reset config and radio presets
- **Method 3**: Full reset (current setting)

Factory reset is triggered by:
1. Settings menu (requires password 113266)
2. Hardware button combination during boot
3. Setting flag in boot.bin

## Security Implications

⚠️ **Critical Security Issues:**

1. **Plaintext Passwords**: Both passwords stored in plaintext
2. **Weak Passwords**: Simple 6-digit numeric passwords
3. **Writable Configuration**: FAT partition is read/write
4. **No Encryption**: BT pairing keys stored unencrypted
5. **No Integrity Check**: Simple checksum, not cryptographic hash

**Recommendations:**
- Change default passwords immediately
- Disable debug logging in production
- Implement secure boot if possible
- Encrypt sensitive data (BT keys, WiFi passwords)

## References

- FAT16 Specification: Microsoft FAT File System Documentation
- INI File Format: https://en.wikipedia.org/wiki/INI_file

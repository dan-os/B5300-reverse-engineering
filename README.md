# B5300 CarPlay Reverse Engineering

This repository is a hobby attempt at reverse engineering the popular [B5300 CarPlay / Android Auto head unit](https://www.aliexpress.us/item/3256806677605382.html).

Any and all contribution is welcomed and encouraged!

> **[Notice]** Unforunately, I can't upload any decompiled firmware here (sorry!). However, the process to unpack the .bin yourself is trivial by following [these instructions](docs/2-unpacking-firmware.md).

There's a UART TX pad on the board, this outputs UART at 500k baud. Log from boot in logs folder.

You can access a shell using the UART, the startup.sh needs editing the comment out the insmod d:\apps\desktop.mod line and then rebuild and flash back otherwise the desktop.mod will be writing to the uart constantly.

On the back of the PCB there's what looks like an unpopulated connector, the RX, TX and GND can be found on here.
<img src="PXL_20251014_144721978.jpg" alt="Sample Image" width="400" height="300">

Orange is GND, Black is TX, Green is RX. After it has booted you'll have shell access. Obviously the desktop app doesn't automatically run anymore.

    insmod d:\apps\desktop.mod  

## Tutorials

- [1. How-To: Extract your firmware](docs/1-extracting-firmware.md)
- [2. How-To: Unpack the filesystem](docs/2-unpacking-firmware.md)
- [3. How-To: Repack the filesystem](docs/3-repacking-firmware.md)
- [4. How-To: Flash modified firmware](docs/4-flashing-firmware.md)

## Factory codes

Factory codes provide access to hidden pages in the Settings menu. Some are useless while others allow you to customise your device, e.g. by modifying the startup image or changing the UI style to your liking etc.

Here's an exhaustive list of factory codes I've found so far:

| Code     | Title               | Notes                            |
| -------- | ------------------- | -------------------------------- |
| `001106` | Interface selection | Interface style selection menu   |
| `112233` | Logo                | Startup image customization menu |
| `112345` | Debug               | Debugging menu                   |
| `113266` | Factory             | Advanced settings                |
| `123579` | Self examination    | Empty for me                     |
| `230762` | Interface selection | Empty for me                     |

More info on factory codes (including screenshots) can be found [here](docs/factory-codes.md).

## B5300 Specs

- **FCC ID:** [2BD44-B5300](https://fccid.io/2BD44-B5300)
- **Manufacturer:** Guangzhou Chechi Electronic Technology Co., Ltd.
- **SoC:** Allwinner F133-B
- **Operating System:** [Melis4.0 RTOS](https://github.com/usr-sse2/lindenis-v833-RTOS-melis-4.0)

## Sources & Credits

[This great forum thread dedicated to reversing a similar F133-based head unit](https://4pda.to/forum/index.php?showtopic=1059544)

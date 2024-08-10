# How-To: Extract the firmware

This tutorial explains how to dump the contents of the B5300 flash ROM to a .bin file which can be unpacked and decompiled later. An example unmodified firmware.bin from my own unit can be found [here](../firmware/examples/B5300/original/).

## Prerequisites

#### Hardware
- B5300 head unit (duh)
- CH341a programmer (or alternative): [link](https://www.aliexpress.us/w/wholesale-CH341a-programmer.html)
- SOIC8 programming clip (or probes): [clip](https://www.aliexpress.us/w/wholesale-SOIC8-clip.html), [probes](https://www.aliexpress.us/w/wholesale-test-hook-probes.html)

#### Software
- [flashrom](https://www.flashrom.org/) (or alternative): `brew install flashrom`

## Instructions

Disassemble the unit by removing the 4 small screws on the rear corners of the case to seperate the screen from the circuit. You may find it useful to run a guitar plectrum along the seam to remove any glue holding the parts together. Note that the delicate cable to the screen runs along the bottom so be careful not to damage it.

Locate the SPI flash ROM chip. Exact models will vary by batch but should all be compatible with this extraction method. In my case, this is a cFeon QH128A-104HIP (a [EN25QH128A](https://www.datasheets360.com/pdf/3768117275930620345) clone).

Attach the SOIC clip (or probes) to the chip, ensuring that pin 1 of the clip (red cable) is aligned with pin 1 on the chip, marked by the indent on the chip.

Attach the clip cable (or probes) to the programmer on the BIOS 25 SPI port ensuring that the orientation is correct (see image).

Dump the contents of the ROM using flashrom:
```bash
➜  ~ sudo flashrom --programmer ch341a_spi --read firmware.bin
```

Expected output:
```
flashrom 1.4.0 on Darwin 23.5.0 (arm64)
flashrom is free software, get the source code at https://flashrom.org

Found Eon flash chip "EN25QH128" (16384 kB, SPI) on ch341a_spi.
===
This flash part has status UNTESTED for operations: WP
The test status of this chip may have been updated in the latest development
version of flashrom. If you are running the latest development version,
please email a report to flashrom@flashrom.org if any of the above operations
work correctly for you with this flash chip. Please include the flashrom log
file for all operations you tested (see the man page for details), and mention
which mainboard or programmer you tested in the subject line.
You can also try to follow the instructions here:
https://www.flashrom.org/contrib_howtos/how_to_mark_chip_tested.html
Thanks for your help!
Reading flash... done.
```

You should now have `firmware.bin` file!

**But wait!** You must first verify that it was saved correctly by comparing the .bin against the contents of the chip once more. For me, it took 3 reads to produce a correct and valid dump. So, be certain yours is valid when you make your backup!

Verify the integrity of the saved .bin using flashrom:
```bash
sudo flashrom --programmer ch341a_spi --verify firmware.bin
```

Expected output:
```
flashrom 1.4.0 on Darwin 23.5.0 (arm64)
flashrom is free software, get the source code at https://flashrom.org

Found Eon flash chip "EN25QH128" (16384 kB, SPI) on ch341a_spi.
===
This flash part has status UNTESTED for operations: WP
The test status of this chip may have been updated in the latest development
version of flashrom. If you are running the latest development version,
please email a report to flashrom@flashrom.org if any of the above operations
work correctly for you with this flash chip. Please include the flashrom log
file for all operations you tested (see the man page for details), and mention
which mainboard or programmer you tested in the subject line.
You can also try to follow the instructions here:
https://www.flashrom.org/contrib_howtos/how_to_mark_chip_tested.html
Thanks for your help!
Verifying flash... VERIFIED.
```

Keep repeating the above process until your .bin is VERIFIED against the contents of the chip and then you can relax knowing you have a golden backup of the original! For next steps, see [unpacking instructions](2-unpacking-firmware.md).

### Important!

It's **crucial** to save a backup of the original .bin file so you can restore your device if something goes wrong later, so do this now! Don't say I didn't warn you! However, if the worst does happen you can find my copy [here](../firmware/examples/B5300/original/).

## Troubleshooting

### No device found
```
No EEPROM/flash device found.
Note: flashrom can never write if the flash chip isn't found automatically.
```

It's *very* likely that the SOIC clip isn't making good contact with the chip. It can be tricky to get seated so try and try again. If you're *certain* and have tested that the connection is good, it may be that your flash device isn't supported by the programmer (i.e. flashrom) and you will need to find an alternative that does.

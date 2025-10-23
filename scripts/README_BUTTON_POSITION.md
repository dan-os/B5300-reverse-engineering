# ButtonDot Position Modifier

This script allows you to modify the position of the menu overlay button (ButtonDot) in the Android-related UI data files.

## Files Affected

- `AndroidAuto.data` - Android Auto interface
- `AndroidWireless.data` - Android wireless mirroring
- `MirrorAndroid.data` - Android mirror mode

## Usage

### List all ButtonDot positions in a file:

```bash
./modify_button_position.py MirrorAndroid.data --list
```

Output:
```
ButtonDot positions in 'MirrorAndroid.data':
  [0] Offset 0x51c: X=1, Y=1, W=50, H=48
  [1] Offset 0x9a8: X=0, Y=1180, W=77, H=60
  [2] Offset 0x9ac: X=1180, Y=77, W=60, H=60
```

### Modify a ButtonDot position:

```bash
./modify_button_position.py <filename> <new_x> <new_y> [--index INDEX] [--no-backup]
```

**Examples:**

1. Move the main button in MirrorAndroid to position (100, 100):
   ```bash
   ./modify_button_position.py MirrorAndroid.data 100 100 --index 2
   ```

2. Move the button in AndroidAuto to position (500, 200):
   ```bash
   ./modify_button_position.py AndroidAuto.data 500 200 --index 0
   ```

3. Modify without creating a backup:
   ```bash
   ./modify_button_position.py MirrorAndroid.data 800 50 --index 2 --no-backup
   ```

## Parameters

- `<filename>` - The .data file to modify (required)
- `<new_x>` - New X coordinate in pixels (required)
- `<new_y>` - New Y coordinate in pixels (required)
- `--index INDEX` - Which ButtonDot instance to modify (default: 0)
- `--no-backup` - Skip creating a backup file
- `--list` or `-l` - List all ButtonDot positions without modifying

## Default Button Positions

### MirrorAndroid.data & AndroidWireless.data
- **Main button (index 2)**: X=1180, Y=77, Size=60×60px
  - This is the visible menu overlay button
  - Located in the upper-right corner

### AndroidAuto.data
- **Main button (index 0)**: X=237, Y=400, Size=100×30px
  - Different position for Android Auto mode
  - Wider, shorter button design

## Screen Dimensions

The device appears to use a **1280×720** display resolution based on the button positions.

## Backup Files

By default, the script creates a backup with the `.bak` extension before modifying:
- `MirrorAndroid.data.bak`
- `AndroidAuto.data.bak`
- `AndroidWireless.data.bak`

To restore from backup:
```bash
cp MirrorAndroid.data.bak MirrorAndroid.data
```

## Notes

- Coordinates use standard UI positioning: (0,0) is top-left corner
- The script automatically verifies changes after modification
- Multiple ButtonDot entries may exist per file (icons, different states)
- Use `--list` first to identify which index you want to modify
- Always test changes before deploying to the device

## Troubleshooting

**Q: Which index should I modify?**
A: Use `--list` to see all positions. The highest index with coordinates near (1180, 77) is typically the main visible button.

**Q: Button doesn't appear where I set it?**
A: Ensure coordinates are within screen bounds (0-1280 for X, 0-720 for Y)

**Q: Changes don't take effect?**
A: Make sure to deploy the modified .data file back to the device and restart the UI application.

` ./modify_button_position.py ../firmware/workspace/extracted/minfs/apps/Data/AndroidAuto.data 10 135 --index 3 --no-backup`
Worked for me to move the button from the RHS of the screen to the LHS by default. 
 

# REDROID-GO

REDROID-GO is an open-source, custom-designed handheld gaming console inspired by the original ODROID-GO. This project enhances the original (discontinued) design with modern features, while maintaining as much as possible full software compatibility.

## Features
- **USB-C Connector** – Modern power and data connectivity.
- **Optional IPS Display** – Upgrade to a vibrant IPS screen instead of the standard TFT.
- **100% Software Compatibility** – Works with ODROID-GO software (unfortunately, only when using the TFT display, see below).
- **Fully Open-Source** ❤️ – Schematics, PCB, and BOM included!

## Repository Contents
- **KiCad Project** – Includes schematic, PCB design, and layout.
- **Bill of Materials (BOM)** – All of the PCB components are sourced from LCSC. Other components, such as the display, speaker, battery, buttons need to be bought separately.
- **Assembly Instructions** – Step-by-step guide to build your REDROID-GO (coming soon).

### Branching Structure
The _master_ branch contains the latest, **unstable** version of the project, which has not been manufactured or tested yet. If you are looking for a stable and tested version, please refer to the **releases** section, where you can find previous working versions of REDROID-GO.

## Compatibility
The base idea is to keep the project as much software-compatible as possible to the original ODROID-GO. There are some caveats though:
- New ESP32-WROVERs require the setting `CONFIG_INT_WDT` set to `y` in ESP-IDF.
- When using the IPS display, the commands to initialize the display should include an additional `0x31`. This is because even if the IPS display uses the same driver IC as the TFT one, by default the colors are inverted.

## Contributing
Contributions are welcome! Feel free to submit pull requests or open issues to discuss improvements.

## Acknowledgments
Special thanks to **Hardkernel** for the original ODROID-GO design and the open-source community for keeping retro gaming alive.

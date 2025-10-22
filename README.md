
![logo](https://github.com/user-attachments/assets/940dbb1f-c628-4089-b30e-78433d526763)

REDROID-GO is an open-source, custom-designed handheld gaming console inspired by the original ODROID-GO. This project enhances the original (discontinued) design with modern features, while maintaining as much as possible software compatibility.

<img width="390" height="530" alt="redroid_go_front" src="https://github.com/user-attachments/assets/8ff2602d-4b23-446b-a254-f02d86409650" />
<img width="390" height="530" alt="redroid_go_bottom" src="https://github.com/user-attachments/assets/2bca3361-def3-498c-9aa0-8ef3de1df3ef" />




## Features
- **USB-C Connector** – Modern power and data connectivity.
- **Optional IPS Display** – Upgrade to a vibrant IPS screen instead of the standard TFT.
- **High Software Compatibility** – Works with ODROID-GO software, but unfortunately some patches may be required, see below.
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
- When using the IPS display, the commands to initialize it should include an additional `0x21`. This is because even if the IPS display uses the same driver IC as the TFT one, by default the colors are inverted.

## Hardware Fabrication

### Ordering the PCB
You can order the PCB directly from the `gerber.zip` release artifact using any common PCB manufacturer.<br>
Specs for ordering:
- **Thickness:** 1.6 mm, **required** to make it fit in the case
- **Finish:** ENIG is **strongly recommended**. ENIG provides a flatter and more durable pad surface than HASL, which ensures more consistent readings from the membrane buttons over time.

### Soldering the Components
All components can be soldered by hand.

**Tips**
- A regular soldering iron is sufficient — use a **thin tip** for finer control
- Apply **no-clean flux or thermal flux** to ease solder flow and avoid bridges
- **Start with the USB-C connector and the display connector** — they are the most difficult parts to solder; then proceed with the remaining components
- A **desoldering braid** can be very useful to wick away any excess solder or to correct bridges
- When done soldering, clean the PCB with **isopropyl alcohol (≥90% IPA)**, especially around the buttons’ pads, using a brush or lint-free wipe; let it dry fully before powering

## Contributing
Contributions are welcome! Feel free to submit pull requests or open issues to discuss improvements.

## Acknowledgments
Special thanks to **Hardkernel** for the original ODROID-GO design and the open-source community for keeping retro gaming alive. Thanks also to:
 -  [32teeth](https://github.com/32teeth) for the membrane buttons library.
 -  [DoganM95](https://github.com/DoganM95) and [snakeye](https://github.com/snakeye) for references on USB PD resistors and auto programming of the ESP32 (see [CH340C-Serial-Programmer](https://github.com/DoganM95/CH340C-Serial-Programmer) and [ch340g-esp32](https://github.com/snakeye/ch340g-esp32)).
 -  [ducalex](https://github.com/ducalex) for providing awesome software for the platform such as [odroid-go-multi-firmware](https://github.com/ducalex/odroid-go-multi-firmware) and [retro-go](https://github.com/ducalex/retro-go).

# Hardware Fabrication
<img width="964" height="1000" alt="image" src="https://github.com/user-attachments/assets/c1d60a4c-e20c-4b1a-9794-0d30412a038f" />

Building a REDROID-GO requires ordering a custom PCB, soldering ~70 components, and 3D printing (or outsourcing) the case.  
All design files are included in the repository (`pcb/` for KiCad, `case/` for FreeCAD) — Gerber & STL files are in the release assets for convenience.

**Estimated build time**  
With all tools and parts ready + intermediate soldering skills → one (rainy) weekend.

## 1. Ordering the PCB

Order the 2-layer PCB using the `gerber.zip` file from the latest release.

**Specifications (mandatory for proper fit):**
- Layers: 2
- Thickness: **1.6 mm** (critical for case fit)
- Surface finish: **ENIG** (strongly recommended) — much better pad flatness and long-term reliability for membrane button contacts than HASL
- Solder mask color: your choice (black looks great!)
- Silkscreen: optional but nice

## 2. Buying the components

Two BOMs (Bill Of Material) are provided:
- `BOM_redroid_go_LCSC.csv` → this is the list of all SMD components required for the board
- `BOM_redroid_go_AliExpress.csv` → additionals parts

## 3. Soldering the Components (Hand-soldering guide)

All parts are hand-solderable — no reflow oven required.
The board has several test points (TPx pads) that make progressive testing easy and strongly recommended.

**Difficulty:** Medium (USB-C & FPC connectors are the hardest parts)

**Recommended tools:**
- Soldering iron with **fine conical tip**
- Solder
- No-clean flux or thermal flux (essential!)
- Desoldering braid
- Isopropyl alcohol (≥90%) (for cleaning)
- Multimeter (for debugging)

**Soldering & testing order (progressive – test at each major stage!)**  
By following this order you minimize risk: if something fails, you know exactly where the problem is and haven't wasted time soldering the whole board yet.

1. **USB-C connector first**  
   Solder the USB-C port carefully (tack one corner pin, check alignment, then solder rest).  
   → **Test:** With a USB cable connected to a charger/PC, measure **~5V** between **TP14 (VBUS)** and **TP11 (GND)**.  
   No voltage → redo solder joints or check cable.

2. **LDO regulator for serial-to-USB converter**  
   Solder the LDO (U5) (and its surrounding capacitors).  
   → **Test:** Apply 5V via USB-C and measure **~3.3V** on **TP15**.  
   No/stable 3.3V → check polarity, bridges, or bad LDO.

3. **CH340 serial-to-USB converter IC**  
   Solder the CH340 + its caps.  
   → **Test:** Connect the board to a PC via USB. It should appear as a new COM port (Windows) or `/dev/ttyUSB*` (Linux/macOS).  
   Try both USB-C orientations — it must work flipped!  
   No recognition or recognition errors → check solder joints on the USB-C connector (on Linux, use `dmesg` to see the kernel logs)
   
5. **Buck converter + power switch**  
   Solder the buck converter IC and its surrounding components.  
   → **Test:** With USB power or battery connected, toggle the power switch and measure **~3.3V** on **TP1**.  
   Correct voltage → proceed safely. Wrong/missing voltage → fix before continuing.

6. **ESP32 module (U1) + reset circuitry**  
   Solder the ESP32 module, its surrounding capacitors, pull-ups/pull-downs, and **Q1** (automatic reset transistor for esptool.py).  
   → **Test:** Connect via USB, open a terminal and run:  
     ```bash
     esptool --port /dev/ttyUSB0 read-mac   # (or COMx on Windows)
     ```
     You should see the ESP32's MAC address. If communication works → great, the core programming path is functional!

7. **Display connector & backlight control**  
    Solder the display FPC connector + related parts (Q3, C10, R20, R26, R19, R25, R24).
    → Flash a simple test firmware (see Software section in the main README).
    If successful, you should see something on the screen.

8. **Remaining components**  
    Now solder the rest (exept the LEDs, see the Assembly section). These are lower risk once the core power/programming/display chain is verified.

**Extra practical tips:**
 - Use tweezers to place small components accurately.
 - Double-check orientation of polarized parts: ICs (notch/dot), diode D1, LEDs, etc. (capacitors used in the project and resistors have no polarity).
 - Solder one pin first, check alignment/flushness, then solder the remaining pins.
 - Tiny component labels are hard to read — use your smartphone camera zoomed in (macro mode helps a lot).
 - After all soldering: clean the entire board thoroughly with IPA (especially button pads) to remove flux residue — this prevents future button contact issues. Let it dry before powering.

**Test Points summary**
| Test Point |               Function / Description              |               Expected Value / Use Case              |         Typical Measurement Conditions            |
|:----------:|:-------------------------------------------------:|:----------------------------------------------------:|:-------------------------------------------------:|
| TP1        | 3.3V output from the main buck converter          | ≈ 3.3 V (stable when powered on)                     | Power switch ON, USB or battery connected         |
| TP2        | Vin to the buck converter (input voltage)         | ≈ 3.7–5.0 V (from battery or USB after diode/switch) | Power applied, before buck conversion, after fuse |
| TP3        | MENU button signal                                | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP4        | VOLUME button signal                              | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP5        | X-axis                                            | ~0–3.3 V (analog, 0 V idle)                          | Check continuity or voltage change on press       |
| TP6        | Y-axis                                            | ~0–3.3 V (analog, 0 V idle)                          | Check continuity or voltage change on press       |
| TP7        | SELECT button signal                              | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP8        | START button signal                               | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP9        | B button signal                                   | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP10       | A button signal                                   | Pulled high → ~3.3 V idle, drops to 0 V when pressed | Check continuity or voltage change on press       |
| TP11       | GND (ground reference)                            | 0 V reference                                        | Use as negative probe reference for all tests     |
| TP12       | GND (additional ground reference)                 | 0 V reference                                        | Extra convenient ground pad                       |
| TP13       | VBAT (battery voltage)                            | ≈ 3.7–4.2 V (typical LiPo range)                     | Battery connected, power switch OFF or ON         |
| TP14       | VUSB / VBUS (USB 5V input)                        | ≈ 4.8–5.2 V                                          | USB cable plugged into charger/PC                 |
| TP15       | 3.3V output from LDO (for CH340 serial converter) | ≈ 3.3 V (stable when USB powered)                    | USB connected (before main buck/power switch)     |

## 4. 3D Printing the Shell

Use the STL files from the `case.zip` release artifact (or the raw FreeCAD project in `case/` if you want to customize).

**Recommended print settings:**
- Material: **PETG** or **ABS** (PLA is too brittle)
- Layer height: 0.20 mm
- Infill: 20–25%
- Supports: yes for the front part, not required for the rear part
- Wall thickness: at least 3–4 perimeters
- Print orientation: flat on the bed

It is also possible to resin print the shell. Some great results were achieved both by outsourcing the print to commercial external services and with house printers.

Tip: Print the front piece first and test for proper fitting — small scaling errors can ruin assembly.

## 5. Assembly

This is the final stage: putting everything together!

### 5.1 Sharpening / Post-Processing the 3D Prints
3D-printed parts often suffer from the "elephant foot" effect, which can shrink button holes and make movement stiff.

- Test-fit all **buttons** into their sockets in the front shell.
- Check for smooth, friction-free travel when pressed.
- If tight → carefully **sharpen/enlarge** the holes using a **ceramic sharpening tool**, small round file, or hobby knife. Go slowly and test frequently.
- Also check the **LED holes** in the front shell. If too small, gently enlarge them with a **2 mm drill bit**.

### 5.2 Display Protection (Acrylic/plexiglass Panel)
This is the most precise and visible part of the build — take your time.

The recommended acrylic panel (from the BOM) starts at **60 × 60 mm** and needs to be cut to **60 × 50 mm** to fit the front shell recess perfectly.

1. **Do NOT remove** the protective films yet — they protect the surface during cutting and painting.
2. Measure and mark the cutting line accurately (use a metal ruler and fine marker).
3. Cut the panel (knife, fine-tooth saw, or laser if available).
4. Dry-fit the panel into the front shell recess — it should sit flush without gaps.
5. Use the front shell as a jig: with protective film still on, **mark** the exact areas to remain transparent (the display window) using a permanent marker (see example below).
   <img width="1440" height="1440" alt="image" src="https://github.com/user-attachments/assets/7185e085-878c-4059-9c60-5f3621548785" />
7. Carefully cut away and **remove the exterior protective film** (the part outside the marked window).
   <img width="1024" height="1024" alt="Untitled3" src="https://github.com/user-attachments/assets/fcd2aac9-b43b-4de2-a9fa-62d3effcd56d" />
8. **Spray paint** the exposed acrylic surface (black or dark color recommended for best contrast).
    <img width="1024" height="1024" alt="Untitled2" src="https://github.com/user-attachments/assets/c16ff788-9ffd-44cb-acc0-db5b92a7c00d" />
10. **Do NOT** remove the remaining interior film yet — it keeps the clear window dust-free until final gluing.

### 5.3 Installing the Display
1. Remove the protective film from the display (handle by edges only — avoid touching the active area).
2. Snap-fit the display into its socket in the front shell.
3. Apply small dots of **hot glue** at the corners/edges to secure it.
   <img width="1024" height="1600" alt="Untitled5" src="https://github.com/user-attachments/assets/7b7ddb81-2a8b-4e2e-bb23-e21865bca3fd" />
6. Apply **T7000 glue** (or equivalent) around the edges of the recess.
7. Remove the **remaining** internal protective film from the painted acrylic panel and carefully place it. Press gently and evenly — clamp lightly if needed.
8. Let cure (note that T7000 typically needs 24–48 hours for full strength).

### 5.4 Buttons, LEDs & PCB Installation
1. Place the **buttons** — they should sit flush and move freely.
2. Insert the **membrane contacts** into the front shell button sockets.
3. Position the two **LEDs** into their dedicated sockets in the front shell (mind polarity: longer leg = anode).
4. Carefully lower the **PCB** onto the front shell, aligning the screw holes and making sure LEDs enter their sockets properly.
5. Secure the PCB with the **two screws** (highlighted in blue in section 5.6). Use **6mm** length screws.
6. Double-check LED alignment, then **solder** the LED legs to the pads on the PCB.
7. Trim excess LED legs with flush cutters.
8. Connect the display.

### 5.5 Power Switch Modification
Replacement Game Boy Color power switches often come with an adapter that is too tall for REDROID-GO.

1. Cut/modify the adapter plastic part to match the shape shown in the reference picture (usually remove ~2–3 mm from the top/end).
2. Test-fit the modified switch — it should slide smoothly into its slot and actuate correctly.
   <img width="768" height="768" alt="Untitled7" src="https://github.com/user-attachments/assets/1be0bc78-1891-4133-a089-9c57b228cfbd" />


### 5.6 Battery & Speaker
1. Place the **speaker** into its cavity (speaker grille facing outward).
2. Insert the **battery** into its compartment.
3. Connect both to the corresponding connectors on the PCB.
   <img width="1024" height="1600" alt="Untitled6" src="https://github.com/user-attachments/assets/ee2974d6-0d96-4c2c-a7a8-fb8ac2c8bdfb" />


### 5.7 Closing the Case
1. Align the rear shell like turning a book page — this helps guide the modified power switch into its hole without bending.
2. Carefully bring the two halves together.
3. Insert and tighten the remaining screws (use **8mm** length screws).
   <img width="1600" height="900" alt="Untitled8" src="https://github.com/user-attachments/assets/465cfd0d-4f17-4859-be1f-56f9307fcf26" />



Good luck and have fun building your REDROID-GO!  

#!/usr/bin/env python3

# Created with the help of ChatGPT

import os
try:
    import FreeCAD
except:
    import freecad
import Mesh

in_file = 'case/redroid_go.FCStd'
out_dir = 'output/stl'

os.makedirs(out_dir, exist_ok=True)
doc = FreeCAD.openDocument(in_file)


front_nolabels = [
    doc.getObject('Body002'),
]

front_labels = front_nolabels.copy()
front_labels += [
    doc.getObject('Extrude'),
    doc.getObject('Extrude001'),
    doc.getObject('Extrude003'),
    doc.getObject('Extrude004'),
]

back = [
    doc.getObject('Body003'),
]


for obj, label in [(front_nolabels, 'front_nolabels'),
                   (front_labels, 'front'),
                   (back, 'back')]:
    export_path = os.path.join(out_dir, f"{label}.stl")
    Mesh.export(obj, export_path)
    print(f"Exported {label} -> {export_path}")

FreeCAD.closeDocument(doc.Name)

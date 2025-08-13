#!/usr/bin/env python3

# Created with the help of ChatGPT

import os
import FreeCAD
import Mesh

in_file = 'case/redroid_go.FCStd'
out_dir = 'output/stl'

os.makedirs(out_dir, exist_ok=True)
doc = FreeCAD.openDocument(in_file)

exported_count = 0
for obj in doc.Objects:
    print(obj.TypeId)
    if obj.TypeId == "PartDesign::Body":
        export_path = os.path.join(out_dir, f"{obj.Label}.stl")
        Mesh.export([obj], export_path)
        print(f"Exported {obj.Label} -> {export_path}")
        exported_count += 1

FreeCAD.closeDocument(doc.Name)

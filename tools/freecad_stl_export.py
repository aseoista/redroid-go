#!/usr/bin/env python3

# Created by ChatGPT

import os
import sys
import argparse



def export_bodies(input_file, output_dir, labels=None):
    """
    Export PartDesign::Body objects from a FreeCAD file to STL.
    
    :param input_file: Path to .FCStd file
    :param output_dir: Directory for output STL files
    :param labels: List of body labels to export (None means all bodies)
    """

    import freecad
    import Mesh
    
    os.makedirs(output_dir, exist_ok=True)
    doc = FreeCAD.openDocument(input_file)

    exported_count = 0
    for obj in doc.Objects:
        if obj.TypeId == "PartDesign::Body":
            if labels is None or obj.Label in labels:
                export_path = os.path.join(output_dir, f"{obj.Label}.stl")
                Mesh.export([obj], export_path)
                print(f"Exported {obj.Label} -> {export_path}")
                exported_count += 1

    FreeCAD.closeDocument(doc.Name)

    if exported_count == 0:
        print("No matching bodies found for export.")
        return 1
    elif labels is None or exported_count == len(labels):
        print(f"Done. Exported {exported_count} body(ies).")
        return 0
    else:
        print(f"Some bodies could not be found.")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Export FreeCAD bodies to STL."
    )
    parser.add_argument(
        "input_file",
        help="Path to the FreeCAD .FCStd file"
    )
    parser.add_argument(
        "output_dir",
        help="Directory to save STL files"
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        help="Labels of the bodies to export (default: all bodies)"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Input file not found: {args.input_file}")
        return 1

    return export_bodies(args.input_file, args.output_dir, args.labels)


if __name__ == "__main__":
    sys.exit(main())

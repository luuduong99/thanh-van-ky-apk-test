#!/usr/bin/env python3
"""Validate CP350 painting template structure. Passing does NOT indicate art is finished."""
import argparse, hashlib, io, zipfile
import xml.etree.ElementTree as ET
from PIL import Image

def check(path):
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, "ORA ZIP CRC failed"
        assert archive.read("mimetype") == b"image/openraster"
        root = ET.fromstring(archive.read("stack.xml"))
        assert (int(root.attrib["w"]),int(root.attrib["h"])) == (1290,2694)
        layers = list(root.find("stack"))
        assert len(layers) == 17
        assert sum(layer.attrib["name"].endswith("__PAINT") for layer in layers) == 15
        assert Image.open(io.BytesIO(archive.read("mergedimage.png"))).size == (1290,2694)
        for layer in layers:
            assert Image.open(io.BytesIO(archive.read(layer.attrib["src"]))).size == (1290,2694)
    print("CP350 ORA structure PASS: 17 layers, 15 empty paint targets; NOT art/rig QA")
if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("ora")
    check(p.parse_args().ora)

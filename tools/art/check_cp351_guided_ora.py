#!/usr/bin/env python3
"""Validate CP351 21-layer ORA handoff, not real art acceptance."""
import argparse
import io
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
from PIL import Image

def audit(original_package, updated_ora):
    with zipfile.ZipFile(original_package) as package:
        assert package.testzip() is None
        with zipfile.ZipFile(io.BytesIO(package.read('CP350_NATIVE_PAINTING_SCAFFOLD_NOT_ART_NOT_RIG.ora'))) as ref:
            assert ref.testzip() is None
            previous = ref.read('mergedimage.png')
    with zipfile.ZipFile(updated_ora) as z:
        assert z.testzip() is None
        layers = ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
        assert len(layers) == 21
        assert sum('__PAINT' in layer.attrib['name'] for layer in layers) == 15
        assert len([t for t in layers[:4] if t.attrib['visibility'] == 'hidden'
                    and t.attrib['name'].startswith(('18__', '19__', '20__', '21__'))]) == 4
        assert z.read('mergedimage.png') == previous
        assert Image.open(io.BytesIO(previous)).size == (1290, 2694)
        for i in range(15):
            px = np.asarray(Image.open(io.BytesIO(z.read(f'data/layer{i:02d}.png'))).convert('RGBA'))
            assert not np.any(px[:, :, 3]), f'Paint layer {i} is not blank'
    return 'PASS: 21 layers, 4 hidden QA guides, 15 blank painter layers, unchanged merged image. NOT painted art.'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cp350_package')
    parser.add_argument('cp351_ora')
    args = parser.parse_args()
    print(audit(args.cp350_package, args.cp351_ora))

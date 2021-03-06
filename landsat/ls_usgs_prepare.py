"""
Ingest data from the command-line.
"""
from __future__ import absolute_import

import uuid
import logging
import yaml
import re
import click
from osgeo import osr
import os
from pathlib import Path

images1 = [('1', 'coastal_aerosol'),
           ('2', 'blue'),
           ('3', 'green'),
           ('4', 'red'),
           ('5', 'nir'),
           ('6', 'swir1'),
           ('7', 'swir2'),
           ('8', 'panchromatic'),
           ('9', 'cirrus'),
           ('10', 'lwir1'),
           ('11', 'lwir2'),
           ('QUALITY', 'quality')]

images2 = [('1', 'blue'),
           ('2', 'green'),
           ('3', 'red'),
           ('4', 'nir'),
           ('5', 'swir1'),
           ('7', 'swir2'),
           ('QUALITY', 'quality')]

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin
    from urllib2 import urlopen

MTL_PAIRS_RE = re.compile(r'(\w+)\s=\s(.*)')


def _parse_value(s):
    s = s.strip('"')
    for parser in [int, float]:
        try:
            return parser(s)
        except ValueError:
            pass
    return s


def _parse_group(lines):
    tree = {}

    for line in lines:
        try:
            match = MTL_PAIRS_RE.findall(line.decode('utf-8'))
        except:
            match = MTL_PAIRS_RE.findall(line)
        if match:
            key, value = match[0]
            if key == 'GROUP':
                tree[value] = _parse_group(lines)
            elif key == 'END_GROUP':
                break
            else:
                tree[key] = _parse_value(value)
    return tree


def get_geo_ref_points(info):
    return {
        'ul': {'x': info['CORNER_UL_PROJECTION_X_PRODUCT'], 'y': info['CORNER_UL_PROJECTION_Y_PRODUCT']},
        'ur': {'x': info['CORNER_UR_PROJECTION_X_PRODUCT'], 'y': info['CORNER_UR_PROJECTION_Y_PRODUCT']},
        'll': {'x': info['CORNER_LL_PROJECTION_X_PRODUCT'], 'y': info['CORNER_LL_PROJECTION_Y_PRODUCT']},
        'lr': {'x': info['CORNER_LR_PROJECTION_X_PRODUCT'], 'y': info['CORNER_LR_PROJECTION_Y_PRODUCT']},
    }


def get_coords(geo_ref_points, spatial_ref):
    t = osr.CoordinateTransformation(spatial_ref, spatial_ref.CloneGeogCS())

    def transform(p):
        lon, lat, z = t.TransformPoint(p['x'], p['y'])
        return {'lon': lon, 'lat': lat}

    return {key: transform(p) for key, p in geo_ref_points.items()}


def satellite_ref(sat, file_name):
    """
    To load the band_names for referencing either LANDSAT8 or LANDSAT7 or LANDSAT5 bands
    Landsat7 and Landsat5 have same band names
    """
    name = (Path(file_name)).stem
    name_len = name.split('_')
    if sat == 'LANDSAT_8':
        sat_img = images1
    elif len(name_len) > 7:
        sat_img = images2
    else:
        sat_img = images2[:6]
    return sat_img


def get_mtl(path):
    """
    Path is pointing to the folder , where the USGS Landsat scene list in MTL format is downloaded
    from Earth Explorer or GloVis
    """
    newfile = "Empty File"
    metafile = "Name_of_File"
    for file in os.listdir(path):
        if file.endswith("MTL.txt"):
            metafile = file
            newfile = open(os.path.join(path, metafile), 'rb')
    return _parse_group(newfile)['L1_METADATA_FILE'], metafile


def prepare_dataset(path):
    info, fileinfo = get_mtl(path)
    # Copying [PRODUCT_METADATA] group into 'info_pm'
    info_pm = info['PRODUCT_METADATA']
    level = info_pm['DATA_TYPE']
    product_type = info_pm['DATA_TYPE']

    sensing_time = info_pm['DATE_ACQUIRED'] + ' ' + info_pm['SCENE_CENTER_TIME']

    cs_code = 32600 + info['PROJECTION_PARAMETERS']['UTM_ZONE']
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(cs_code)

    geo_ref_points = get_geo_ref_points(info_pm)
    satellite = info_pm['SPACECRAFT_ID']

    images = satellite_ref(satellite, fileinfo)
    return {
        'id': str(uuid.uuid5(uuid.NAMESPACE_URL, path)),
        'processing_level': level,
        'product_type': product_type,
        # 'creation_dt': ct_time,
        'label': info['METADATA_FILE_INFO']['LANDSAT_SCENE_ID'],
        'platform': {'code': satellite},
        'instrument': {'name': info_pm['SENSOR_ID']},
        # 'acquisition': {'groundstation': {'code': station}},
        'extent': {
            'from_dt': sensing_time,
            'to_dt': sensing_time,
            'center_dt': sensing_time,
            'coord': get_coords(geo_ref_points, spatial_ref),
        },
        'format': {'name': info_pm['OUTPUT_FORMAT']},
        'grid_spatial': {
            'projection': {
                'geo_ref_points': geo_ref_points,
                'spatial_reference': 'EPSG:%s' % cs_code,
                #     'valid_data': {
                #         'coordinates': tileInfo['tileDataGeometry']['coordinates'],
                #         'type': tileInfo['tileDataGeometry']['type']}
            }
        },
        'image': {
            'bands': {
                image[1]: {
                    'path': info_pm['FILE_NAME_BAND_' + image[0]],
                    'layer': 1,
                } for image in images
            }
        },
        'L1_METADATA_FILE': info,
        'lineage': {'source_datasets': {}},
    }


def absolutify_paths(doc, path):
    for band in doc['image']['bands'].values():
        band['path'] = os.path.join(path, band['path'])
    return doc

#\b is the backspace character
@click.command(help="""\b 
                    Prepare USGS Landsat Collection 1 data for ingestion into the Data Cube.
                    This prepare script supports only for MTL.txt metadata file
                    To Set the Path for referring the datasets -
                    Download the  Landsat scene data from Earth Explorer or GloVis into
                    'some_space_available_folder' and unpack the file.
                    For example: yourscript.py --output [Yaml- which writes datasets into this file for indexing]
                    [Path for dataset as : /home/some_space_available_folder/]""")
@click.option('--output', required=False, help="Write datasets into this file",
              type=click.Path(exists=False, writable=True, dir_okay=False))
@click.argument('datasets',
                nargs=-1)
def main(output, datasets):
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    if output:
        docs = (absolutify_paths(prepare_dataset(path), path) for path in datasets)
        with open(output, 'w') as stream:
            yaml.dump_all(docs, stream)
    else:
        raise RuntimeError('must specify --output')


if __name__ == "__main__":
    main()

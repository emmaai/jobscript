import sys
import fiona
import logging
import csv
from shapely.geometry import shape, box
from osgeo import ogr
from osgeo import gdal
from osgeo import osr


_LOG = logging.getLogger('test')
_LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
_LOG.addHandler(ch)

def tiles_from_shp(tile_file='Australian_Albers_Polygons.shp', shp_file=None):
    if shp_file is None:
        _LOG.error("need a shape file")
        return
    tile_list = set() 
    i = 0
    j = 0
    geo_box_list = list() 
    with fiona.open(shp_file) as polygons:
        for polygon in polygons:
            bound = shape(polygon['geometry']).bounds
            geo_box_list.append(box(bound[0], bound[1], bound[2], bound[3]))

    with fiona.open(tile_file) as tiles:
        for tile in tiles:
            for geo_box in geo_box_list:
                if geo_box.intersects(shape(tile['geometry'])):
                    tile_list.add(tile['properties']['label'])
                    break
    return list(tile_list)

def write_tiles_to_file(tile_list, tile_file='mangrove_tile_list'):
    with open(tile_file, 'w', newline='') as csvfile:
        csv_w = csv.writer(csvfile, delimiter=' ')
        for tile in tile_list:
            csv_w.writerow(tile.split(','))


def main(argv):
    _LOG.debug("shape file is %s"% (argv))
    tile_list = tiles_from_shp(shp_file=argv)
    _LOG.info(tile_list)
    write_tiles_to_file(tile_list)

if __name__ == '__main__':
    main(sys.argv[1])
                    

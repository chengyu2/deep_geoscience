import os
from unittest import TestCase

import numpy as np
from osgeo import gdal

from config import GlobalVars
from data_loader.ls_data_reader import LS7Reader


class TestLSDataReader(TestCase):

    def setUp(self):
        self.ls_dr = LS7Reader()

    def test_open_dir(self):
        dir_name = os.path.join(GlobalVars.PROJECT_ROOT, "landsat", "ls7_level1_scene")
        locations_data_points = self.ls_dr.open_dataset(dir_name=dir_name)
        print(locations_data_points)


    def test_convert_geotiff_to_array(self):
        ds = gdal.Open(
            "/Users/chengyu/PycharmProjects/deep_geoscience/landsat/ls7_level1_scene/LE07_L1TP_090084_20171014_20171015_01_RT/LE07_L1TP_090084_20171014_20171015_01_RT_B1.TIF")

        array_image = np.array(ds.GetRasterBand(1).ReadAsArray())
        self.assertIsInstance(array_image, np.ndarray)

        print(array_image.shape)

    def test_load_dataset(self):
        array_4d = self.ls_dr.load_dataset()
        self.assertEqual(array_4d.ndim, 4)
        print(array_4d.shape)



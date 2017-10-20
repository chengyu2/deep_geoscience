
import os

from osgeo import gdal
import numpy as np
from scipy.ndimage import zoom

from config import GlobalVars


class LSDataReader:

    def __init__(self, dataset_dir: str = ""):
        self.data_set_type = "dummy"
        self.dataset_dir = dataset_dir

    def load_dataset(self) -> np.ndarray:
        """
        Read from files to form a 4d array
        :return: (batch_id, band_id, height, width)
        """
        dir_datapoints = self.open_dataset(dir_name=self.dataset_dir)
        list_data_points = []
        for dir_datapoint in dir_datapoints:
            array_datapoint = self.create_3d_data_tensor(dir_datapoint=dir_datapoint)
            list_data_points.append(array_datapoint)
        return self.batch_data(list_data_points=list_data_points)



    def create_3d_data_tensor(self, dir_datapoint: str) -> np.ndarray:
        """

        :param dir_datapoint: dir location of a single datapoint
        :return:
        """
        raise NotImplementedError("Abstract method.")


    def convert_geotiff_to_array(self, dir_geotiff: str) -> np.ndarray:
        """

        :param dir_geotiff: Convert the dir name of a geotiff file into a numpy array
        :return:
        """
        ds = gdal.Open(dir_geotiff)
        array_image = np.array(ds.GetRasterBand(1).ReadAsArray())
        return array_image


    def batch_data(self, list_data_points: list) -> np.ndarray:
        return np.stack(list_data_points, axis=0)


    def open_dataset(self, dir_name: str) -> list:
        """

        :param dir_name:
        :return: a list of directories containing datapoints
        """
        dir_dataset = []
        files = os.listdir(path= dir_name)
        for file in files:
            file_path_abs = os.path.join(dir_name, file)
            if os.path.isdir(file_path_abs):
                dir_dataset.append(file_path_abs)
        return dir_dataset


class LS7Reader(LSDataReader):

    def __init__(self, data_set_type:str = "LE07_L1TP", dataset_dir: str = os.path.join(GlobalVars.PROJECT_ROOT, "landsat", "ls7_level1_scene")):
        super().__init__()
        self.data_set_type = data_set_type
        self.dataset_dir = dataset_dir
        self.band_mapping = {"B1":0, "B2":1, "B3":2, "B4":3, "B5":4, "B6_VCID_1":5, "B6_VCID_2": 6, "B7":7, "B8":8}


    def create_3d_data_tensor(self, dir_datapoint: str) -> np.ndarray:
        """
        Generate a 3d representation for a grid
        :param dir_datapoint:
        :return:
        """
        files = os.listdir(path=dir_datapoint)
        data_list = [None] * 9
        for file in files:
            geotiff_path_abs = os.path.join(dir_datapoint, file)

            for band in self.band_mapping:
                if band in geotiff_path_abs:
                    data_list[self.band_mapping[band]] = self.convert_geotiff_to_array(dir_geotiff=geotiff_path_abs)


        data_list[-1] = zoom(data_list[-1], 0.5, order=3)

        dim_0 = min([img.shape[0] for img in data_list])
        dim_1 = min([img.shape[1] for img in data_list])
        data_list = [img[:dim_0, :dim_1] for img in data_list]

        return np.stack(data_list, axis=0)







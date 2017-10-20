from unittest import TestCase
import os

from config import GlobalVars
from data_loader.sat_loader import Sat6Loader
from utils.file_util import FileUtil


class TestSatDataLoader(TestCase):
    def setUp(self):
        self.path_sat6 = os.path.join(GlobalVars.PROJECT_ROOT, "SAT-4_and_SAT-6_datasets", "sat-6-full.mat")
        self.sat_loader = Sat6Loader(data_set_path=self.path_sat6)



    def test_dataset(self):
        dataset = self.sat_loader._load_dataset(mat_file_path=self.path_sat6)
        print(dataset)
        print("Type of the loaded matlab dataset is {}".format(type(dataset)))
        print("Training set input shape is {}".format(dataset["train_x"].shape))
        print("Training set label shape is {}".format(dataset["train_y"].shape))
        print("Test set input shape is {}".format(dataset["test_x"].shape))
        print("Test set label shape is {}".format(dataset["test_y"].shape))

    def test_export_to_jpg(self):
        export_dir = os.path.join(GlobalVars.PROJECT_ROOT, "SAT-4_and_SAT-6_datasets", "inception_ready")
        FileUtil.validate_folder(folder_path=export_dir)
        self.sat_loader.export_to_inception_format(dataset=self.sat_loader.test_set, export_dir=export_dir)
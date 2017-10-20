from scipy.io import loadmat
from scipy.misc import toimage
import os
import numpy as np

from config import GlobalVars
from utils.file_util import FileUtil


class Sat6Loader:
    """
    References:
    DeepSat – A Learning framework for Satellite Imagery

    """

    def __init__(self, data_set_path: str):

        self._load_dataset(data_set_path)
        self.sat6_label = {0:"building", 1:"barren_land", 2:"trees", 3:"grassland", 4:"road", 5:"water"}

    def workflow(self):
        pass


    def _load_dataset(self, mat_file_path: str)->dict:
        """

        :param mat_file_path: a matlab path that should end in .mat format
        :return:
        """
        content = loadmat(mat_file_path)
        self.train_set = (content["train_x"], content["train_y"] )
        self.test_set = (content["test_x"], content["test_y"] )
        return content


    def export_to_inception_format(self, dataset: tuple, export_dir: str):
        """
        Inception training format is explained here:
        https://www.tensorflow.org/tutorials/image_retraining

        :return:
        """
        x, y = dataset
        assert x.shape[-1] == y.shape[-1] # batch size should equal
        for i in range(x.shape[-1]):
            img_array = x[:, :, :, i]
            label_one_hot = y[:, i]
            label = self.sat6_label[np.asscalar(np.where(label_one_hot==1)[0])]
            export_jpg_path = os.path.join(export_dir, label, '{}.jpg'.format(i))
            FileUtil.validate_file(file_path=export_jpg_path)
            toimage(img_array, channel_axis=2).save(export_jpg_path)
            if i%10000 == 0:
                print("{} images have been processed".format(i))


if __name__ == '__main__':

    sat6_loader = Sat6Loader(data_set_path=os.path.join(GlobalVars.PROJECT_ROOT, "SAT-4_and_SAT-6_datasets", "sat-6-full.mat"))
    images = np.concatenate((sat6_loader.train_set[0], sat6_loader.test_set[0]), axis=3)
    labels = np.concatenate((sat6_loader.train_set[1], sat6_loader.test_set[1]), axis=1)
    export_dir = os.path.join(GlobalVars.PROJECT_ROOT, "SAT-4_and_SAT-6_datasets", "inception_ready")
    sat6_loader.export_to_inception_format(dataset=(images, labels), export_dir=export_dir)



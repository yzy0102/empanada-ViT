import math
import cv2
import dask.array as da
from torch.utils.data import Dataset
from empanada.array_utils import take
from empanda.data.utils import resize_by_factor

class VolumeDataset(Dataset):
    def __init__(self, array, axis=0, tfs=None, scale=1):
        super(VolumeDataset, self).__init__()
        if not math.log(scale, 2).is_integer():
            raise Exception(f'Image rescaling must be log base 2, got {scale}')

        self.array = array
        self.axis = axis
        self.tfs = tfs
        self.scale = scale

    def __len__(self):
        return self.array.shape[self.axis]

    def __getitem__(self, idx):
        # load the image
        image = take(self.array, idx, self.axis)

        # if dask, then call compute
        if type(image) == da.core.Array:
            image = image.compute()

        # downsample image by scale
        image = resize_by_factor(image, self.scale)
        image = self.tfs(image=image)['image']

        return {'index': idx, 'image': image}

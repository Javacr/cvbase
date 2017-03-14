import cv2
import numpy as np

from cvbase.io import check_file_exist


def read_img(img_or_path):
    """Read an image

    Args:
        img_or_path(ndarray or str): either an image or path of an image
    Output:
        ndarray: image array
    """
    if isinstance(img_or_path, np.ndarray):
        return img_or_path
    elif isinstance(img_or_path, str):
        check_file_exist(img_or_path,
                         'img file does not exist: {}'.format(img_or_path))
        return cv2.imread(img_or_path)
    else:
        raise TypeError('"img" must be a numpy array or a filename')


def resize_keep_ar(img, max_long_edge, max_short_edge, return_scale=False):
    """Resize image with aspect ratio unchanged
    the long edge of resized image is no greater than max_long_edge, the short
    edge of resized image is no greater than max_short_edge.

    Args:
        img(ndarray): image or image path
        max_long_edge(int): max value of the long edge of resized image
        max_short_edge(int): max value of the short edge of resized image
    Output:
        tuple: (resized image, scale factor)
    """
    if max_long_edge < max_short_edge:
        raise ValueError(
            '"max_long_edge" should not be less than "max_short_edge"')
    img = read_img(img)
    h, w = img.shape[:2]
    scale = min(
        float(max_long_edge) / max(h, w), float(max_short_edge) / min(h, w))
    resized_img = cv2.resize(img, (int(w * scale), int(h * scale)))
    if return_scale:
        return resized_img, scale
    else:
        return resized_img


def limit_size(img, max_edge, return_scale=False):
    """Limit the size of an image
    If the long edge of the image is greater than max_edge, resize the image

    Args:
        img(ndarray): input image
        max_edge(int): max value of long edge
    Output:
        tuple: (resized image, scale factor)
    """
    img = read_img(img)
    h, w = img.shape[:2]
    if max(h, w) > max_edge:
        scale = float(max_edge) / max(h, w)
        resized_img = cv2.resize(img, (int(w * scale), int(h * scale)))
    else:
        scale = 1.0
        resized_img = img
    if return_scale:
        return resized_img, scale
    else:
        return resized_img

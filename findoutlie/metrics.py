""" Scan outlier metrics
"""

# Any imports you need
# +++your code here+++
import numpy as np


def dvars(img):
    """Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the mean of the (voxel differences squared)).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    # compute dvars and return
    return (np.diff(img.get_fdata(), axis=3) ** 2).mean(axis=(0, 1, 2)) ** 0.5

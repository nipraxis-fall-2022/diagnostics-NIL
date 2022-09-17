""" Scan outlier metrics
"""

# Any imports you need
import numpy as np
import nibabel as nib

from findoutlie.registration import euler_transform


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


def framewise_displacement(img):
    """Calculate framewise displacement metric on Nibabel image `img`

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    fd : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    # get the data
    data = img.get_fdata()

    # get the voxel sizes
    spacing = nib.affines.voxel_sizes(img.affine)

    # get image origin
    origin = img.affine[:3, 3]

    # use the first frame as the fixed image
    fixed = data[..., 0]

    # loop over the remaining frames and compute the displacement
    params = np.zeros((data.shape[3], 6))
    print("Computing motion parameters...")
    for i in range(1, data.shape[-1]):
        print(f"Registering frame: {i}", end="\r")
        # compute the transform
        transform = euler_transform(fixed, data[..., i], spacing, origin)

        # get the transform parameters, converting the angles to mm
        # using the 50 mm radius head assumption
        params[i, :] = np.array(transform.GetParameters()) * np.array([50, 50, 50, 1, 1, 1])
    print("\nDone.")

    # now compute the framewise displacement by computing difference between
    # nth and n-1th frames, and taking sum of the absolute values
    framewise_displacement = np.abs(np.diff(params, axis=0)).sum(axis=1)
    # framewise_displacement = np.insert(framewise_displacement, 0, 0)  # add zero to make up for first frame

    # return the framewise displacement
    return framewise_displacement


# if __name__ == "__main__":
#     import sys
#     img = nib.load(sys.argv[1])
#     print(framewise_displacement(img))

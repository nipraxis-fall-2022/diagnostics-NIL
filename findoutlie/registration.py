import numpy as np
import SimpleITK as sitk

from typing import Tuple


def command_iteration(method):
    print(
        f"{method.GetOptimizerIteration():3}, Metric: {method.GetMetricValue():7.5f}, "
        f"Convergence Value: {method.GetOptimizerConvergenceValue()}"
    )


def euler_transform(
    fixed: np.ndarray, moving: np.ndarray, spacing: Tuple[float], origin: Tuple[float], verbose: bool = False
) -> np.ndarray:
    """Does a rigid-body alignment between fixed and moving images.

    Parameters
    ----------
    fixed : np.ndarray
        Fixed image.
    moving : np.ndarray
        Moving image.
    spacing : np.ndarray
        Spacing (resolution) of the images.
    origin : np.ndarray
        Origin of the images.
    verbose : bool, optional
        Whether to print out the registration progress, by default False

    Returns
    -------
    np.ndarray
        The transformation parameters.
    """
    # convert to sitk objects
    fixed_img = sitk.GetImageFromArray(fixed)
    fixed_img.SetSpacing(spacing)
    fixed_img.SetOrigin(origin)
    moving_img = sitk.GetImageFromArray(moving)
    moving_img.SetSpacing(spacing)
    moving_img.SetOrigin(origin)

    # first level
    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetMetricAsCorrelation()
    registration_method.SetInterpolator(sitk.sitkLinear)
    registration_method.SetOptimizerAsGradientDescent(
        learningRate=5e-3,
        numberOfIterations=1000,
        estimateLearningRate=registration_method.EachIteration,
        convergenceMinimumValue=1e-6,
        convergenceWindowSize=10,
    )
    transform = sitk.Euler3DTransform()
    registration_method.SetInitialTransform(transform)
    if verbose:
        registration_method.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(registration_method))
    output_transform = registration_method.Execute(fixed_img, moving_img)

    # display status
    if verbose:
        print(output_transform)
        print(f"Stop condition: {registration_method.GetOptimizerStopConditionDescription()}")
        print(f"Iteration: {registration_method.GetOptimizerIteration()}")
        print(f"Metric value: {registration_method.GetMetricValue()}")

    # for debugging
    # resampler = sitk.ResampleImageFilter()
    # resampler.SetReferenceImage(fixed_img)
    # resampler.SetInterpolator(sitk.sitkLanczosWindowedSinc)
    # resampler.SetDefaultPixelValue(0)
    # resampler.SetTransform(output)
    # out_img = resampler.Execute(moving_img)
    # out = sitk.GetArrayFromImage(out_img)

    # return the transform
    return output_transform


# if __name__ == "__main__":
#     import sys
#     import nibabel as nib

#     fixed = nib.load(sys.argv[1])
#     moving = nib.load(sys.argv[2])
#     spacing = nib.affines.voxel_sizes(fixed.affine)
#     origin = fixed.affine[:3, 3]
#     out = euler_transform(fixed.get_fdata(), moving.get_fdata(), spacing, origin)
#     nib.Nifti1Image(out, fixed.affine).to_filename("out.nii.gz")

# Analysis plan

## Goal

Reject outliers from functional data.

## Methods

### DVARS

Already implemented.

### Framewise Displacement

Framewise Displacement (FD) is a measure indexing the movement of the head from one volume 
to the next. FD is computed by taking the frame-to-frame difference of the
displacement (sum of the absolute value of registration parameters):

$$ FD = \Delta_i - \Delta_{i-1} $$
$$ \Delta_i = \lvert\delta_{ix}\rvert + \lvert\delta_{iy}\rvert + \lvert\delta_{iz}\rvert + \lvert\delta_{i\alpha}\rvert + \lvert\delta_{i\beta}\rvert + \lvert\delta_{i\gamma}\rvert$$
$$ \delta_{i\nu} = \nu_i - \nu_{i-1} $$

where $\nu$ can be any of the six rigid-body parameters: $x$, $y$, $z$, $\alpha$, $\beta$, and $\gamma$ which represent the translation/rotation parameters of a rigid-body registration transform.

To compute FD, a rigid-body transform computation will need to be computed. A simple
way to do this (without invoking command-line application or code written in other languages) is with the [SimpleITK library](https://simpleitk.readthedocs.io/en/master/index.html). 

The rigid-body ([Euler3DTransform](https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1Euler3DTransform.html))
registration will be carried out using a [correlation](https://itk.org/Doxygen/html/classitk_1_1CorrelationImageToImageMetricv4.html) similarity metric along with a [gradient
descent optimizer](https://itk.org/Doxygen/html/classitk_1_1GradientDescentOptimizerv4Template.html). Though other optimizers may be
experimented with if time permits.

After obtaining the tranform parameters, FD will be computed as described above. Frames
will be rejected (censored) using a threshold criterion of 0.2 (standard in our lab).

## Assessing the outlier detection.

TBD

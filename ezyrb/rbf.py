"""Module for Radial Basis Function Interpolation."""

import numpy as np
from scipy.interpolate import RBFInterpolator
from .approximation import Approximation


class RBF(Approximation):
    """
    Multidimensional interpolator using Radial Basis Function.

    :param kernel: The radial basis function; the default is ‘multiquadric’.
    :type kernel: str or callable
    :param float smooth: values greater than zero increase the smoothness of
        the approximation. 0 is for interpolation (default), the function will
        always go through the nodal points in this case.
    :param int neighbors: if specified, the value of the interpolant at each
        evaluation point will be computed using only the nearest data points.
        If None (default), all the data points are used by default.
    :param float epsilon: Shape parameter that scales the input to the RBF.
        If kernel is ‘linear’, ‘thin_plate_spline’, ‘cubic’, or ‘quintic’, this
        defaults to 1 and can be ignored. Otherwise, this must be specified.
    :param int degree: Degree of the added polynomial. The default value is
        the minimum degree for kernel or 0 if there is no minimum degree.

    :cvar kernel: The radial basis function; the default is ‘multiquadric’.
    :cvar interpolator: the RBF interpolator

    :Example:

         >>> import ezyrb
         >>> import numpy as np
         >>>
         >>> x = np.random.uniform(-1, 1, size=(4, 2))
         >>> y = np.array([np.sin(x[:, 0]), np.cos(x[:, 1]**3)]).T
         >>> rbf = ezyrb.RBF()
         >>> rbf.fit(x, y)
         >>> y_pred = rbf.predict(x)
         >>> print(np.allclose(y, y_pred))

    """
    def __init__(self,
                 kernel='thin_plate_spline',
                 smooth=0,
                 neighbors=None,
                 epsilon=None,
                 degree=None):
        self.kernel = kernel
        self.smooth = smooth
        self.neighbors = neighbors
        self.degree = degree
        self.epsilon = epsilon
        self.interpolator = None
        self.xi = None

    def fit(self, points, values):
        """
        Construct the interpolator given `points` and `values`.

        :param array_like points: the coordinates of the points.
        :param array_like values: the values in the points.
        """
        self.xi = np.asarray(points)
        N = self.xi.shape[-1]

        if self.epsilon is None:
            # default epsilon is the "the average distance between nodes" based
            # on a bounding hypercube
            ximax = np.amax(self.xi, axis=0)
            ximin = np.amin(self.xi, axis=0)
            edges = ximax - ximin
            edges = edges[np.nonzero(edges)]
            self.epsilon = np.power(np.prod(edges)/N, 1.0/edges.size)
            if self.kernel in ['thin_plate_spline', 'cubic', 'quintic']:
                self.epsilon = 1

        self.interpolator = RBFInterpolator(
            points,
            values,
            neighbors=self.neighbors,
            smoothing=self.smooth,
            kernel=self.kernel,
            epsilon=self.epsilon,
            degree=self.degree)

    def predict(self, new_point):
        """
        Evaluate interpolator at given `new_points`.

        :param array_like new_points: the coordinates of the given points.
        :return: the interpolated values.
        :rtype: numpy.ndarray
        """
        return self.interpolator(np.asarray(new_point))

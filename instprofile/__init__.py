import sys
import numpy as np

def peakdet(y_vector, delta, x_vector = None):
    """
    Obtains the peaks and valleys of a vector.

    The original function was created in MATLAB by Eli Billauer and translated
    to python by @endolith (https://gist.github.com/endolith/250860).

    It the last value is a peak, it will not detect it.

    Parameters
    ----------

    y_vector: list;
        Vctor containing the ordinate.

    delta: float;
        The peak threshold. It is required at least a difference of `delta`
        between a peak and its surrounding to declare it as a peak. Same goes
        with valleys.

    x_vector: list (optional);
        The vector's X-axis values can be passed as a third argument (thanks to
        Sven Billiet for his contribution on this), in which case peakdet()
        returns these values instead of indices

    Returns
    -------

    The returned vectors "maxtab" and "mintab" contain the peak and valley
    points.
    """

    maxtab = []
    mintab = []

    if x_vector is None:
        x_vector = np.arange(len(y_vector))

    y_vector = np.asarray(y_vector)

    if len(y_vector) != len(x_vector):
        sys.exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    for i in np.arange(len(y_vector)):
        this = y_vector[i]
        if this > mx:
            mx = this
            mxpos = x_vector[i]
        if this < mn:
            mn = this
            mnpos = x_vector[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x_vector[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x_vector[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)

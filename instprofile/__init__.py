"""
Instrumental Profile
====================

When one observes the spectrum of a source of light, the x-axis of the
spectrum is in pixels. To convert this to wavelengths, it is used a spectrum
of a well know source of light, e.g., the light of a lamp of ThAr. The
spectrum of the lamp has known emission lines, thus it is possible to convert
from pixel to wavelength.

From theory, the emission lines of the lamp spectrum should be infinitely
narrow. Unfortunately, this does not happens because of the optics of the
instrument, which broadens the spectrum. When studying spectral lines of
unknown sources, this broadening effect has to be considered.

For an example of how to use it, see this `link`__.

__ http://nbviewer.ipython.org/urls/raw.githubusercontent.com/gabraganca/instprofile/master/example/Instrumental_Profile.ipynb
"""
import sys
import numpy as np
from scipy.optimize import leastsq

__version__ = "0.0.1"

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


def fit_gauss(x_vector, y_vector, guess):
    """
    Fit a gaussian to the data. It is very sensible to the guessed value of
    the mean.

    Parameters
    ----------

    x_vector: list;
        Vector with the abscissa.

    y_vector: list;
        Vector with the ordinate.

    guess: list;
        List with guessed values. The values are [peak, mean, standard_deviation].
    """

    gauss_fit = lambda p, x: p[0]*(1/np.sqrt(2*np.pi*(p[2]**2)))*\
                             np.exp(-(x-p[1])**2/(2*p[2]**2)) #1d Gaussian func
    e_gauss_fit = lambda p, x, y: (gauss_fit(p, x) - y) #1d Gaussian fit

    out = leastsq(e_gauss_fit, guess, args=(x_vector, y_vector), maxfev=100000,
                  full_output=1) #Gauss Fit


    # normalization factor p[0], mean p[1], standard deviation p[2].
    a , mu, sigma = out[0]

    return a, mu, sigma


def find_fit(x_vector, y_vector, delta):
    """
    Finds the peaks in the vector and fits gaussian for each peak

    Parameters
    ----------

    x_vector: list;
        A list with the abscissa

    y_vector: list;
        A list with the ordinate.

    delta: float;
        The peak threshold. It is required at least a difference of `delta`
        between a peak and its surrounding to declare it as a peak. Same goes
        with valleys.

    Returns
    -------

    A numpy array with three columns and the number the lines corresponds
    to each peak fitted. The thre columns are respectrively, the peak, mean
    and standard deviation from the gaussian fits.

    """
    means_found, peaks_found = peakdet(y_vector, delta, x_vector)[0].T
    # print means_found, peaks_found


    values_fit = np.array([fit_gauss(x_vector, y_vector,
                                     [peaks_found[i], means_found[i], 0.1])
                           for i in range(len(means_found))])

    # Get real peak

    values_fit[:, 0] = values_fit[:,0]*(1/np.sqrt(2*np.pi*(values_fit[:,2]**2)))

    return values_fit


def fwhm(stdev):
    """
    Obtain the full width at half maximum from a Gaussian obtained from the standard deviation.

    Equation obtained from http://en.wikipedia.org/wiki/Full_width_at_half_maximum.

    Parameters
    ----------

    stdev: float, list;
        Standard deviation.

    Returns
    -------

    The full width at half maximum value.
    """

    if isinstance(stdev, list):
        stdev = np.array(stdev)

    return 2*np.sqrt(2*np.log(2))*stdev


def inst_profile(wave_vector, flux_vector, delta, upper_lim=None):
    """
    Obtain the instrumental profile from a spectrum.

    The instrumental profile is defined as the full width at half maximum
    (FWHM) of the emission lines from a spectrum of a lamp. The algorithm finds
    the emission lines, fits a gaussian for each of them and return the FWHM of
    each emission line.

    Parameters
    ----------

    wave_vector: list;
        Vector with the values of the wavelengths.

    flux_vector: list;
        Vector with the flux of the spectrum

    delta: float;
        The peak threshold. It is required at least a difference of `delta`
        between a peak and its surrounding to declare it as a peak. Same goes
        with valleys.

    upper_lim: float (Optional);
        Sometimes the fit is not perfect and very high values for FWHM are
        found. This make a upper cut on the values.

    Returns
    -------

    A numpy.ndarray with the two columns, in wich each one of them are, respectively,
    the wavelength of the emission line and the FWHM of the emissions lines detected.
    """

    values = find_fit(wave_vector, flux_vector, delta)

    inst_profile  = np.zeros([len(values), 2], float)


    inst_profile[:,0] = values[:,1] # Abscissa
    inst_profile[:,1] = fwhm(values[:,2]) # Instrumental profile


    # Reject negative values, i.e., bad fits
    cond_neg = (inst_profile[:,0] > 0) & (inst_profile[:,1] > 0)

    inst_profile = inst_profile[cond_neg]

    if isinstance(upper_lim, (int, float)):
        cond = inst_profile[:,1] < upper_lim
        inst_profile = inst_profile[cond]


    return inst_profile

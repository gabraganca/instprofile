Instrumental Profile
====================

When one observes the spectrum of a source of light, the x-axis of the spectrum
is in pixels. To convert this to wavelengths, it is used a spectrum of a well
know source of light, e.g., the light of a lamp of ThAr. The spectrum of the
lamp has known emission lines, thus it is possible to convert from pixel to
wavelength.

From theory, the emission lines of the lamp spectrum should be infinitely
narrow. Unfortunately, this does not happens because of the optics of the
instrument, which broadens the spectrum. When studying spectral lines of
unknown sources, this broadening effect has to be considered.

Installation
------------

The only dependency is `numpy <http://www.numpy.org/>`_. To install it, clone or
download this repository and then:

::

    python setup.py install


or:

::

    python setup.py build
    pip install .


How to use it
-------------

I made an `IPython notebook`__ showing how one can obtain the instrumental
profile from a lamp spectrum. I used a spectrum of a real lamp to show it.

__ http://nbviewer.ipython.org/urls/raw.githubusercontent.com/gabraganca/instprofile/master/example/Instrumental_Profile.ipynb

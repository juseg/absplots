.. Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Absplots
========

.. Here come badges after the first release
   .. image:: https://img.shields.io/pypi/v/absplots.svg
      :target: https://pypi.python.org/pypi/absplots
   .. image:: https://img.shields.io/pypi/l/absplots.svg
      :target: https://www.gnu.org/licenses/gpl-3.0.txt
   .. image:: https://zenodo.org/badge/0000000.svg
      :target: https://zenodo.org/badge/latestdoi/0000000

Matplotlib_ subplots with absolute margins in mm or inches.

Installation::

   pip install absplots

Example usage::

   import absplots as apl

   # init 150x100 mm figure with 5 mm margins between and around subplots
   fig, grid = apl.subplots_mm(figsize=(150, 100), nrows=2, ncols=2,
                               gridspec_kw=dict(left=5, right=5, wspace=5,
                                                bottom=5, top=5, hspace=5))

.. _matplotlib: https://matplotlib.org

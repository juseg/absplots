# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Matplotlib subplots with absolute margins in mm or inches.
"""

import matplotlib.pyplot as plt
import matplotlib.figure as mfig


# Custom figure class
# -------------------

class AbsFigure(mfig.Figure):
    """Custom figure class allowing absolute subplot dimensioning."""

    def _process_kw_inches(self, nrows, ncols, gridspec_kw):
        """Convert gridspec keywords from inches to relative."""

        # get figure dimensions in inches
        figw, figh = self.get_size_inches()

        # get default gridspec params
        # FIXME it would be more logical to read defaults as ratios not inches
        if gridspec_kw is None:
            gridspec_kw = {}
        left = gridspec_kw.pop('left', self.subplotpars.left)
        right = gridspec_kw.pop('right', self.subplotpars.right)
        bottom = gridspec_kw.pop('bottom', self.subplotpars.bottom)
        top = gridspec_kw.pop('top', self.subplotpars.top)
        wspace = gridspec_kw.pop('wspace', self.subplotpars.wspace)
        hspace = gridspec_kw.pop('hspace', self.subplotpars.hspace)

        # normalize inner spacing to axes dimensions
        if wspace != 0.0:
            wspace = (((figw-left-right)/wspace+1)/ncols-1)**(-1)
        if hspace != 0.0:
            hspace = (((figh-bottom-top)/hspace+1)/nrows-1)**(-1)

        # normalize outer margins to figure dimensions
        gridspec_kw.update(left=left/figw, right=1-right/figw,
                           bottom=bottom/figh, top=1-top/figh,
                           wspace=wspace, hspace=hspace)

        # return processed keywords
        return gridspec_kw

    def _process_kw_mm(self, nrows, ncols, gridspec_kw):
        """Convert gridspec keywords from mm to relative."""

        # convert all non null arguments to inches
        mm = 1/25.4
        if gridspec_kw is not None:
            for dim in ['left', 'right', 'bottom', 'top', 'wspace', 'hspace']:
                if dim in gridspec_kw:
                    gridspec_kw[dim] *= mm

        # convert from inches to relative
        gridspec_kw = self._process_kw_inches(nrows, ncols, gridspec_kw)

        # return processed keywords
        return gridspec_kw

    def add_axes_inches(self, rect, **kwargs):
        """
        Create new axes with dimensions in inches.

        Parameters
        ----------
        rect : list of float
            The dimensions [left, bottom, width, height] of the new axes in
            inches.
        **kwargs :
            Additional keyword arguments are passed to
            :meth:`matplotlib.figure.Figure.add_axes`.
        """
        figw, figh = self.get_size_inches()
        rect = [rect[0]/figw, rect[1]/figh, rect[2]/figw, rect[3]/figh]
        return self.add_axes(rect, **kwargs)

    def add_axes_mm(self, rect, **kwargs):
        """
        Create new axes with dimensions in millimeters.

        Parameters
        ----------
        rect : list of float
            The dimensions [left, bottom, width, height] of the new axes in
            millimeters.
        **kwargs :
            Additional keyword arguments are passed to
            :meth:`matplotlib.figure.Figure.add_axes`.
        """
        return self.add_axes_inches([x/25.4 for x in rect], **kwargs)

    def add_gridspec_inches(self, nrows, ncols, **kwargs):
        """
        Create new gridspec with dimensions in inches.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.
        ncols : int
            Number of columns in grid.
        **kwargs :
            Additional gridspec keyword arguments read as absolute values in
            inches and passed to :meth:`matplotlib.figure.Figure.add_gridspec`.
        """

        # convert gridspec keywords
        kwargs = self._process_kw_inches(nrows, ncols, kwargs)

        # return new gridspec
        return self.add_gridspec(nrows=nrows, ncols=ncols, **kwargs)

    def add_gridspec_mm(self, nrows, ncols, **kwargs):
        """
        Create new gridspec with dimensions in millimeters.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.
        ncols : int
            Number of columns in grid.
        **kwargs :
            Additional gridspec keyword arguments read as absolute values in
            mm and passed to :meth:`matplotlib.figure.Figure.add_gridspec`.
        """

        # convert gridspec keywords
        kwargs = self._process_kw_mm(nrows, ncols, kwargs)

        # return new gridspec
        return self.add_gridspec(nrows=nrows, ncols=ncols, **kwargs)

    def get_size_mm(self):
        """Returns the current size of the figure in mm as an numpy array."""
        return self.get_size_inches()*25.4

    def subplots_inches(self, nrows=1, ncols=1, gridspec_kw=None, **kwargs):
        """
        Add a set of subplots to this figure with dimensions in inches.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.
        ncols : int
            Number of columns in grid.
        gridspec_kw : dict
            Dictionary containing any of the gridspec keywords (left, right,
            top, bottom, wspace, hspace, width_ratios, height_ratios) where all
            dimensions are interpreted as absolute values in inches.
        **kwargs :
            Additional keyword arguments are passed to
            :meth:`matplotlib.figure.Figure.subplots`.
        """

        # convert gridspec keywords
        gridspec_kw = self._process_kw_inches(nrows, ncols, gridspec_kw)

        # create subplots
        return self.subplots(nrows=nrows, ncols=ncols,
                             gridspec_kw=gridspec_kw, **kwargs)

    def subplots_mm(self, nrows=1, ncols=1, gridspec_kw=None, **kwargs):
        """
        Add a set of subplots to this figure with dimensions in millimeters.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.
        ncols : int
            Number of columns in grid.
        gridspec_kw : dict
            Dictionary containing any of the gridspec keywords (left, right,
            top, bottom, wspace, hspace, width_ratios, height_ratios) where all
            dimensions are interpreted as absolute values in millimeters.
        **kwargs :
            Additional keyword arguments are passed to
            :meth:`matplotlib.figure.Figure.subplots`.
        """

        # convert gridspec keywords
        gridspec_kw = self._process_kw_mm(nrows, ncols, gridspec_kw)

        # create subplots
        return self.subplots(nrows=nrows, ncols=ncols,
                             gridspec_kw=gridspec_kw, **kwargs)


# Figure helper functions
# -----------------------

def figure(**kwargs):
    """Create a new figure with dimensions in inches."""

    # by default select custom figure class
    figure_class = kwargs.pop('FigureClass', AbsFigure)

    # create a new figure
    fig = plt.figure(FigureClass=figure_class, **kwargs)
    return fig


def figure_mm(figsize=None, **kwargs):
    """Create a new figure with dimensions in mm."""

    # convert figure size to mm
    mm = 1/25.4
    if figsize is not None:
        figw, figh = figsize
        figsize = (figw*mm, figh*mm)

    # create new figure
    fig = figure(figsize=figsize, **kwargs)
    return fig


# Subplot helper functions
# ------------------------

def subplots_inches(nrows=1, ncols=1, **kwargs):
    """Create figure and subplots with dimensions in inches."""

    # segregate subplots and figure keywords
    spl_keys = ['sharex', 'sharey', 'squeeze', 'subplot_kw', 'gridspec_kw']
    spl_kw = {key: kwargs[key] for key in kwargs if key in spl_keys}
    fig_kw = {key: kwargs[key] for key in kwargs if key not in spl_keys}

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots_inches(nrows=nrows, ncols=ncols, **spl_kw)
    return fig, axs


def subplots_mm(nrows=1, ncols=1, **kwargs):
    """Create figure and subplots with dimensions in mm."""

    # segregate subplots and figure keywords
    spl_keys = ['sharex', 'sharey', 'squeeze', 'subplot_kw', 'gridspec_kw']
    spl_kw = {key: kwargs[key] for key in kwargs if key in spl_keys}
    fig_kw = {key: kwargs[key] for key in kwargs if key not in spl_keys}

    # create new figure and axes
    fig = figure_mm(**fig_kw)
    axs = fig.subplots_mm(nrows=nrows, ncols=ncols, **spl_kw)
    return fig, axs

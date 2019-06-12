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

    def add_axes_inches(self, rect, **kwargs):
        """
        Create new axes with dimensions in inches.

        Parameters
        ----------
        rect : list of float
            The dimensions [left, bottom, width, height] of the new axes in
            inches.
        **kwargs:
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
        **kwargs:
            Additional keyword arguments are passed to
            :meth:`matplotlib.figure.Figure.add_axes`.
        """
        return self.add_axes_inches([x/25.4 for x in rect], **kwargs)

    def get_size_mm(self):
        """Returns the current size of the figure in mm as an numpy array."""
        return self.get_size_inches()*25.4

    def subplots_inches(self, nrows=1, ncols=1, gridspec_kw=None, **kwargs):
        """Create subplots with dimensions in inches."""

        # get figure dimensions in inches
        figw, figh = self.get_size_inches()

        # get default gridspec params
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

        # create subplots
        return mfig.Figure.subplots(self, nrows=nrows, ncols=ncols,
                                    gridspec_kw=gridspec_kw, **kwargs)

    def subplots_mm(self, gridspec_kw=None, **kwargs):
        """Create subplots with dimensions in mm."""

        # convert all non null arguments to inches
        mm = 1/25.4
        if gridspec_kw is not None:
            for dim in ['left', 'right', 'bottom', 'top', 'wspace', 'hspace']:
                if dim in gridspec_kw:
                    gridspec_kw[dim] *= mm

        # create subplots
        return self.subplots_inches(gridspec_kw=gridspec_kw, **kwargs)


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

def subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
             subplot_kw=None, gridspec_kw=None, projection=None, **fig_kw):
    """Same as matplotlib function but allow a projection argument."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
                       squeeze=squeeze, subplot_kw=subplot_kw,
                       gridspec_kw=gridspec_kw)
    return fig, axs


def subplots_inches(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                    subplot_kw=None, gridspec_kw=None, projection=None,
                    **fig_kw):
    """Create figure and subplots with dimensions in inches."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots_inches(nrows=nrows, ncols=ncols, sharex=sharex,
                              sharey=sharey, squeeze=squeeze,
                              subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    return fig, axs


def subplots_mm(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                subplot_kw=None, gridspec_kw=None, projection=None, **fig_kw):
    """Create figure and subplots with dimensions in mm."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure_mm(**fig_kw)
    axs = fig.subplots_mm(nrows=nrows, ncols=ncols, sharex=sharex,
                          sharey=sharey, squeeze=squeeze,
                          subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    return fig, axs

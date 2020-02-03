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

        # if None provided, return None
        if gridspec_kw is None:
            return gridspec_kw

        # get figure dimensions in inches
        figw, figh = self.get_size_inches()

        # convert outer margins to ratios
        if 'left' in gridspec_kw:
            gridspec_kw['left'] = gridspec_kw['left'] / figw
        if 'right' in gridspec_kw:
            gridspec_kw['right'] = 1 - gridspec_kw['right'] / figw
        if 'bottom' in gridspec_kw:
            gridspec_kw['bottom'] = gridspec_kw['bottom'] / figh
        if 'top' in gridspec_kw:
            gridspec_kw['top'] = 1 - gridspec_kw['top'] / figh

        # normalize inner spacing to axes dimensions
        if 'wspace' in gridspec_kw and gridspec_kw['wspace'] != 0.0:
            left = gridspec_kw.get('left', self.subplotpars.left)
            right = gridspec_kw.get('right', self.subplotpars.right)
            gridspec_kw['wspace'] = (
                (figw*(right-left)/gridspec_kw['wspace']+1)/ncols-1)**(-1)
        if 'hspace' in gridspec_kw and gridspec_kw['hspace'] != 0.0:
            bottom = gridspec_kw.get('bottom', self.subplotpars.bottom)
            top = gridspec_kw.get('top', self.subplotpars.top)
            gridspec_kw['hspace'] = (
                (figh*(top-bottom)/gridspec_kw['hspace']+1)/nrows-1)**(-1)

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

        Returns
        -------
        axes : :class:`matplotlib.axes.Axes` (or a subclass)
            The newly created axes, whose class depends on the projection used.
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

        Returns
        -------
        axes : :class:`matplotlib.axes.Axes` (or a subclass)
            The newly created axes, whose class depends on the projection used.
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

        Returns
        -------
        gridspec : :class:`matplotlib.gridspec.GridSpec`
            The newly created gridspec.
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

        Returns
        -------
        gridspec : :class:`matplotlib.gridspec.GridSpec`
            The newly created gridspec.
        """

        # convert gridspec keywords
        kwargs = self._process_kw_mm(nrows, ncols, kwargs)

        # return new gridspec
        return self.add_gridspec(nrows=nrows, ncols=ncols, **kwargs)

    def get_size_mm(self):
        """
        Returns the current size of the figure in millimeters.

        Returns
        -------
        size : ndarray
            The size (width, height) of the figure in millimeters.
        """
        return self.get_size_inches()*25.4

    def get_position_inches(self, ax=None, original=True):
        """
        Returns axes position in inches (is this useful?).

        Parameters
        ----------
        original : bool
            If True, return the original position. Otherwise return the active
            position. See :meth:`matplotlib.axes.Axes.get_position`.

        Returns
        -------
        pos : [left, bottom, width, height]
            The axes position in inches.
        """
        ax = ax or self.gca()
        figw, figh = self.get_size_inches()
        pos = ax.get_position(original=original)
        return [pos.x0*figw, pos.y0*figh,
                (pos.x1-pos.x0)*figw, (pos.y1-pos.y0)*figh]

    def get_position_mm(self, ax=None, original=True):
        """
        Returns axes position in millimeters (is this useful?).

        Parameters
        ----------
        original : bool
            If True, return the original position. Otherwise return the active
            position. See :meth:`matplotlib.axes.Axes.get_position`.

        Returns
        -------
        pos : [left, bottom, width, height]
            The axes position in millimeters.
        """
        ax = ax or self.gca()
        figw, figh = self.get_size_mm()
        pos = ax.get_position(original=original)
        return [pos.x0*figw, pos.y0*figh,
                (pos.x1-pos.x0)*figw, (pos.y1-pos.y0)*figh]

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

        Returns
        -------
        axes : :class:`matplotlib.axes.Axes` or an array of axes
            The newly created subplot(s).
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

        Returns
        -------
        axes : :class:`matplotlib.axes.Axes` or an array of axes
            The newly created subplot(s).
        """

        # convert gridspec keywords
        gridspec_kw = self._process_kw_mm(nrows, ncols, gridspec_kw)

        # create subplots
        return self.subplots(nrows=nrows, ncols=ncols,
                             gridspec_kw=gridspec_kw, **kwargs)


# Figure helper functions
# -----------------------

def figure(**kwargs):
    """
    Create a new figure with dimensions in inches.

    Parameters
    ----------
    **kwargs :
        All keyword arguments are passed to :meth:`matplotlib.pyplot.figure`.

    Returns
    -------
    figure : :class:`AbsFigure`
        An :class:`AbsFigure` instance with methods to create new axes and
        subplots in absolute dimensions in inches or mm, or a figure of the
        custom `FigureClass` provided.
    """

    # by default select custom figure class
    figure_class = kwargs.pop('FigureClass', AbsFigure)

    # create a new figure
    fig = plt.figure(FigureClass=figure_class, **kwargs)
    return fig


def figure_mm(figsize=None, **kwargs):
    """
    Create a new figure with dimensions in millimeters.

    Parameters
    ----------
    figsize : (scalar, scalar)
        The figure width and height in millimeters.
    **kwargs :
        Additional keyword arguments are passed to :meth:`figure`.

    Returns
    -------
    figure : :class:`AbsFigure`
        An :class:`AbsFigure` instance with methods to create new axes and
        subplots in absolute dimensions in inches or mm, or a figure of the
        custom `FigureClass` provided.
    """

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
    """
    Create new figure and subplots with dimensions in inches.

    Parameters
    ----------
    nrows : int
        Number of rows in the subplot grid.
    ncols : int
        Number of columns in the subplot grid.
    **kwargs :
        Keyword arguments sharex, sharey, squeeze, subplot_kw and gridspec_kw
        are passed to :meth:`AbsFigure.subplots_inches`. Other keyword
        arguments are interpreted as figure keywords and passed to
        :meth:`figure`.

    Returns
    -------
    figure : :class:`AbsFigure`
        A figure whose size is controlled by the optional `figsize` argument
        with values in inches.
    axes : :class:`matplotlib.axes.Axes` or array of axes.
        A single or multiple subplots whose placement is controlled by the
        optional `gridspec_kw` argument with values in inches.
    """

    # segregate subplots and figure keywords
    spl_keys = ['sharex', 'sharey', 'squeeze', 'subplot_kw', 'gridspec_kw']
    spl_kw = {key: kwargs[key] for key in kwargs if key in spl_keys}
    fig_kw = {key: kwargs[key] for key in kwargs if key not in spl_keys}

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots_inches(nrows=nrows, ncols=ncols, **spl_kw)
    return fig, axs


def subplots_mm(nrows=1, ncols=1, **kwargs):
    """
    Create new figure and subplots with dimensions in millimeters.

    Parameters
    ----------
    nrows : int
        Number of rows in the subplot grid.
    ncols : int
        Number of columns in the subplot grid.
    **kwargs :
        Keyword arguments sharex, sharey, squeeze, subplot_kw and gridspec_kw
        are passed to :meth:`AbsFigure.subplots_inches`. Other keyword
        arguments are interpreted as figure keywords and passed to
        :meth:`figure`.

    Returns
    -------
    figure : :class:`AbsFigure`
        A figure whose size is controlled by the optional `figsize` argument
        with values in millimeters.
    axes : :class:`matplotlib.axes.Axes` or array of axes.
        A single or multiple subplots whose placement is controlled by the
        optional `gridspec_kw` argument with values in millimeters.
    """

    # segregate subplots and figure keywords
    spl_keys = ['sharex', 'sharey', 'squeeze', 'subplot_kw', 'gridspec_kw']
    spl_kw = {key: kwargs[key] for key in kwargs if key in spl_keys}
    fig_kw = {key: kwargs[key] for key in kwargs if key not in spl_keys}

    # create new figure and axes
    fig = figure_mm(**fig_kw)
    axs = fig.subplots_mm(nrows=nrows, ncols=ncols, **spl_kw)
    return fig, axs

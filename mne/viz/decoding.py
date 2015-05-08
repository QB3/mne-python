"""Functions to plot decoding results
"""
from __future__ import print_function

# Authors: Denis Engemann <denis.engemann@gmail.com>
#          Clement Moutard <clement.moutard@gmail.com>
#
# License: Simplified BSD

import numpy as np


def plot_gat_matrix(gat, title=None, vmin=None, vmax=None, tlim=None,
                    ax=None, cmap='RdBu_r', show=True, colorbar=True,
                    xlabel=True, ylabel=True):
    """Plotting function of GeneralizationAcrossTime object

    Predict each classifier. If multiple classifiers are passed, average
    prediction across all classifier to result in a single prediction per
    classifier.

    Parameters
    ----------
    gat : instance of mne.decoding.GeneralizationAcrossTime
        The gat object.
    title : str | None
        Figure title. Defaults to None.
    vmin : float | None
        Min color value for score. If None, sets to min(gat.scores_).
        Defaults to None.
    vmax : float | None
        Max color value for score. If None, sets to max(gat.scores_).
        Defaults to None.
    tlim : array-like, (4,) | None
        The temporal boundaries. If None, expands to
        [tmin_train, tmax_train, tmin_test, tmax_test]
        Defaults to None.
    ax : object | None
        Plot pointer. If None, generate new figure. Defaults to None.
    cmap : str | cmap object
        The color map to be used. Defaults to 'RdBu_r'.
    show : bool
        If True, the figure will be shown. Defaults to True.
    colorbar : bool
        If True, the colorbar of the figure is displayed. Defaults to True.
    xlabel : bool
        If True, the xlabel is displayed. Defaults to True.
    ylabel : bool
        If True, the ylabel is displayed. Defaults to True.

    Returns
    -------
    fig : instance of matplotlib.figure.Figure
        The figure.
    """
    if not hasattr(gat, 'scores_'):
        raise RuntimeError('Please score your data before trying to plot '
                           'scores')
    import matplotlib.pyplot as plt
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    # Define color limits
    if vmin is None:
        vmin = np.min(gat.scores_)
    if vmax is None:
        vmax = np.max(gat.scores_)

    # Define time limits
    if tlim is None:
        tt_times = gat.train_times['times_']
        tn_times = gat.test_times_['times_']
        tlim = [tn_times[0][0], tn_times[-1][-1], tt_times[0], tt_times[-1]]
    # Plot scores
    im = ax.imshow(gat.scores_, interpolation='nearest', origin='lower',
                   extent=tlim, vmin=vmin, vmax=vmax,
                   cmap=cmap)
    if xlabel is True:
        ax.set_xlabel('Testing Time (s)')
    if ylabel is True:
        ax.set_ylabel('Training Time (s)')
    if title is not None:
        ax.set_title(title)
    ax.axvline(0, color='k')
    ax.axhline(0, color='k')
    ax.set_xlim(tlim[:2])
    ax.set_ylim(tlim[2:])
    if colorbar is True:
        plt.colorbar(im, ax=ax)
    if show is True:
        plt.show()
    return fig if ax is None else ax.get_figure()


def plot_gat_diagonal(gat, title=None, xmin=None, xmax=None, ymin=None,
                      ymax=None, ax=None, show=True, color='b', xlabel=True,
                      ylabel=True, legend=True):
    """Plotting function of GeneralizationAcrossTime object

    Predict each classifier. If multiple classifiers are passed, average
    prediction across all classifier to result in a single prediction per
    classifier.

    Parameters
    ----------
    gat : instance of mne.decoding.GeneralizationAcrossTime
        The gat object.
    title : str | None
        Figure title. Defaults to None.
    xmin : float | None, optional, defaults to None.
        Min time value.
    xmax : float | None, optional, defaults to None.
        Max time value.
    ymin : float | None, optional, defaults to None.
        Min score value. If None, sets to min(scores).
    ymax : float | None, optional, defaults to None.
        Max score value. If None, sets to max(scores).
    ax : object | None
        Plot pointer. If None, generate new figure. Defaults to None.
    show : bool, optional, defaults to True.
        If True, the figure will be shown. Defaults to True.
    color : str
        Score line color. Defaults to 'steelblue'.
    xlabel : bool
        If True, the xlabel is displayed. Defaults to True.
    ylabel : bool
        If True, the ylabel is displayed. Defaults to True.
    legend : bool
        If True, a legend is displayed. Defaults to True.

    Returns
    -------
    fig : instance of matplotlib.figure.Figure
        The figure.
    """
    if not hasattr(gat, 'scores_'):
        raise RuntimeError('Please score your data before trying to plot '
                           'scores')
    import matplotlib.pyplot as plt
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    # detect whether gat is a full matrix or just its diagonal
    if np.all(np.unique([len(t) for t in gat.test_times_['times_']]) == 1):
        scores = gat.scores_
    else:
        # Get scores from identical training and testing times even if GAT
        # is not square.
        scores = np.zeros(len(gat.scores_))
        for i, T in enumerate(gat.train_times['times_']):
            for t in gat.test_times_['times_']:
                # find closest testing time from train_time
                j = np.abs(t - T).argmin()
                # check that not more than 1 classifier away
                if T - t[j] <= gat.train_times['step']:
                    scores[i] = gat.scores_[i][j]
    ax.plot(gat.train_times['times_'], scores, color=color,
            label="Classif. score")
    ax.axhline(0.5, color='k', linestyle='--', label="Chance level")
    if title is not None:
        ax.set_title(title)
    if ymin is None:
        ymin = np.min(scores)
    if ymax is None:
        ymax = np.max(scores)
    ax.set_ylim(ymin, ymax)
    if xmin is not None and xmax is not None:
        ax.set_xlim(xmin, xmax)
    if xlabel is True:
        ax.set_xlabel('Time (s)')
    if ylabel is True:
        ax.set_ylabel('Classif. score ({0})'.format(
                      'AUC' if 'roc' in repr(gat.scorer_) else r'%'))
    if legend is True:
        ax.legend(loc='best')
    if show is True:
        plt.show()
    return fig if ax is None else ax.get_figure()

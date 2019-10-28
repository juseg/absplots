#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""An example using the absolute margins gridspec functinality."""

import numpy as np
import absplots as apl


# init figure and gridspec
fig = apl.figure_mm(figsize=(120, 80))
gs = fig.add_gridspec_mm(ncols=3, left=10, right=5, wspace=5,
                         nrows=3, bottom=10, top=5, hspace=5)

# add subplots
fig.add_subplot(gs[0, :])
fig.add_subplot(gs[1, :-1])
fig.add_subplot(gs[1:, -1])
fig.add_subplot(gs[-1, 0])
fig.add_subplot(gs[-1, -2])

# plot some data
x = np.linspace(-1, 1, 101)
for i, ax in enumerate(fig.axes):
    ax.plot(x, x**(i+1))
    ax.text(0, 0.5, "ax%d" % (i+1), va="center", ha="center")
    ax.tick_params(labelbottom=False, labelleft=False)

# save
fig.savefig('gridspec.png', dpi=254)

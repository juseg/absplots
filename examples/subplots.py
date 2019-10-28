#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""A basic example with 5mm margins between and around subplots."""

import numpy as np
import absplots as apl

# init figure with high aspect ratio
fig, grid = apl.subplots_mm(figsize=(120, 40), nrows=1, ncols=3, sharey=True,
                            gridspec_kw=dict(left=10, right=5, wspace=5,
                                             bottom=10, top=5, hspace=5))

# plot some data
x = np.linspace(-1, 1, 101)
for i, ax in enumerate(grid.flat):
    ax.plot(x, x**(i+1))
    ax.text(0, 0.5, 'ax%d' % i, ha='center')

# save
fig.savefig('subplots.png', dpi=254)

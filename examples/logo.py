#!/usr/bin/env python
# Copyright (c) 2020, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Plot Absplots logo explaining what it's for."""

import absplots as apl

# init figure with high aspect ratio
fig, grid = apl.subplots_mm(figsize=(120, 40), ncols=2, gridspec_kw=dict(
    left=10, right=10, wspace=10, bottom=10, top=10, width_ratios=(3, 4)))

# add logo text
kwargs = dict(fontsize='52', fontweight='bold', ha='center', va='center')
grid[0].text(0, 0, 'Abs', color='C0', **kwargs)
grid[1].text(0, 0, 'plots', color='0.25', **kwargs)

# plot some data
for i, ax in enumerate(grid):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.tick_params(color='0.5', labelbottom=False, labelleft=False)
    for spine in ax.spines.values():
        spine.set_color('0.5')

# add double arrows in the margins
kwargs = dict(xycoords='axes fraction', textcoords='offset points',
              arrowprops=dict(arrowstyle='<->', color='0.5'))
cm2pts = 72/2.54
grid[0].annotate('', (0, 0.3), (-cm2pts, 0), **kwargs)
grid[0].annotate('', (1, 0.3), (+cm2pts, 0), **kwargs)
grid[1].annotate('', (1, 0.3), (+cm2pts, 0), **kwargs)
grid[0].annotate('', (0.45, 1), (0, +cm2pts), **kwargs)
grid[1].annotate('', (0.06, 0), (0, -cm2pts), **kwargs)

# add text labels in the margins
fig.text(0.24, 0.88, '10 mm', color='0.5', ha='left', va='center')
fig.text(0.53, 0.12, '10 mm', color='0.5', ha='left', va='center')
fig.text(0.042, 0.53, '10\nmm', color='0.5', ha='center', va='center')
fig.text(0.447, 0.53, '10\nmm', color='0.5', ha='center', va='center')
fig.text(0.958, 0.53, '10\nmm', color='0.5', ha='center', va='center')

# save
fig.savefig('logo.png', dpi=254)

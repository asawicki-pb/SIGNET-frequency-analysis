import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

df = pd.read_csv('fs_analysis.csv')

PARTICIPANTS = [1,2,3,4,7,10,12,14,16,18,19,20,21,23,24,25,26,
                27,28,29,30,31,33,34,35,36,37,38,40,43,46]

modalities = {
    'fs_accel': 'Accelerometer',
    'fs_gyro':  'Gyroscope',
    'fs_quat':  'Quaternion',
}

cmap_custom = LinearSegmentedColormap.from_list(
    'custom_fs', ['tomato', 'azure', 'forestgreen'], N=256
)

x_labels = [f'u{p:03d}' for p in PARTICIPANTS]

all_vals = df[list(modalities.keys())].values.flatten()
vmin    = np.nanmin(all_vals)
vmax    = np.nanmax(all_vals)
vcenter = np.nanmean(all_vals)
norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)

for ses_id, ses_label in [(1, 'Session I'), (2, 'Session II')]:

    # gridspec: 3 wiersze heatmap + wąska kolumna na colorbar
    fig = plt.figure(figsize=(20, 4))
    gs = gridspec.GridSpec(3, 2, width_ratios=[30, 1], hspace=0.6)

    axes = [fig.add_subplot(gs[i, 0]) for i in range(3)]
    cbar_ax = fig.add_subplot(gs[:, 1])   # colorbar zajmuje całą prawą kolumnę

    fig.suptitle(f'{ses_label} — Sampling Frequency Comparison [Hz]',
                 fontsize=13, fontweight='bold')

    df_ses = df[df['session'] == ses_id].set_index('user').reindex(PARTICIPANTS)

    for i, (ax, (col, mod_name)) in enumerate(zip(axes, modalities.items())):

        data    = df_ses[col].values.reshape(1, -1)
        df_heat = pd.DataFrame(data, index=[mod_name], columns=x_labels)

        sns.heatmap(
            df_heat,
            ax=ax,
            cmap=cmap_custom,
            norm=norm,
            annot=True,
            fmt='.1f',
            annot_kws={'size': 6},
            linewidths=0.3,
            linecolor='gray',
            cbar=i == 2,                          # colorbar tylko dla ostatniego
            cbar_ax=cbar_ax if i == 2 else None,
            cbar_kws={'label': 'Hz'},
        )

        ax.set_title(mod_name, fontsize=11)
        ax.set_ylabel('')
        ax.set_yticks([])

        # xticks tylko dla dolnego panelu
        if i < 2:
            ax.set_xticks([])
        else:
            ax.tick_params(axis='x', rotation=90, labelsize=7)

        # Zaznacz u012 i u037
        for uid, color in [(12, 'gold'), (37, 'gold')]:
            if uid in PARTICIPANTS:
                x_pos = PARTICIPANTS.index(uid)
                ax.add_patch(plt.Rectangle((x_pos, 0), 1, 1,
                             linewidth=2.5, edgecolor=color,
                             facecolor='none', clip_on=False))



    plt.savefig(f'fs_heatmap_session{ses_id}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'fs_heatmap_session{ses_id}.pdf', bbox_inches='tight')
    plt.show()
    print(f'Zapisano: fs_heatmap_session{ses_id}.png')
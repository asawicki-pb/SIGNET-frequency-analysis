import pandas as pd
import numpy as np
import os
from tqdm import tqdm

PARTICIPANTS = [1,2,3,4,7,10,12,14,16,18,19,20,21,23,24,25,26,
                27,28,29,30,31,33,34,35,36,37,38,40,43,46]

results = []

for USER_ID in tqdm(PARTICIPANTS, desc='Sampling frequency analysis'):
    user_str = '%03d' % USER_ID

    for SESSION, week_str in [(1, '001'), (2, '002')]:

        filename_accel = 'data/u%s_w%s/u%s_w%s_accelerometer.log' % (user_str, week_str, user_str, week_str)
        filename_gyro  = 'data/u%s_w%s/u%s_w%s_gyroscope.log'     % (user_str, week_str, user_str, week_str)
        filename_quat  = 'data/u%s_w%s/u%s_w%s_rotvec.log'        % (user_str, week_str, user_str, week_str)

        accel = pd.read_csv(filename_accel, sep='\t')
        gyro  = pd.read_csv(filename_gyro,  sep='\t')
        quat  = pd.read_csv(filename_quat,  sep='\t')

        t_a = accel['accelerometer_timestamp'].values / 1e9
        t_g = gyro['gyroscope_timestamp'].values       / 1e9
        t_q = quat['rotvec_timestamp'].values          / 1e9

        results.append({
            'user':     USER_ID,
            'session':  SESSION,
            'fs_accel': 1.0 / np.mean(np.diff(t_a)),
            'fs_gyro':  1.0 / np.mean(np.diff(t_g)),
            'fs_quat':  1.0 / np.mean(np.diff(t_q)),
        })

df = pd.DataFrame(results)
df.to_csv('fs_analysis.csv', index=False)

# --- Summary statistics ---
print('\n=== Mean sampling frequencies [Hz] ===')
for ses in [1, 2]:
    print(f'\n  Session {ses}:')
    sub = df[df['session'] == ses]
    for col in ['fs_accel', 'fs_gyro', 'fs_quat']:
        print(f'    {col:10s}  mean={sub[col].mean():.2f}  std={sub[col].std():.2f}  '
              f'min={sub[col].min():.2f}  max={sub[col].max():.2f}')

print('\nSaved: fs_analysis.csv')
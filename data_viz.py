import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

import API_Interface as api

pd.set_option('display.max_columns', 100)

with open('TestParams.csv', 'r') as file_in:
    param_file = csv.reader(file_in, delimiter=',')
    params = {}
    for param in param_file:
        params[param[0]] = param[1]

kellen_races = api.getDriversRaces(params['Kellen_Driver_ID'])
kellen_races.finish_position = kellen_races.finish_position.astype(int)
pd.to_datetime(kellen_races['starts_at'])
kellen_races.sort_values(by='starts_at', inplace=True)
print(kellen_races)

# Plotting
fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))
ax1.plot_date(kellen_races['starts_at'], kellen_races['finish_position'].expanding(min_periods=2).mean(), '-',
              label='Finish')
ax1.grid = True
ax1.xaxis.set_major_locator(mticker.MaxNLocator(9))
ax1.set_xticklabels(kellen_races['starts_at'], rotation=45, fontsize=8)
ax1.set_yticks([0, 2, 4, 6, 8, 10])
plt.legend()
plt.show()

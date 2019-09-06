
'''
Demonstration prototype for attack-tree series visualization
Imports data from csv file and draws the ATM fraud attack tree
'''


import numpy as np
import matplotlib
matplotlib.use('TKAgg')

import math

import matplotlib.pyplot as plt
from matplotlib import animation

from celluloid import Camera
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


# coords in plt
coords = {
    'v0': [36, 44,  6, 4],
    'v1': [15, 36, 15, 4],
    'v2': [44, 36, 12, 4],
    'v3': [1, 28, 10, 4],
    'v4': [15, 28, 15, 4],
    'v5': [38, 28, 10, 4],
    'v6': [52, 28, 7, 4],
    'v7': [62, 28, 10, 4],
    'v8': [20, 20, 6, 4],
    'v9': [46, 20, 5, 4],
    'v10': [10, 12, 7, 4],
    'v11': [18, 12, 9, 4],
    'v12': [28, 12, 5, 4],
    'v13': [38, 12, 7, 4],
    'v14': [48, 12, 10, 4],
    'v15': [60, 12, 15, 4],
    'v16': [30, 4, 8, 4],
    'v17': [40, 4, 6, 4],
    'v18': [47, 4, 5, 4],
    'v19': [54, 4, 7, 4],
}

names = {
    'v0': "ATM Fraud",
    'v1': "Access ATM to prepare attack",
    'v2': "Execute attacks on ATM",
    'v3': "Breaking into facility",
    'v4': "Social engineering facility staff",
    'v5': "Get user credentials",
    'v6': "Cash trapping",
    'v7': "Transaction reversal",
    'v8':  "Get PIN",
    'v9':  "Get card",
    'v10':   "Shouldersurf",
    'v11':  "Installing camera",
    'v12':  "Install EPP",
    'v13':  "Card skimming",
    'v14':  "Take card physically",
    'v15':  "Social engineering card owner",
    'v16':  "Install skimmer",
    'v17':  "Clone card",
    'v18':  "Steal card",
    'v19':  "Card trapping"
}

lines_among = [
    ['v0', 'v1'],
    ['v0', 'v2'],
    ['v1', 'v3'],
    ['v1', 'v4'],
    ['v2', 'v5'],
    ['v2', 'v6'],
    ['v2', 'v7'],
    ['v5', 'v8'],
    ['v5', 'v9'],
    ['v8', 'v10'],
    ['v8', 'v11'],
    ['v8', 'v12'],
    ['v9', 'v13'],
    ['v9', 'v14'],
    ['v9', 'v15'],
    ['v13', 'v16'],
    ['v13', 'v17'],
    ['v14', 'v18'],
    ['v14', 'v19'],
]

line0 = [34.8, 41.82, 43, 43]
line5 = [38, 44.3, 27, 27]
line13 = [39.6, 41.8, 11, 11]


# Read in data from a CSV file
data = pd.read_csv('data/ATM_random_risk.csv', header=0, index_col = 0)
data = np.around(data, decimals=2)
# years = ['2010', '2011', '2012', '2013', '2014', '2015']
years = ['2014', '2015', '2016', '2017', '2018', '2019']
attribute = 'Risk'
gif_name = 'atm_random_risk'

# temperature functions

def magnitude(value):
    if (value == 0): return 0
    return int(math.floor(math.log10(abs(value))))


def thermo1(new_value, old_value):

    # return node color for the new value depending on the previous value only

    safe_delta = 10 ** (magnitude(old_value)) # consider that change within order of magnitude of old value is ok
    if old_value == 0:
        # old value is 0
        if new_value > 0:
            return danger_color # any change is big

    if (old_value - new_value) < 0: # value increased
        if (new_value - old_value) > 3* safe_delta:  # increased a lot
            return danger_color
        else:
            if (new_value - old_value) > safe_delta:  # somewhat increased
                return warmer_color
            else:
                return no_color
    else:
        if (old_value - new_value) >= safe_delta:  # somewhat decreased
            return colder_color
        else:
            return no_color



# fc8d59 red
# ffffbf orange
# 91cf60 green

# color constants
colder_color = '#91CF60'
warmer_color = '#FFFFBF'
danger_color = '#FC8D59'
same_color = 'black'
no_color = 'white'
dont_color = '#DCDCDC'



def get_color(name, year, data):
    if name not in data.index:
        return dont_color
    if year == years[0]:
        return no_color
    else:
        prev_year = str(int(year) - 1)
        cur_value = data.loc[name][year]
        prev_value = data.loc[name][prev_year]
        return thermo1(cur_value, prev_value)


def draw_node(name, year, data):
    node_color = get_color(name, year, data)
    rectangle = plt.Rectangle((coords[name][0], coords[name][1]), coords[name][2], coords[name][3],
                              fc=node_color, alpha=0.36, edgecolor='black')
    return rectangle



fig = plt.figure()
fig.set_size_inches(26, 19)
ax = plt.axes(xlim=(0, 76), ylim=(0, 50))
plt.axis('off')
plt.tight_layout()

camera = Camera(fig)

for key, value in coords.items():
    rectangle = draw_node(key, years[0], data)
    plt.gca().add_patch(rectangle)

    plt.text(value[0] + value[2] / 2.0, value[1] + 2.6, names[key],
             fontsize=18, horizontalalignment='center')

    if key in data.index:
        plt.text(value[0] + value[2] / 2.0, value[1] + 1, data.loc[key][years[0]],
                 fontsize=16, horizontalalignment='center', fontweight='bold')

    for pair in lines_among:
        v_up = pair[0]
        x_up = coords[v_up][0] + coords[v_up][2] / 2.0
        y_up = coords[v_up][1]

        v_down = pair[1]
        x_down = coords[v_down][0] + coords[v_down][2] / 2.0
        y_down = coords[v_down][1] + coords[v_down][3]
        line = plt.Line2D((x_up, x_down), (y_up, y_down), lw=1, color='black')
        plt.gca().add_line(line)

    line = plt.Line2D((line0[0], line0[1]), (line0[2], line0[3]), lw=1, color='black')
    plt.gca().add_line(line)

    line = plt.Line2D((line5[0], line5[1]), (line5[2], line5[3]), lw=1, color='black')
    plt.gca().add_line(line)

    line = plt.Line2D((line13[0], line13[1]), (line13[2], line13[3]), lw=1, color='black')
    plt.gca().add_line(line)

    ax.text(54, 47, 'Attribute: ' + attribute, fontsize=24)
    ax.text(54, 45, 'Year: ' + years[0], fontsize=24)

camera.snap()

# next years

for i in range(0, 5, 1):
    cur_year = str(int(years[0]) + i + 1)

    for key, value in coords.items():
        rectangle = draw_node(key, cur_year, data)
        plt.gca().add_patch(rectangle)

        plt.text(value[0] + value[2] / 2.0, value[1] + 2.6, names[key],
                 fontsize=18, horizontalalignment='center')

        if key in data.index:
            plt.text(value[0] + value[2] / 2.0, value[1] + 1, data.loc[key][cur_year],
                     fontsize=16, horizontalalignment='center', fontweight='bold')

        for pair in lines_among:
            v_up = pair[0]
            x_up = coords[v_up][0] + coords[v_up][2] / 2.0
            y_up = coords[v_up][1]

            v_down = pair[1]
            x_down = coords[v_down][0] + coords[v_down][2] / 2.0
            y_down = coords[v_down][1] + coords[v_down][3]
            line = plt.Line2D((x_up, x_down), (y_up, y_down), lw=1, color='black')
            plt.gca().add_line(line)

    line = plt.Line2D((line0[0], line0[1]), (line0[2], line0[3]), lw=1, color='black')
    plt.gca().add_line(line)

    line = plt.Line2D((line5[0], line5[1]), (line5[2], line5[3]), lw=1, color='black')
    plt.gca().add_line(line)

    line = plt.Line2D((line13[0], line13[1]), (line13[2], line13[3]), lw=1, color='black')
    plt.gca().add_line(line)

    ax.text(54, 47, 'Attribute: ' + attribute, fontsize=24)
    ax.text(54, 45, 'Year: ' + cur_year, fontsize=24)

    camera.snap()

animation = camera.animate(interval=3000)
animation.save(gif_name + '.gif', writer='imagemagick')




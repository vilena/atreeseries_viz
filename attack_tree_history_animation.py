

import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import celluloid
from celluloid import Camera
import pandas as pd
from matplotlib import pyplot as plt



# Coordinates of attack tree nodes in plt canvas
coords = {
    'v0': [27, 44,  5, 5],
    'v1': [7, 36, 15, 5],
    'v2': [34, 36, 12, 5],
    'v3': [1, 28, 10, 5],
    'v4': [12, 28, 15, 5],
    'v5': [30, 28, 10, 5],
    'v6': [41, 28, 7, 5],
    'v7': [49, 28, 10, 5],
    'v8': [14, 20, 6, 5],
    'v9': [38, 20, 5, 5],
    'v10': [1, 12, 7, 5],
    'v11': [8.5, 12, 8.5, 5],
    'v12': [18, 12, 5, 5],
    'v13': [26, 12, 7, 5],
    'v14': [33.5, 12, 10, 5],
    'v15': [44, 12, 15, 5],
    'v16': [18, 4, 8, 5],
    'v17': [27, 4, 6, 5],
    'v18': [35, 4, 5, 5],
    'v19': [41, 4, 7, 5],
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

line0 = [24.8, 33, 43, 43]
line5 = [29.6, 36.7, 27, 27]
line13 = [27, 29.6, 11, 11]

# Preparing data; random values generated for leaf nodes

nyears=6

values_dict = {
    'v3': np.random.random_sample(nyears),
    'v4': np.random.random_sample(nyears),
    'v6': np.random.random_sample(nyears),
    'v7': np.random.random_sample(nyears),
    'v10': np.random.random_sample(nyears),
    'v11': np.random.random_sample(nyears),
    'v12': np.random.random_sample(nyears),
    'v15': np.random.random_sample(nyears),
    'v16': np.random.random_sample(nyears),
    'v17': np.random.random_sample(nyears),
    'v18': np.random.random_sample(nyears),
    'v19': np.random.random_sample(nyears),
}

data = pd.DataFrame(values_dict).transpose()
data.columns = ['2014', '2015', '2016', '2017', '2018', '2019']

# derived values computed for intermediary nodes
data.loc['v14'] = data.loc['v18']+data.loc['v19'] - data.loc['v18']*data.loc['v19']
data.loc['v13'] = data.loc['v16']*data.loc['v17']
data.loc['v8'] = data.loc['v10'] + data.loc['v11'] + data.loc['v12'] - data.loc['v10']*data.loc['v11'] - data.loc['v10']*data.loc['v12'] - data.loc['v12']*data.loc['v11'] + data.loc['v10']*data.loc['v11']*data.loc['v12']
data.loc['v9'] = data.loc['v13'] + data.loc['v14'] + data.loc['v15'] - data.loc['v13']*data.loc['v14'] - data.loc['v13']*data.loc['v15'] - data.loc['v14']*data.loc['v15'] + data.loc['v13']*data.loc['v14']*data.loc['v15']
data.loc['v5'] = data.loc['v8'] * data.loc['v9']
data.loc['v2'] = data.loc['v5'] + data.loc['v6'] + data.loc['v7'] - data.loc['v5']*data.loc['v6'] - data.loc['v5']*data.loc['v7'] - data.loc['v6']*data.loc['v7'] + data.loc['v5']*data.loc['v6']*data.loc['v7']
data.loc['v1'] = data.loc['v3']+data.loc['v4'] - data.loc['v3']*data.loc['v4']
data.loc['v0'] = data.loc['v1']*data.loc['v2']

data = np.around(data, decimals=2)


# Define a simple temperature function

# color constants
colder_color = 'green'
warmer_color = 'yellow'
danger_color = 'red'
same_color = 'black'
no_color = 'white'


import math

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
        if (new_value - old_value) > 3*safe_delta: # increased a lot
            return danger_color
        else:
            if (new_value - old_value) > safe_delta: # somewhat increased
                return warmer_color
            else:
                return no_color
    else:
        if (old_value - new_value) >= safe_delta: # somewhat decreased
            return colder_color
        else:
            return no_color
        


def get_color(name, year, data):
    if year == '2014':
        return no_color
    else:
        prev_year = str(int(year) - 1)
        cur_value = data.loc[name][year]
        prev_value = data.loc[name][prev_year]
        return thermo1(cur_value, prev_value)

def draw_node(name, year, data):
    
    node_color = get_color(name, year, data)
    #print node_color
    rectangle = plt.Rectangle((coords[name][0], coords[name][1]), coords[name][2], coords[name][3], 
                              fc=node_color, alpha=0.36, edgecolor='black')
    return rectangle


# drawing and animating


fig = plt.figure()
fig.set_size_inches(22, 19)
ax = plt.axes(xlim = (0,60), ylim = (0,50))
plt.axis('off')
plt.tight_layout()

camera = Camera(fig)

for key, value in coords.items():
    rectangle = draw_node(key, '2014', data)
    plt.gca().add_patch(rectangle)
    
    plt.text(value[0]+value[2]/2.0, value[1]+3, names[key], 
         fontsize=18, horizontalalignment='center')
    
    plt.text(value[0]+value[2]/2.0, value[1]+1, data.loc[key]['2014'], 
         fontsize=16, horizontalalignment='center', fontweight='bold')

    for pair in lines_among:
        v_up = pair[0]
        x_up = coords[v_up][0] + coords[v_up][2]/2.0
        y_up = coords[v_up][1]
    
        v_down = pair[1]
        x_down = coords[v_down][0] + coords[v_down][2]/2.0
        y_down = coords[v_down][1] + coords[v_down][3]
        line = plt.Line2D((x_up, x_down), (y_up, y_down), lw=1, color = 'black')
        plt.gca().add_line(line)


    line = plt.Line2D((line0[0], line0[1]), (line0[2], line0[3]), lw=1, color = 'black')
    plt.gca().add_line(line)

    line = plt.Line2D((line5[0], line5[1]), (line5[2], line5[3]), lw=1, color = 'black')
    plt.gca().add_line(line)

    line = plt.Line2D((line13[0], line13[1]), (line13[2], line13[3]), lw=1, color = 'black')
    plt.gca().add_line(line)

    ax.text(40, 48, 'Attribute: Probability', fontsize = 20)
    ax.text(40, 46, 'Year: '+ '2014', fontsize = 20)

camera.snap()

# next years

for i in range(0, 5, 1):
    cur_year = str(int('2015') + i)

    for key, value in coords.items():
        rectangle = draw_node(key, cur_year, data)
        plt.gca().add_patch(rectangle)

        plt.text(value[0] + value[2] / 2.0, value[1] + 3, names[key],
                 fontsize=18, horizontalalignment='center')

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

    ax.text(40, 48, 'Attribute: Probability', fontsize=20)
    ax.text(40, 46, 'Year: ' + cur_year, fontsize=20)

    camera.snap()

animation = camera.animate(interval=3000)
animation.save('atm_tree_animation.gif', writer = 'imagemagick')




'''Generating synthetic probability and cost data for the ATM fraud attack tree'''

import numpy as np
import pandas as pd


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

prob = pd.DataFrame(values_dict).transpose()
prob.columns = ['2014', '2015', '2016', '2017', '2018', '2019']

prob.loc['v14'] = prob.loc['v18'] + prob.loc['v19'] - prob.loc['v18'] * prob.loc['v19']
prob.loc['v13'] = prob.loc['v16'] * prob.loc['v17']
prob.loc['v8'] = prob.loc['v10'] + prob.loc['v11'] + prob.loc['v12'] - prob.loc['v10'] * prob.loc['v11'] - prob.loc['v10'] * prob.loc['v12'] - prob.loc['v12'] * prob.loc['v11'] + prob.loc['v10'] * prob.loc['v11'] * prob.loc['v12']
prob.loc['v9'] = prob.loc['v13'] + prob.loc['v14'] + prob.loc['v15'] - prob.loc['v13'] * prob.loc['v14'] - prob.loc['v13'] * prob.loc['v15'] - prob.loc['v14'] * prob.loc['v15'] + prob.loc['v13'] * prob.loc['v14'] * prob.loc['v15']
prob.loc['v5'] = prob.loc['v8'] * prob.loc['v9']
prob.loc['v2'] = prob.loc['v5'] + prob.loc['v6'] + prob.loc['v7'] - prob.loc['v5'] * prob.loc['v6'] - prob.loc['v5'] * prob.loc['v7'] - prob.loc['v6'] * prob.loc['v7'] + prob.loc['v5'] * prob.loc['v6'] * prob.loc['v7']
prob.loc['v1'] = prob.loc['v3'] + prob.loc['v4'] - prob.loc['v3'] * prob.loc['v4']
prob.loc['v0'] = prob.loc['v1'] * prob.loc['v2']

prob = np.around(prob, decimals=2)

# Computing cost to defender per year
cost_dict = {
    'v3': np.random.randint(size=nyears, low=0, high=5000),
    'v4': np.random.randint(size=nyears, low=0, high=1000),
    'v6': np.random.randint(size=nyears, low=0, high=10000),
    'v7': np.random.randint(size=nyears, low=0, high=5000),
    'v10': np.random.randint(size=nyears, low=0, high=100),
    'v11': np.random.randint(size=nyears, low=0, high=10000),
    'v12': np.random.randint(size=nyears, low=0, high=10000),
    'v15': np.random.randint(size=nyears, low=0, high=1000),
    'v16': np.random.randint(size=nyears, low=0, high=10000),
    'v17': np.random.randint(size=nyears, low=0, high=1000),
    'v18': np.random.randint(size=nyears, low=0, high=500),
    'v19': np.random.randint(size=nyears, low=0, high=10000),
}

cost_df = pd.DataFrame(cost_dict).transpose()
cost_df.columns = ['2014', '2015', '2016', '2017', '2018', '2019']

cost_df.loc['v1'] = np.maximum(cost_df.loc['v3'], cost_df.loc['v4'])
cost_df.loc['v8'] = np.maximum(np.maximum(cost_df.loc['v10'], cost_df.loc['v11']), cost_df.loc['v12'])
cost_df.loc['v13'] = cost_df.loc['v16'] + cost_df.loc['v17']
cost_df.loc['v14'] = np.maximum(cost_df.loc['v18'], cost_df.loc['v19'])
cost_df.loc['v9'] = np.maximum(np.maximum(cost_df.loc['v13'], cost_df.loc['v14']), cost_df.loc['v15'])
cost_df.loc['v5'] = cost_df.loc['v8'] + cost_df.loc['v9']
cost_df.loc['v2'] = np.maximum(np.maximum(cost_df.loc['v5'], cost_df.loc['v6']), cost_df.loc['v7'])
cost_df.loc['v0'] = cost_df.loc['v1'] + cost_df.loc['v2']

risk = prob * cost_df
risk = np.around(risk, decimals=2)

prob.to_csv('ATM_random_prob.csv', index=True)
cost_df.to_csv('ATM_random_cost.csv', index=True)
risk.to_csv('ATM_random_risk.csv', index=True)
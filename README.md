# atreeseries_viz
A visualisation demo for attack-tree series historical view with the ATM fraud attack tree.

# Gif animation:
Observation starts in 2014. For all subsequent years, we mark a node as _red_ if its attribute value has significantly increased, _yellow_ if slightly increased, and _green_ if decreased. If the change over the previous year is less than the order of magnitude of the attribute value, we don't color this node for the current year. 

## Risk over the years (probability * cost to defender):

![](./demo/atm_risk.gif)

## Probability only:

![](./demo/atm_tree_animation.gif)

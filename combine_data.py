#!/usr/bin/env python
# coding: utf-8

# # Combine data into one plot
# 
# - Combining two or more *related* datasets into one plot can save precious space.
# - Often it is also a better way to present information.
# 
# This will show how to tweak pyplot features you already know to achieve this. 
# - Using subplots to create a single plot with different two y-axes.
# - How to fine tune axes when working with multiple subplots.
# - Combining two or more datasets in bar plots.
# 
# Examples are kept simple. Often you will be able to figure out how to expand them yourself. You also might want to look at [matplotlib examples](https://matplotlib.org/stable/gallery/) for a systematic collection of examples.

# ## Subplots
# ### Using subplots to produce plots using two y-axis
# 
# When combining two data sets, curves, ..... into one plot one often faces the difficulty that their ranges are very different. One of the curves will be barely visible if plotted into one plot. Ways to handle this
# - Rescale one and explain using label="size$\times$1000"
# - Normalise both
# - Use different scales and two different y-axes using `subplots()`
# 
# The `plt.figure()` function returns a handle to a figure object - similar to the file handle after opening a file.

# In[19]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

fig = plt.figure()
print(fig, type(fig))
plt.close()


# This tells us that `fig` is a figure object with 432x288 pixels. This figure handle is rarely used. Usually one does not need to refer to this and can use the standard figure manipulation with `plt` functions. 

# Lets create a simple 1x1 subplot

# In[20]:


# default is a single 1x1 subplot
fig, ax = plt.subplots()
# this is the same as calling plt.subplots(1, 1)
print(fig, type(fig))
print(ax, type(ax))
plt.show()


# - `fig` contains the handle to a figure object - nothing new
# - `ax` contains the handle to an axes object. That gives a lot more options to fine tune a plot.
# 
# Example how to use a single subplot to create a plot with two different y-axes.

# In[21]:


import numpy as np

# Create some mock data
x = np.linspace(-10.0, 10.0, 1000)
sinh = np.sinh(x)
sin = np.sin(x)

# this call returns one axes handle for one plot. It is called ax1 for reasons 
# becoming clear below. Default is a single subplot (1x1).
fig, ax1 = plt.subplots()

color = "red"   # colour used for line and labelling
# many of the pyplot functions are available as methods of the axes object ax1
# the synthax is sometimes a bit different
ax1.set_xlabel('x')
ax1.set_ylabel('sinh(x)', color=color)     # a different colour is used
# Note that we use the plot method of the axes object. Can be done differently using
# subplot() (see lecture)
ax1.plot(x, sinh, color=color)

# axis="y" specifices that changes are only made to the y-axis
ax1.tick_params(axis='y', labelcolor=color)

# instantiate a second axis that shares the same x-axis
ax2 = ax1.twinx()  

color = "blue"   # set color for line and labelling
ax2.set_ylabel('sin(x)', color=color)  
# x-labels already set with ax1
ax2.plot(x, sin, color="blue")
ax2.tick_params(axis='y', labelcolor=color)
# y-limits set by hand for sin. Limits for the x-axis and the sinh axis 
# are left to be set automatically
ax2.set_ylim(-1.0, 1.0)

# further modifications could be done to the left hand axes uses the ax1 object
# changes could be made to the x-axis by using ax1 or ax2 methods.

# a simple way to deal with a slight clipping problem on the right hand
# side. Note that the figure handle from above is used.
fig.tight_layout()  

plt.show()


# Documentation of the many methods to fine tune axes: 
# [Axes methods for labels, limits, tickmarks](https://matplotlib.org/stable/api/axes_api.html#axis-limits)
# 
# The colour notation is different from the simple notation we are usually using. Ways to specify colours in pyplot [Pyplot colour definitions](https://matplotlib.org/stable/tutorials/colors/colors.html).
# 
# Notes:
# - RGB(A) stands for additive colour combination using red, green, blue (and alpha). alpha is the transparancy we encountered before.
# - tableau colours can usually be specified without `tab:`
# 
# ### Fine tuning multiple subplots
# 
# Let's have a look at the axes object produced by a call of `subplots()` for multiple
# plots.
# 

# In[22]:


fig, axes = plt.subplots(2, 3)
print(axes)
axes[1,1].set_xlim(-10,10)
plt.show()


# Returned a list of lists of 2x3 handles for axes objects. Features of the axes objects can be changed as shown above. It is often convenient to extract the handles.
# 

# In[23]:


fig, axes = plt.subplots(2, 3)
print(axes)
ax_bl = axes[1,0]   # handle for bottom left subplot
ax_bl.set_xlim(-10.0, 10.0)
ax_bl.set_ylim(-1.05, 1.05)
ax_bl.plot(x, sin)
plt.show()


# In[24]:


import numpy as np


def one_sub(ax, x, y, label):
    """ Plots one subplot with label using the axes object ax. x and y are the data.  """
    
    ax.plot(x, y, label=label)
    ax.legend()
    return
    
    
# Create more mock data
t = np.linspace(-10.0, 10.0, 1000)
sin = np.sin(t)
sinh = np.sinh(t)
cos = np.cos(t)
cosh = np.cosh(t)
tan = np.tan(t)
tanh = np.tanh(t)

# create list of function values for more convenient plotting
funcs = [[sinh, cosh, tanh], [sin, cos, tan]]
# and the labels 
labels = [["sinh", "cosh", "tanh"], ["sin", "cos", "tan"]]

# Call of subplots for 2x3 grid 
# All subplots share the same x-axis, subplots in the top and bottom rows share the same
# y-axis. This removes tick labels cluttering the space between plots and synchronises 
# limits and ticks
# This can be handled on an axes by axes basis for more complicated plots.
fig, axes = plt.subplots(2, 3, sharex="all", sharey="row")

# since the x-axes limits are shared, setting one affects all
axes[1,1].set_xlim(-10.0, 10.0)
# y-axes need to set for each row once
axes[0,1].set_ylim(-1.0e4, 1.0e4)
axes[1,1].set_ylim(-2.0, 2.0)
# if not set, automatic limits will be set for all subplots with shared axes

# fine tuning of the y-ticks, affects all shared axes
# setting major ticks (default)
axes[0,0].set_xticks(np.arange(-10, 11, 5))
# setting minor ticks
axes[0,0].set_xticks(np.arange(-10, 11, 1), minor=True)

# plots the hyperbolic functions in the top row
iy = 0   # top part of the plot
for ix in range(3):
    one_sub(axes[iy, ix], x, funcs[iy][ix], labels[iy][ix])

# now the trigonometric functions into the bottom row
iy = 1   # top part of the plot
for ix in range(3):
    one_sub(axes[iy, ix], x, funcs[iy][ix], labels[iy][ix])

# producing a title for the whole plot
fig.suptitle("hyberbolic and trigonometric functions")
axes[1,0].set_xlabel("x")
axes[1,1].set_xlabel("x")
axes[1,2].set_xlabel("x")
axes[1,0].set_ylabel("f(x)")
axes[0,0].set_ylabel("f(x)")
# fig.supxlabel() and fig.supylabel() are recent additions to matplotlib
# you'll need a very new version of anaconda to have that available
# still some teething problems, probably best stick with the solutions above


# Matplot lib page with more examples
# 
# [Examples creating multiple subplots](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html)

# ## Bar plots
# ### Producing bar plots with columns side-by-side
# 
# Bar plot showing the historical populations of inner and outer London. A numerical x-axis is used and the bars are offset by the same amount to the left and the right. (Remember that labels were used in the lecture, another option).
# 
# 
# Create the data.

# In[25]:


import matplotlib.pyplot as plt
import numpy as np

# population data for inner, outer and greater (=inner+outer) London
# data made numpy arrays for more convenient calculations
years = np.array([1801, 1851, 1901, 1951, 2001]) 
inner_pop = np.array([879491, 1995846, 4670177, 3680821, 2765975])
outer_pop = np.array([131666, 290763, 1556317, 4483595, 4406061])
greater_pop = np.array([1011157, 2286609, 6226494, 8164416, 7172036])

# convert to millions for nicer layout
inner_pop = inner_pop / 1.0e6
outer_pop = outer_pop / 1.0e6


# In[26]:


plt.figure()
iyears = years - 5.0   # offset to the left
# the 2nd argument is the height of the bars
# width in units of the x-axis
plt.bar(iyears, inner_pop, width=7.0, label="inner")
oyears = years + 5.0   # and to the right
plt.bar(oyears, outer_pop, width=7.0, label="outer")

# general matters
plt.title("Population of London")
plt.xlabel("year")
plt.ylabel("population (millions)")
plt.legend()    
plt.show()


# ### Stacking bars on top of each other
# 
# The optional argument `bottom` is used to stack bars on top of each other. Note that you have to add up all previous values if you want to add a third, fourth, .....

# In[27]:


# bars can be also stacked on top of each other
plt.figure()
plt.bar(years, inner_pop, width=10.0, label="inner")
# if optional argument bottom is used, the bars of height are plotted 
# from the value of bottom
plt.bar(years, outer_pop, bottom=inner_pop, width=10.0, label="outer")

# general matters
plt.title("Population of London")
plt.xlabel("year")
plt.ylabel("population (millions)")
plt.legend()    
plt.show()


# In[ ]:





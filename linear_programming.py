import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

from matplotlib.widgets import Button, Slider


# The parametrized function to be plotted
def wl(t, wood):
    return (wood - 20*t) / 30

def ll(t, labor):
    return (labor - 5*t) / 4

def pl(t, profit):
    return (profit - 25*t) / 30

t = np.linspace(0, 150, 5)

# Define initial parameters
init_wood = 690
init_labor = 120
init_profit = 750

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
wline, = ax.plot(t, wl(t, init_wood), lw=2, color='r', label='Wood')
lline, = ax.plot(t, ll(t, init_labor), lw=2, color='g', label='Labor')
pline, = ax.plot(t, pl(t, init_profit), lw=2, color='k', label='Profit')
ax.axline((4, 0), (4, 10), color='b', label='Table')
ax.axline((0, 2), (10, 2), color='c', label='Bookshelf')

ax.set(title='Schedule', xlabel='Table', ylabel='Bookshelf')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axwood = fig.add_axes([0.25, 0.1, 0.65, 0.03])
wood_slider = Slider(
    ax=axwood,
    label='Wood',
    valmin=0,
    valmax=2000,
    valinit=init_wood,
)

axprofit = fig.add_axes([0.25, 0.15, 0.65, 0.03])
profit_slider = Slider(
    ax=axprofit,
    label='Profit',
    valmin=0,
    valmax=2000,
    valinit=init_profit,
)

# Make a vertically oriented slider to control the amplitude
axlabor = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
labor_slider = Slider(
    ax=axlabor,
    label="Labor",
    valmin=0,
    valmax=500,
    valinit=init_labor,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    wline.set_ydata(wl(t, wood_slider.val))
    pline.set_ydata(pl(t, profit_slider.val))
    lline.set_ydata(ll(t, labor_slider.val))
    fig.canvas.draw_idle()

def cal_profit():
    c = [-25, -30]
    A = [[20, 30], [5,4]]
    b = [wood_slider.val, labor_slider.val]
    x1_bounds = (4, None)
    x2_bounds = (2, None)

    res = linprog(c, A_ub=A, b_ub=b, bounds=[x1_bounds, x2_bounds])
    return -res.fun

def cal_and_update(val):
    profit = cal_profit()
    profit_slider.set_val(profit)
    update(val)

# register the update function with each slider
# wood_slider.on_changed(update)
# labor_slider.on_changed(update)
wood_slider.on_changed(cal_and_update)
labor_slider.on_changed(cal_and_update)
profit_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    wood_slider.reset()
    labor_slider.reset()
    profit_slider.reset()
button.on_clicked(reset)

ax.legend()
ax.set_xlim([0, 50])
ax.set_ylim([0, 50])

plt.show()


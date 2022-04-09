from matplotlib import pyplot as plt
import matplotlib.image as mpiage
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import scipy.interpolate as interpolate
from numpy.lib.function_base import append
import numpy as np
from scipy.special import binom

currently_point = None
point_alpha_default = 0.8
mousepress = None
currently_dragging = False
current_artist = None
offset = [0,0]
n = 0

spline_object = None
line_object = None
points = [] # circles objects array

def Bernstein(n, k):
    """Bernstein polynomial.

    """
    coeff = binom(n, k)
    #print(n,k)
    def _bpoly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bpoly

def Bezier(points, num=200):
    """Build Bézier curve from points.

    """
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for ii in range(N):
        curve += np.outer(Bernstein(N - 1, ii)(t), points[ii])
    return curve

def spline():
    global line_object, spline_object

    xdata = list(line_object.get_xdata())
    ydata = list(line_object.get_ydata())

    x_new, y_new = Bezier(list(zip(xdata, ydata))).T

    spline_object.set_data(x_new, y_new)

# button_press_event
def on_click(event):
    global n, line_object, spline_object
    if len(points)<2:
        x,y = event.xdata, event.ydata

        point = patches.Circle((x,y), radius= 50, color = 'r', fill = False, lw=2, picker=True)
        point.set_picker(5)
        points.append(point)
        ax.add_patch(point)

        if len(points)==2:
            x0, y0 = points[0].center
            line_object = ax.plot([x0, x], [y0, y], 'g--', lw=0.5, picker=True)[0]
            line_object.set_pickradius(5)

            spline_object = ax.plot([x0, x], [y0, y], c='b', lw=1)[0]
        plt.draw()


# pick_event
def on_pick(event):
    global line_object, currently_point, n, current_artist

    if current_artist == None:
        if isinstance(event.artist, Line2D):
            current_artist = Line2D
            x,y = event.mouseevent.xdata , event.mouseevent.ydata
            # if  min(points['x']) < x < max(points['x']) and min(points['y']) < y < max(points['y']):
            point = patches.Circle((x,y), radius= 50, color ='g', fill = False, lw=2, picker=True)
            point.set_picker(5)

            xdata = list(line_object.get_xdata())
            ydata = list(line_object.get_ydata())

            for i in range(0,len(xdata)-1):
                if x > min(xdata[i],xdata[i+1]) and x < max(xdata[i],xdata[i+1]) and \
                    y > min(ydata[i],ydata[i+1]) and y < max(ydata[i],ydata[i+1]) :
                        ax.add_patch(point)
                        points.insert(i+1, point)
                        xdata.insert(i+1, x)
                        ydata.insert(i+1, y)

            line_object.set_data(xdata, ydata)
            plt.draw()

        elif isinstance(event.artist, patches.Circle):
            current_artist = patches.Circle
            circle = event.artist
            n = points.index(circle)
            currently_point = circle


def on_press(event):
    global currently_dragging
    global mousepress
    # currently_dragging = True

def on_motion(event):
    global currently_dragging, currently_point, line_object, n, current_artist

    if currently_point != None and current_artist == patches.Circle:
        spline()
        x, y = event.xdata, event.ydata
        currently_point.set_center((x,y))

        xdata = list(line_object.get_xdata())
        ydata = list(line_object.get_ydata())
        xdata[n] = x
        ydata[n] = y
        line_object.set_data(xdata, ydata)

        plt.draw()

def on_release(event):
    global currently_dragging, currently_point, current_artist
    # if len(points) > 2:
    #     spline()
    current_artist = None
    currently_point = None
    currently_dragging = False


data = mpiage.imread('orange.jpg')

fig, ax = plt.subplots()
ax.set_xlim(0, 4000)
ax.set_ylim(0, 3000)

plt.imshow(data)

def func(event):
    print(event)
# ax.plot([1,200,2000], [1, 200, 2000], picker=True)
# events = ['button_press_event'
#             ,'button_release_event'
#             , 'draw_event'
#             , 'key_press_event'
#             , 'key_release_event'
#             , 'pick_event'
#             , 'motion_notify_event'
#             , 'resize_event'
#             , 'scroll_event'
#             , 'figure_enter_event'
#             , 'figure_leave_event'
#             , 'axes_enter_event'
#             , 'axes_leave_event'
#             , 'close_event']
# for event in events:
#     fig.canvas.mpl_connect(event, func)

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()

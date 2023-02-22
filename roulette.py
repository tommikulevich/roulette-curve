# Roulette Visualization: Rolling Triangle with Arbitrary Parameters on Any Curve
# - Author: Tomash Mikulevich
# - Created with: PyCharm 2022.2.1 (Professional Edition - Student Pack)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def draw(i):
    # Getting data
    xy0 = polygon.get_xy()
    order = np.array(param.get_xdata())

    # Initial rotation conditions
    if xy0[1][1] - fun(xy0[1][0], u) <= 80 * dt:
        xy0, order = rollvec(xy0, order)

    x_rot = xy0[0][0]
    y_rot = xy0[0][1]

    # Checking collision of the first side of a triangle
    sidex_range, sidey_range = np.linspace(xy0[0][0], xy0[1][0], num), np.linspace(xy0[0][1], xy0[1][1], num)
    sidex_range, sidey_range = sidex_range[sidex_range >= 0], sidey_range[sidex_range >= 0]
    fun_range = fun(sidex_range, u)

    indX, indY = sidex_range[sidey_range - fun_range <= 1 / num], sidey_range[sidey_range - fun_range <= 1 / num]
    if np.size(indX) > 1:
        x_rot, y_rot = indX[-1], indY[-1]

    # Checking collision of the second side of a triangle
    sidex_range, sidey_range = np.linspace(xy0[1][0], xy0[2][0], num), np.linspace(xy0[1][1], xy0[2][1], num)
    sidex_range, sidey_range = sidex_range[sidex_range >= 0], sidey_range[sidex_range >= 0]
    fun_range = fun(sidex_range, u)

    indX, indY = sidex_range[sidey_range - fun_range <= 1 / num], sidey_range[sidey_range - fun_range <= 1 / num]
    if np.size(indX) > 1:
        x_rot, y_rot = indX[-1], indY[-1]
        xy0, order = rollvec(xy0, order)

    # Rotation
    phi = np.pi / 500

    xy0[0] = rotate(xy0[0], x_rot, y_rot, phi)
    xy0[1] = rotate(xy0[1], x_rot, y_rot, phi)
    xy0[2] = rotate(xy0[2], x_rot, y_rot, phi)

    # Setting data
    if np.size(xy0, axis=0) > 3:
        xy0 = xy0[:-1]

    polygon.set_xy(xy0)
    param.set_xdata(order)

    xR, yR = xy0[order[v]][0], xy0[order[v]][1]
    x0, y0 = np.sum(xy0, axis=0) / 3

    cyclogonX.append(xR)
    cyclogonY.append(yR)

    cyclogonLine.set_data(cyclogonX, cyclogonY)
    centrePoint.center = x0, y0
    radiusLine.set_data([xR, x0], [yR, y0])

    return polygon, centrePoint, radiusLine, cyclogonLine, param


def rotate(x, x_r, y_r, phi):
    return np.array([np.cos(phi) * (x[0] - x_r) + np.sin(phi) * (x[1] - y_r) + x_r,
                     -np.sin(phi) * (x[0] - x_r) + np.cos(phi) * (x[1] - y_r) + y_r])


def rollvec(n, m):
    if np.size(n, axis=0) > 3:
        n = n[:-1]
    return np.roll(n, -1, axis=0), np.roll(m, -1, axis=0)


def fun(x, y):
    return eval(y)


# Initialization
run = True
print("Specify the sides of the triangle: with the rule that any side should have a smaller length than the sum of "
      "the lengths of the other sides \n(e.g. a=4 b=3 c=2, so a < b+c, b < a+c, c < a+b)")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))

if a >= b + c or b >= a + c or c >= a + b:
    run = False

tMin = 0
tMax = 15
dt = 0.001
num = int(1 / dt)

t = np.arange(tMin, 2 * tMax, dt)
print("Specify the curve: if using the function, use 'np.'. \n"
      "Examples:  (0.2 * (x-5)) ** 2  ||  2*np.sin(x)  ||  3*np.sqrt(np.abs(0.5*x))  ||  np.exp(0.1*x)  ||  0*x: ")
u = input("Your curve: ")
f = fun(t, u)
v = 1

angleInit = np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

x = np.array([0, 0, -a * np.cos(np.pi / 2 - angleInit)])
y = np.array([fun(0, u), b + fun(0, u), a * np.sin(np.pi / 2 - angleInit) + fun(0, u)])
xy = np.stack((x, y), axis=1)

xC, yC = np.sum(x) / 3, np.sum(y) / 3

fig = plt.figure()
ax = plt.axes(xlim=(-a, 2 * tMax), ylim=(-5, tMax))
ax.set_aspect('equal')

functionLine, = ax.plot(t, f, linewidth=1.5)
polygon = plt.Polygon(xy, facecolor='none', edgecolor='purple', linewidth=0.5)
ax.add_patch(polygon)
centrePoint = plt.Circle((xC, yC), 0.1, fill=False)
ax.add_patch(centrePoint)

radiusX, radiusY = [], []
radiusLine, = ax.plot(radiusX, radiusY)
cyclogonX, cyclogonY = [], []
cyclogonLine, = ax.plot(cyclogonX, cyclogonY)

param, = ax.plot([2, 1, 0], [0, 0, 0])
param.remove()

if run:
    animate = FuncAnimation(fig, func=draw, frames=np.size(t), interval=1, repeat=False)
    plt.show()
else:
    print("Wrong length of sides! You can't draw a triangle like that...")

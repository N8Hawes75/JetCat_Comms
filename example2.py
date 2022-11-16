import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial

fig, ax = plt.subplots()
line1, = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return line1,

def update(frame, ln, x, y):
    x.append(frame)
    y.append(np.sin(frame))
    ln.set_data(x, y)
    return ln,

ani = FuncAnimation(
    fig, partial(update, ln=line1, x=[], y=[]),
    frames=np.linspace(0, 2*np.pi, 128),
    init_func=init, blit=True)

plt.show()

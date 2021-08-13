import numpy as np
from esn_dev.utils import normalize


def gauss2d_sequence(centers=None, sigma=0.5, N=1000, size=[20, 20], borders=[[-2, 2], [-2, 2]],dtype=None):
    """Creates a moving gaussian blob on grid with `size`"""
    if centers is None:
        # t = np.arange(0,500*np.pi,0.1)
        # x = np.sin(t)
        # y = np.cos(0.25*t)
        #t = np.arange(0, 200 * np.pi, 0.02 * np.pi)
        t = np.linspace(0, 200 * np.pi, N,dtype=dtype)

        x, y = np.sin(0.3 * t), np.cos(t,dtype=None)
        centers = np.array([y, x]).T

    yc, xc = centers[:, 0], centers[:, 1]
    yy = np.linspace(borders[0][0], borders[0][1], size[0],dtype=dtype)
    xx = np.linspace(borders[1][0], borders[1][1], size[1],dtype=dtype)

    xx = xx[None, :, None] - xc[:, None, None]
    yy = yy[None, None, :] - yc[:, None, None]

    gauss = (xx**2 + yy**2) / (2 * sigma**2)
    return np.exp(-gauss,dtype=dtype)


def square_sequence(toplefts=None, square_size=(3,3), size=(20,20), borders=[[-2, 2], [-2, 2]]):
    """Creates a moving gaussian blob on grid with `size`"""
    if toplefts is None:
        t = np.arange(0, 500 * np.pi, 0.1)
        xa = (size[1]-square_size[1]) / 2
        x  = xa * np.sin(t) + xa
        ya = (size[0]-square_size[0]) / 2
        y  = ya * np.cos(0.25 * t) + ya
        toplefts = np.rint([y, x]).T.astype(int)

    square = np.ones(square_size)
    seq    = np.zeros((toplefts.shape[0],) + size)
    sx, sy = square_size

    for (i,(cy,cx)) in enumerate(toplefts):
        seq[i, cy:cy+sy, cx:cx+sx] += square
    return seq


def mackey2d_sequence(N=5000, b=None, sigma=0.5, size=[20,20], borders=[[-2, 2], [-2, 2]],dtype=None):
    #T = N*0.1 
    #t = np.arange(0, T, 0.1,dtype=dtype)
    # t below is equal to that of gauss2d_sequence
    t = np.linspace(0, 200 * np.pi, N,dtype=dtype)
    x = normalize(mackey_sequence(b=b, N=N)) * 2 - 1
    y = np.cos(t,dtype=dtype)
    centers = np.array([y,x]).T
    return gauss2d_sequence(centers, sigma=sigma, size=size, borders=borders,dtype=dtype)


def mackey_sequence(b=None, N=3000):
    """Create the Mackey-Glass series"""
    c = 0.2
    tau = 17
    n = 10

    yinit = np.array([0.9697, 0.9699, 0.9794, 1.0003, 1.0319, 1.0703, 1.1076,
        1.1352, 1.1485, 1.1482, 1.1383, 1.1234, 1.1072, 1.0928, 1.0820, 1.0756,
        1.0739, 1.0759])

    if b is None:
        b = np.zeros(N) + 0.1
    if isinstance(b,float):
        b = np.zeros(N) + b

    y = np.zeros(N)
    y[:yinit.shape[0]] = yinit

    for i in range(tau, N - 1):
        yi = y[i] - b[i] * y[i] + c * y[i - tau] / (1 + y[i - tau]**n)
        y[i + 1] = yi
    return y
 
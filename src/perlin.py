import numpy as np


def _lerp(a, b, t):
    """
    Linear interpolation between a and b using t.
    """
    return a + t * (b - a)


def _fade(t, fade_a, fade_b, fade_c):
    """
    Fade function used to smooth the interpolation.
    Uses the classic Perlin fade curve: 6t^5 - 15t^4 + 10t^3.
    """
    return t * t * t * (t * (t * fade_a - fade_b) + fade_c)


def _gradient(ix, iy, seed_x, seed_y):
    """
    Generates a pseudo-random gradient vector at integer coordinates.
    This vector is deterministic and based on seed.
    """
    np.random.seed(ix * seed_x + iy * seed_y)
    angle = np.random.rand() * 2 * np.pi
    return np.array([np.cos(angle), np.sin(angle)])


def noise(x, y, seed_x, seed_y, fade_a, fade_b, fade_c):
    """
    2D Perlin noise function.

    Args:
        x (float): X coordinate
        y (float): Y coordinate

    Returns:
        float: Noise value in range approximately [-1, 1]
    """
    # Grid points surrounding the input
    x0 = int(np.floor(x))
    x1 = x0 + 1
    y0 = int(np.floor(y))
    y1 = y0 + 1

    # Local coordinates within grid cell
    sx = _fade(x - x0, fade_a, fade_b, fade_c)
    sy = _fade(y - y0, fade_a, fade_b, fade_c)

    # Gradient vectors at grid points
    g00 = _gradient(x0, y0, seed_x, seed_y)
    g10 = _gradient(x1, y0, seed_x, seed_y)
    g01 = _gradient(x0, y1, seed_x, seed_y)
    g11 = _gradient(x1, y1, seed_x, seed_y)

    # Offsets from grid points
    d00 = np.array([x - x0, y - y0])
    d10 = np.array([x - x1, y - y0])
    d01 = np.array([x - x0, y - y1])
    d11 = np.array([x - x1, y - y1])

    # Dot products between gradients and offsets
    n00 = np.dot(g00, d00)
    n10 = np.dot(g10, d10)
    n01 = np.dot(g01, d01)
    n11 = np.dot(g11, d11)

    # Bilinear interpolation of dot products
    ix0 = _lerp(n00, n10, sx)
    ix1 = _lerp(n01, n11, sx)
    value = _lerp(ix0, ix1, sy)

    return value

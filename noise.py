import random

tiledim = 16  # In nodes


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t, a, b):
    return a + t * (b - a)


def grad(hash, x, y, z):
    h = hash & 15
    if h < 8:
        u = x
    else:
        u = y
    if h < 4:
        v = y
    else:
        if h == 12 or h == 14:
            v = x
        else:
            v = z
    if h & 1 == 0:
        first = u
    else:
        first = -u
    if h & 2 == 0:
        second = v
    else:
        second = -v
    return first + second


p = []
for x in range(2 * tiledim):
    p.append(0)

permutation = []
for value in range(tiledim):
    permutation.append(value)
random.shuffle(permutation)

for i in range(tiledim):
    p[i] = permutation[i]
    p[tiledim + i] = p[i]


def noise(x, y, z):
    X = int(x) & (tiledim - 1)
    Y = int(y) & (tiledim - 1)
    Z = int(z) & (tiledim - 1)

    x -= int(x)
    y -= int(y)
    z -= int(z)

    u = fade(x)
    v = fade(y)
    w = fade(z)

    A = p[X] + Y
    AA = p[A] + Z
    AB = p[A + 1] + Z
    B = p[X + 1] + Y
    BA = p[B] + Z
    BB = p[B + 1] + Z

    return lerp(w, lerp(v,
                        lerp(u, grad(p[AA], x, y, z),
                             grad(p[BA], x - 1, y, z)),
                        lerp(u, grad(p[AB], x, y - 1, z),
                             grad(p[BB], x - 1, y - 1, z))),
                lerp(v,
                     lerp(u, grad(p[AA + 1], x, y, z - 1),
                          grad(p[BA + 1], x - 1, y, z - 1)),
                     lerp(u, grad(p[AB + 1], x, y - 1, z - 1),
                          grad(p[BB + 1], x - 1, y - 1, z - 1))))

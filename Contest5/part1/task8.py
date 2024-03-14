import math


L, x1, v1, x2, v2 = map(int, input().split())

# w = V / R
# R = L / (2 * Pi)
R = L / (2 * math.pi)

x11 = x1 / R
x22 = x2 / R
w1 = v1 / R
w2 = v2 / R

if x1 == x2:
    print('YES')
    print(0)
elif v1 == v2 == 0:
    print('NO')
else:
    print('YES')
    # cos(x11 + w1 * t) = cos(x22 + w2 * t)
    if w1 != w2 and w1 * w2 != 0:
        if (w2 - w1) * (x22 - x11) > 0:
            if w1 * w2 < 0:
                t1 = (2 * math.pi - abs(x22 - x11)) / (w1 - w2)
            else:
                t1 = min(
                    (2 * math.pi - (x22 - x11)) / (w1 - w2),
                    abs((4 * math.pi - (x22 + x11)) / (w1 + w2)),
                    (x22 + x11) / (w1 + w2),
                )
        else:
            t1 = (x22 - x11) / (w1 - w2)
    else:
        if w1 * w2 == 0:
            if x22 - x11 < 0 or w1 == 0:
                t1 = (2 * math.pi - (x22 + x11)) / (w1 + w2)
            else:
                t1 = (x22 - x11) / (w1 + w2)
        else:
            t1 = min(
                (x22 + x11) / (w1 + w2),
                (2 * math.pi - (x22 + x11)) / (w1 + w2),
            )
    print(x11, x22, w1, w2)
    print(abs(t1))

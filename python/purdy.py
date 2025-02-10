# Taken from https://web.archive.org/web/20070406100645/http://www.cs.uml.edu/~phoffman/xcinfo3.html
# Converted to python by chatgpt (idk c)
# find_time method written by chatgpt using reasoning


import math

def purdy1(d: float, tsec: float) -> float:
    b_vals = [11.15895, 4.304605, 0.5234627, 4.031560, 2.316157]
    r_vals = [3.796158e-2, 1.646772e-3, 4.107670e-4, 7.068099e-6, 5.220990e-9]

    v = sum(-b_vals[i] * math.exp(-r_vals[i] * d) for i in range(5))
    twsec = d / v

    k = 0.0654 - 0.00258 * v
    a = 85 / k
    b = 1 - 1035 / a
    p = a * (twsec / tsec - b)

    return p


def frac(d: float) -> float:
    if d < 110:
        return 0

    laps = int(d // 400)
    meters = d - laps * 400

    if meters <= 50:
        partlap = 0
    elif meters <= 150:
        partlap = meters - 50
    elif meters <= 250:
        partlap = 100
    elif meters <= 350:
        partlap = 100 + (meters - 250)
    else:
        partlap = 200

    tmeters = laps * 200 + partlap
    return tmeters / d


def purdy(dist: float, tsec: float) -> float:
    ptable = [
        40.0, 11.000, 50.0, 10.9960, 60.0, 10.9830, 70.0, 10.9620,
        80.0, 10.934, 90.0, 10.9000, 100.0, 10.8600, 110.0, 10.8150,
        120.0, 10.765, 130.0, 10.7110, 140.0, 10.6540, 150.0, 10.5940,
        160.0, 10.531, 170.0, 10.4650, 180.0, 10.3960, 200.0, 10.2500,
        220.0, 10.096, 240.0, 9.9350, 260.0, 9.7710, 280.0, 9.6100,
        300.0, 9.455, 320.0, 9.3070, 340.0, 9.1660, 360.0, 9.0320,
        380.0, 8.905, 400.0, 8.7850, 450.0, 8.5130, 500.0, 8.2790,
        550.0, 8.083, 600.0, 7.9210, 700.0, 7.6690, 800.0, 7.4960,
        900.0, 7.32000, 1000.0, 7.18933, 1200.0, 6.98066, 1500.0, 6.75319,
        2000.0, 6.50015, 2500.0, 6.33424, 3000.0, 6.21913, 3500.0, 6.13510,
        4000.0, 6.07040, 4500.0, 6.01822, 5000.0, 5.97432, 6000.0, 5.90181,
        7000.0, 5.84156, 8000.0, 5.78889, 9000.0, 5.74211, 10000.0, 5.70050,
        12000.0, 5.62944, 15000.0, 5.54300, 20000.0, 5.43785, 25000.0, 5.35842,
        30000.0, 5.29298, 35000.0, 5.23538, 40000.0, 5.18263, 50000.0, 5.08615,
        60000.0, 4.99762, 80000.0, 4.83617, 100000.0, 4.68988, -1.0, 0.0
    ]

    c1, c2, c3 = 0.20, 0.08, 0.0065

    i, dtemp = 0, 0.1
    while dist > dtemp and dtemp > 0:
        dtemp = ptable[i]
        i += 2
    if dtemp < 1:
        return 0

    i -= 2
    d3, pace3 = ptable[i], ptable[i + 1]
    d1, pace1 = ptable[i - 2], ptable[i - 1]

    t1 = d1 / pace1
    t3 = d3 / pace3
    # Interpolate to get the standard time t for the given distance
    t = t1 + (t3 - t1) * (dist - d1) / (d3 - d1)
    v = dist / t

    t950 = t + c1 + c2 * v + c3 * frac(dist) * v * v

    k = 0.0654 - 0.00258 * v
    a = 85 / k
    b_val = 1 - 950 / a
    p_val = a * (t950 / tsec - b_val)

    return p_val


def find_time(dist: float, purdy_score: float) -> float:
    """
    Given a distance and a purdy score, return the time (in seconds)
    that would yield that purdy score.
    """
    ptable = [
        40.0, 11.000, 50.0, 10.9960, 60.0, 10.9830, 70.0, 10.9620,
        80.0, 10.934, 90.0, 10.9000, 100.0, 10.8600, 110.0, 10.8150,
        120.0, 10.765, 130.0, 10.7110, 140.0, 10.6540, 150.0, 10.5940,
        160.0, 10.531, 170.0, 10.4650, 180.0, 10.3960, 200.0, 10.2500,
        220.0, 10.096, 240.0, 9.9350, 260.0, 9.7710, 280.0, 9.6100,
        300.0, 9.455, 320.0, 9.3070, 340.0, 9.1660, 360.0, 9.0320,
        380.0, 8.905, 400.0, 8.7850, 450.0, 8.5130, 500.0, 8.2790,
        550.0, 8.083, 600.0, 7.9210, 700.0, 7.6690, 800.0, 7.4960,
        900.0, 7.32000, 1000.0, 7.18933, 1200.0, 6.98066, 1500.0, 6.75319,
        2000.0, 6.50015, 2500.0, 6.33424, 3000.0, 6.21913, 3500.0, 6.13510,
        4000.0, 6.07040, 4500.0, 6.01822, 5000.0, 5.97432, 6000.0, 5.90181,
        7000.0, 5.84156, 8000.0, 5.78889, 9000.0, 5.74211, 10000.0, 5.70050,
        12000.0, 5.62944, 15000.0, 5.54300, 20000.0, 5.43785, 25000.0, 5.35842,
        30000.0, 5.29298, 35000.0, 5.23538, 40000.0, 5.18263, 50000.0, 5.08615,
        60000.0, 4.99762, 80000.0, 4.83617, 100000.0, 4.68988, -1.0, 0.0
    ]

    c1, c2, c3 = 0.20, 0.08, 0.0065

    # Find the correct segment in the table for this distance
    i, dtemp = 0, 0.1
    while dist > dtemp and dtemp > 0:
        dtemp = ptable[i]
        i += 2
    if dtemp < 1:
        return 0

    i -= 2
    d3, pace3 = ptable[i], ptable[i + 1]
    d1, pace1 = ptable[i - 2], ptable[i - 1]

    t1 = d1 / pace1
    t3 = d3 / pace3
    t = t1 + (t3 - t1) * (dist - d1) / (d3 - d1)
    v = dist / t

    t950 = t + c1 + c2 * v + c3 * frac(dist) * v * v

    k = 0.0654 - 0.00258 * v
    a_val = 85 / k
    b_val = 1 - 950 / a_val

    # In purdy(), the score is computed as:
    #   purdy_score = a_val * (t950/tsec - b_val)
    # so solving for tsec gives:
    #   tsec = t950 / ((purdy_score / a_val) + b_val)
    tsec = t950 / ((purdy_score / a_val) + b_val)
    return tsec

def convert_distance(dist: float, time: float, new_dist: float) -> float:
    """
    Given a distance, time, and a new distance, return the time
    that would be equivalent to the given time for the new distance.
    """
    return find_time(new_dist, purdy(dist, time))

# Example usage:
# thousand_points = purdy(1000, 155.55)
# print("Purdy score for 1000m in 155.55 sec:", thousand_points)
# print("Required time for 100m to achieve that Purdy score:", find_time(400, thousand_points))


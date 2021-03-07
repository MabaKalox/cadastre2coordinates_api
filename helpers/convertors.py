import math


def LKS92TM_to_Geodetic(x_m, y_m):
    # constants
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = 2 * f - pow(f, 2)
    false_nm = -6000000.0
    false_em = 500000.0
    k0 = 0.9996
    n_long_c_merid = 24
    n1 = 0.00167922038638372
    n2 = pow(n1, 2)
    n3 = n1 * n2
    n4 = pow(n2, 2)
    g = 111132.952547919

    e4 = x_m - false_nm
    f4 = e4 / k0
    h4 = y_m - false_em
    i4 = h4 / k0
    j4 = (f4 * math.pi) / (g * 180)
    x4 = ((3 * n1 / 2.0) - (27 * n3 / 32.0)) * math.sin(j4 * 2)
    ac4 = ((21 * n2 / 16.0) - (55 * n4 / 32.0)) * math.sin(j4 * 4)
    ah4 = (151 * n3) * math.sin(j4 * 6) / 96.0
    am4 = 1097 * n4 * math.sin(j4 * 8) / 512.0
    ar4 = j4 + x4 + ac4 + ah4 + am4
    as4 = math.sin(ar4)
    at4 = 1 / math.cos(ar4)
    ba4 = a / math.pow((1 - e2 * as4 * as4), 0.5)
    bl4 = math.tan(ar4)
    az4 = a * (1 - e2) / math.pow((1 - e2 * as4 * as4), 1.5)
    bb4 = i4 / ba4
    bc4 = bb4 * bb4
    bd4 = bb4 * bc4
    be4 = bc4 * bc4
    bf4 = be4 * bb4
    bg4 = bd4 * bd4
    bh4 = bb4 * bg4
    bm4 = bl4 * bl4
    bn4 = bl4 * bm4
    bo4 = bm4 * bm4
    bq4 = bn4 * bn4
    br4 = ba4 / az4
    bs4 = br4 * br4
    bt4 = bs4 * br4

    bu4 = bs4 * bs4
    ce4 = -((bl4 / (k0 * az4)) * bb4 * h4 / 2.0)
    cj4 = (bl4 / (k0 * az4)) * (bd4 * h4 / 24) * (-4 * bs4 + 9 * br4 * (1 - bm4) + 12 * bm4)
    co4 = -(bl4 / (k0 * az4)) * (bf4 * h4 / 720.0) * (
                8 * bu4 * (11 - 24 * bm4) - 12 * bt4 * (21 - 71 * bm4) + 15 * bs4 * (
                    15 - 98 * bm4 + 15 * bo4) + 180 * br4 * (5 * bm4 - 3 * bo4) + 360 * bo4)
    ct4 = (bl4 / (k0 * az4)) * (bh4 * h4 / 40320.0) * (1385 + 3633 * bm4 + 4095 * bo4 + 1575 * bq4)
    latitude_dd = ((ar4 + ce4 + cj4 + co4 + ct4) / math.pi) * 180

    ec4 = (n_long_c_merid / 180.0) * math.pi
    eh4 = at4 * bb4
    em4 = -at4 * (bd4 / 6.0) * (br4 + 2 * bm4)
    er4 = at4 * (bf4 / 120.0) * (-4 * bt4 * (1 - 6 * bm4) + bs4 * (9 - 68 * bm4) + 72 * br4 * bm4 + 24 * bo4)
    ew4 = -at4 * (bh4 / 5040.0) * (61 + 662 * bm4 + 1320 * bo4 + 720 * bq4)
    longitude_dd = ((ec4 + eh4 + em4 + er4 + ew4) / math.pi) * 180

    return latitude_dd, longitude_dd

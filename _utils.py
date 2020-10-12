def floatfrombytes(bs):
    hs = ''.join(['%02X' % x for x in bs])
    return float.fromhex(hs)

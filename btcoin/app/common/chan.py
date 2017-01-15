def chan_min(objs, key):
    return min([getattr(e, key) for e in objs])


def chan_max(objs, key):
    return max([getattr(e, key) for e in objs])

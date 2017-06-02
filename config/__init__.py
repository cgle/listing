import os
import ujson
import collections

base_dir = os.path.dirname(os.path.realpath(__file__))

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def load(*fnames):
    conf = {}    
    for fname in fnames:
        file_path = os.path.join(base_dir, fname)
        this_conf = ujson.loads(open(file_path, 'r').read())
        update(conf, this_conf)
    return conf

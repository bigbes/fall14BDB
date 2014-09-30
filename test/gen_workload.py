#!/usr/bin/env python

import yaml
import random

import itertools
import string

from ordered_set import OrderedSet

class Distribution(object):
    pass

class NoneDistribution(Distribution):
    def __init__(self, key, val=None):
        self.key = key
        self.val = val
        self.pos = 0

    def get(self):
        if self.pos >= len(self.key):
            self.pos = 0

        key = self.key[self.pos]
        val = None if self.val is None else random.choice(self.val)
        self.pos +=1
        return (key, val)

class UniformDistribution(Distribution):
    pass

def randomword(length):
    return ''.join([random.choice(string.hexdigits) for k in xrange(length)])

class Workload(object):
    wl_defaults = {
        'get': 50,
        'put': 50,
        'ops': 200,
        'distrib': 'none',
        'shuffle': False,
        'key_size': 20,
        'min_val_size': 128,
        'max_val_size': 4096,
    }

    key_file = 'cities.txt'

    avail_distrib = [
        'uniform',
        #'pareto',
        #'hotspot',
        #'latest',
        'none',
    ]

    def read_config(self, conf):
        cfg = {} if cfg is None else yaml.load(open(conf, 'r').read())
        assert(isinstance(cfg, dict))
        if ('get' in cfg) or ('put' in cfg):
            self.get = cfg.get('get', 0)
            self.put = cfg.get('put', 0)
        else:
            self.get = self.wl_defaults['get']
            self.put = self.wl_defaults['put']
        assert(self.get + self.put == 100)
        self.ops = cfg.get('ops', self.wl_defaults['ops'])
        self.distrib = cfg.get('distrib', self.wl_defaults['distrib'])
        assert(self.distrib in self.avail_distrib)
        self.shuffle = cfg.get('shuffle', self.wl_defaults['shuffle'])
        self.key_size = cfg.get('key_size', self.wl_defaults['key_size'])
        self.min_val_size = cfg.get('min_val_size', self.wl_defaults['min_val_size'])
        self.max_val_size = cfg.get('max_val_size', self.wl_defaults['max_val_size'])
        assert(isinstance(self.shuffle, bool))

    def __init__(self, cfg=None):
        self.read_config(cfg)
        self.keyset = OrderedSet()
        self.opset  = []
        self.opset.extend([0] * long(self.ops*self.put/100))
        self.opset.extend([1] * long(self.ops*self.get/100))
        if self.shuffle:
            random.shuffle(self.opset)

    def generate_insert(self):
        self.insert_count = xrange()

    def generate(self):
        self.keys = open(self.key_file, 'r').read().split()
        if self.shuffle:
            random.shuffle(self.keys)

        self.keys = [k[:20] for k in self.keys]
        self.keys = filter((lambda x: len(x) > 10), self.keys)
        self.keys = self.keys[:500]
        self.vals = []
        for k in xrange(len(self.keys)):
            self.vals.append(
                    randomword(random.randint(self.min_val_size, self.max_val_size))
            )
        put = NoneDistribution(self.keys, self.vals)
        get = NoneDistribution(self.keyset)
        for k in self.opset:
            if k == 0:
                kv = put.get()
                self.keyset.append(kv[0])
                yield ('put', kv[0], kv[1])
            elif k == 1:
                kv = get.get()
                yield ('get', kv[0])


if __name__ == '__main__':
    path = os.path.dirname(sys.argv[0])
    if not path:
        path = '.'
    os.chdir(path)

    wl = Workload()
    with open('1.out', 'w') as f:
        for k in wl.generate():
            f.write(' '.join(k)+'\n')

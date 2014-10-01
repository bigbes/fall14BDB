#!/usr/bin/env python

import os
import sys
import yaml
import random

import string

import argparse

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
        'max_val_size': 256,
    }

    key_file = 'keys.txt'
    val_file = 'values.txt'

    avail_distrib = [
        # 'uniform',
        # 'pareto',
        # 'hotspot',
        # 'latest',
        'none',
    ]

    def read_config(self, conf):
        cfg = {} if conf is None else yaml.load(open(conf, 'r').read())
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
        self.keys = open(self.key_file, 'r').read().split('\n')
        if self.shuffle:
            random.shuffle(self.keys)
        self.vals = open(self.val_file, 'r').read().split('\n')
        if self.shuffle:
            random.shuffle(self.vals)
        put = NoneDistribution(self.keys, self.vals)
        get = NoneDistribution(self.keyset)
        for k in self.opset:
            if k == 0:
                kv = put.get()
                self.keyset.append(kv[0])
                yield ['put', kv[0], kv[1]]
            elif k == 1:
                kv = get.get()
                yield ['get', kv[0]]

def chdir():
    path = os.path.dirname(sys.argv[0])
    if not path:
        path = '.'
    os.chdir(path)

def parse_args(cur_path):
    parser = argparse.ArgumentParser(
            description = "Generating workload for testing HW1")
    parser.add_argument(
            '--config',
            default = None,
            help    = 'Config file'
    )
    parser.add_argument(
            '--output',
            default = 'output',
            help    = 'Output file'
    )

    args = parser.parse_args()
    if args.config:
        args.config = os.path.join(cur_path, args.config)
    else:
        args.config = None
    if args.output:
        args.output = os.path.join(cur_path, args.output)
        args.output += '.in'
    return args


if __name__ == '__main__':
    cur_path = os.getcwd()
    chdir()
    cur_args = parse_args(cur_path)

    wl = Workload(cur_args.config)
    with open(cur_args.output, 'w') as f:
        f.write(yaml.dump([k for k in wl.generate()]))

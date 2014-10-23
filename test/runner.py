#!/usr/bin/env python

import os
import sys
import yaml
import argparse

from cStringIO import StringIO

from lib.database import Database

def run_workload(fl, db, out):
    fl = yaml.load(fl.read())
    for arr in fl:
        if arr[0] == 'put':
            db.put(arr[1], arr[2])
        elif arr[0] == 'get':
            val = db.get(arr[1])
            out.write(val + '\n')
        elif arr[0] == 'del':
            db.delete(arr[1])
            try:
                val = db.get(arr[1])
            except:
                pass
            else:
                raise ValueError('element wasn\'t deleted')

def parse_args(cur_path):
    parser = argparse.ArgumentParser(
            description = "Generating workload for testing HW1")
    parser.add_argument(
            '--workload',
            default = 'workload.in',
            help    = 'config file'
    )
    parser.add_argument(
            '--new',
            action  = 'store_true',
            default = False,
            help    = 'new workload flag'
    )
    parser.add_argument(
            '--so',
            default = './libmydb.so',
            help    = 'shared library for DB'
    )


    args = parser.parse_args()
    if args.workload:
        args.workload = os.path.join(cur_path, args.workload)
    else:
        args.workload = None
    if args.so:
        args.so = os.path.join(cur_path, args.so)
    return args

def chdir():
    path = os.path.dirname(sys.argv[0])
    if not path:
        path = '.'
    os.chdir(path)

if __name__ == '__main__':
    cur_path = os.getcwd()
    chdir()
    cur_args = parse_args(cur_path)
    error = False
    db = Database(cur_args.so)
    wl = open(cur_args.workload)
    out = StringIO()
    try:
        run_workload(wl, db, out)
    except Exception as e:
        error =  repr(e)
    output = cur_args.workload.replace('.in', '.out')
    print "=" * 80
    print "Library:", cur_args.so
    if cur_args.new:
        open(output, 'w').write(out.getvalue())
        print "Workload output successfully generated"
        print "Output:", output
    else:
        print "Test with workload " + repr(cur_args.workload)
        if (open(output, 'r').read() == out.getvalue()) and not error:
            print "Result is OK."
        else:
            open(output + '.bad', 'w').write(out.getvalue())
            print "Result is not OK.",
            if error:
                print "Error: " + error,
            print ''
    print "=" * 80

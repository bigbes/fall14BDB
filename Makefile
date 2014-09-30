all:
	gcc mydb.c -std=c99 -shared -fPIC -o libmydb.so

gen_workload:
	python test/gen_workload.py 1.yml 1.wl

test:
	python test/runner.py ../libmydb.so 1.wl

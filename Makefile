all:
	gcc mydb.c -std=c99 -shared -fPIC -o libmydb.so

gen_workload:
	python test/gen_workload.py --output workload
	python test/runner.py --new --workload workload.in --so ./libmydb.so

runner:
	python test/runner.py --workload workload.in --so ./libmydb.so

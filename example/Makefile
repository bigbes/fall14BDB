all:
	make -C third_party/sophia
	cp third_party/sophia/db/libsophia.a ./
	gcc bdb_sphia.c -std=c99 -shared -fPIC -o libmydb.so -lsophia -L. -Wall

gen_workload:
	python ../test/gen_workload.py --output workload
	python ../test/runner.py --new --workload workload.in --so ./libmydb.so

runner:
	python ../test/runner.py --workload workload.in --so ./libmydb.so

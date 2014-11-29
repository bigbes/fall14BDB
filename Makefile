all:
	gcc mydb.c -std=c99 -shared -fPIC -o libmydb.so

gen_workload:
	@make -C example
	@python test/gen_workload.py --output workload_custom
	@python test/runner.py --new --workload workload_custom.in --so example/libdbsophia.so

gen_workload_uni_1:
	@python test/gen_workload.py --output   workload.uni --config example/uni.schema.yml
	sed 's/!!binary |\n\s*\(.*\)\(\n\)/!!binary "\1"\2/g' workload.uni.in > workload.uni.in_1
	mv workload.uni.in_1 workload.uni.in

gen_workload_uni:
	make -C test_cpp test_uni
	mv workload.uni.out.yours workload.uni.out

gen_workload_old_1:
	@python test/gen_workload.py --output   workload.old --config example/old.schema.yml
	sed 's/!!binary |\n\s*\(.*\)\(\n\)/!!binary "\1"\2/g' workload.old.in > workload.old.in_1
	mv workload.old.in_1 workload.old.in

gen_workload_old:
	make -C test_cpp test_old
	mv workload.old.out.yours workload.old.out

gen_workload_lat_1:
	@python test/gen_workload.py --output   workload.lat --config example/lat.schema.yml
	sed 's/!!binary |\n\s*\(.*\)\(\n\)/!!binary "\1"\2/g' workload.lat.in > workload.lat.in_1
	mv workload.lat.in_1 workload.lat.in

gen_workload_lat:
	make -C test_cpp test_lat
	mv workload.lat.out.yours workload.lat.out

gen_workload_all: gen_workload_uni gen_workload_old gen_workload_lat

gen_workload_all_1: gen_workload_uni_1 gen_workload_old_1 gen_workload_lat_1

runner:
	python test/runner.py --workload custom_workloads/workload.in --so ./libmydb.so

runner_rw:
	python test/runner.py --workload custom_workloads/workload_custom.in --so ./libmydb.so

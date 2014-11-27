#include <sys/time.h>

#include <cstring>
#include <vector>
#include <iostream>
#include <fstream>

#include <yaml-cpp/yaml.h>

#include "database.h"

YAML::Node parse_yaml_workload(char *wl_name) {
	return YAML::LoadFile(wl_name);
}

int main() {
	Database *db = new Database(const_cast<char *>("./libmydb.so"),
			const_cast<char *>("./mydbpath"));
	YAML::Node workload = parse_yaml_workload(const_cast<char *>("../custom_workloads/workload.in"));
	std::ofstream out ("../custom_workloads/workload.out.yours");
	struct timespec t1, t2; memset(&t1, 0, sizeof(t1)); memset(&t2, 0, sizeof(t2));
	uint64_t time = 0;
	for (YAML::const_iterator it = workload.begin(); it != workload.end(); ++it) {
		auto op = it->as< std::vector<std::string> >();
		int retval = 0;
		if (op[0] == std::string("put")) {
			clock_gettime(CLOCK_MONOTONIC, &t1);
			retval = db->put(op[1], op[2]);
			clock_gettime(CLOCK_MONOTONIC, &t2);
			time += (t2.tv_sec - t1.tv_sec) * 1e9 + (t2.tv_nsec - t1.tv_nsec);
		} else if (op[0] == std::string("get")) {
			char *val;
			size_t val_size;
			clock_gettime(CLOCK_MONOTONIC, &t1);
			retval = db->get(op[1], &val, &val_size);
			clock_gettime(CLOCK_MONOTONIC, &t2);
			time += (t2.tv_sec - t1.tv_sec) * 1e9 + (t2.tv_nsec - t1.tv_nsec);
			out.write(val, val_size) << "\n";
		} else if (op[0] == std::string("del")) {
			clock_gettime(CLOCK_MONOTONIC, &t1);
			retval = db->del(op[1]);
			clock_gettime(CLOCK_MONOTONIC, &t2);
			time += (t2.tv_sec - t1.tv_sec) * 1e9 + (t2.tv_nsec - t1.tv_nsec);
		} else {
			std::cout << "bad op\n";
		}
	}
	std::cout << "Overall lib time: " << ((double )time / 1e9) << "\n";
}

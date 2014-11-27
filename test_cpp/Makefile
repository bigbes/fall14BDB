all:
	g++ main.cpp database.cpp -lyaml-cpp -ldl -o test_speed --std=c++11 -lpthread
test:
	time ./test_speed
	rm -rf ./mydbpath

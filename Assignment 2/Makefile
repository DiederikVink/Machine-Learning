#!/bin/bash

run: bin/assignment2
	@./bin/assignment2

bin/assignment2: objects/generate.o objects/main.o objects/perceptron.o objects/rm.o objects/test_error.o
	@g++ -o bin/assignment2 objects/generate.o objects/main.o objects/perceptron.o objects/rm.o objects/test_error.o

objects/generate.o: src/generate.cpp src/generate.hpp
	@g++ -std=c++11 -c src/generate.cpp -o objects/generate.o

objects/main.o: src/main.cpp src/generate.hpp src/perceptron.hpp src/test_error.hpp
	@g++ -std=c++11 -c src/main.cpp -o objects/main.o

objects/perceptron.o : src/perceptron.cpp src/perceptron.hpp
	@g++ -std=c++11 -c src/perceptron.cpp -o objects/perceptron.o

objects/test_error.o : src/test_error.cpp src/perceptron.hpp src/classify.hpp src/generate.hpp src/test_error.hpp
	@g++ -std=c++11 -c src/test_error.cpp -o objects/test_error.o

objects/rm.o : src/rm.cpp src/rm.hpp
	@g++ -std=c++11 -I externals/ -c src/rm.cpp -o objects/rm.o

clean:
	@rm -f objects/*.o bin/assignment2 src/*.swp

cleanup:
	@rm -f objects/*.o src/*.swp

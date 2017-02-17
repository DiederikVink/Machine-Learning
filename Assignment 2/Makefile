#!/bin/bash

run: bin/assignment2
	@./bin/assignment2
	@python src/graph.py

bin/assignment2: objects/generate.o objects/main.o objects/perceptron.o objects/classify.o objects/rm.o
	@g++ -o bin/assignment2 objects/generate.o objects/main.o objects/perceptron.o objects/classify.o objects/rm.o

objects/generate.o: src/generate.cpp src/generate.h
	@g++ -std=c++11 -c src/generate.cpp -o objects/generate.o

objects/main.o: src/main.cpp src/generate.h
	@g++ -std=c++11 -c src/main.cpp -o objects/main.o

objects/classify.o: src/classify.cpp src/classify.hpp
	@g++ -std=c++11 -c src/classify.cpp -o objects/classify.o

objects/perceptron.o : src/perceptron.cpp src/perceptron.hpp
	@g++ -std=c++11 -c src/perceptron.cpp -o objects/perceptron.o

objects/rm.o : src/rm.cpp src/rm.hpp
	@g++ -std=c++11 -c src/rm.cpp -o objects/rm.o

clean:
	@rm -f objects/*.o bin/assignment2 src/*.swp

cleanup:
	@rm -f objects/*.o src/*.swp

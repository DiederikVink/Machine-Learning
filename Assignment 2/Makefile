#!/bin/bash

run: bin/assignment2
	@./bin/assignment2
	@python src/graph.py

bin/assignment2: objects/generate.o objects/main.o
	@g++ -o bin/assignment2 objects/generate.o objects/main.o

objects/generate.o: src/generate.cpp src/generate.h
	@g++ -std=c++11 -c src/generate.cpp -o objects/generate.o

objects/main.o: src/main.cpp src/generate.h
	@g++ -std=c++11 -c src/main.cpp -o objects/main.o

clean:
	@rm -f objects/*.o bin/assignment2 src/*.swp

cleanup:
	@rm -f objects/*.o src/*.swp

#!/bin/bash

run: bin/assignment2
	./bin/assignment2

bin/assignment2: objects/generate.o objects/main.o
	g++ -o bin/assignment2 objects/generate.o objects/main.o

objects/generate.o: src/generate.cpp src/generate.h
	g++ -c src/generate.cpp -o objects/generate.o

objects/main.o: src/main.cpp src/generate.h
	g++ -c src/main.cpp -o objects/main.o

clean:
	rm -f objects/*.o bin/assignment2

cleanup:
	rm -f *.o

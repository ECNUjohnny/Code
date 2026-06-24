CXX = g++

test04: test05.o test04.o
	$(CXX) test05.o test04.o -o test4.exe

test05.o: test04.h test05.cpp
	$(CXX) -c test05.cpp -o test05.o

test04.o: test04.h test04.cpp
	$(CXX) -c test04.cpp -o test04.o


.PHONY: clean

clean: 
	del /Q /F *.o test04.exe
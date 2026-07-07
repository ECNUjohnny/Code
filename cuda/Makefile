COMPILER = nvcc

CFLAGS = -Xcompiler "/utf-8"

test01: 
	$(COMPILER) $(CFLAGS) test01.cu -o test01

.PHONY: clean

clean:
	del /Q /F *.o *.exe

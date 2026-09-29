COMPILER = nvcc

CFLAGS = -arch=native -Xcompiler -utf-8

TARGET = test01

all: $(TARGET)

$(TARGET): $(TARGET).obj  
	$(COMPILER) $(CFLAGS) $(TARGET).obj -o $(TARGET) -L ./lib

$(TARGET).obj: $(TARGET).cu
	$(COMPILER) $(CFLAGS) -c $(TARGET).cu -o $(TARGET).obj

.PHONY: all clean

clean:
	del /Q /F *.obj

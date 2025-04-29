To utilize the module

1. Build the cbi tool

# root @ b21cb147824a in /final
$ make install 

2. Make the cbi instrumentations

# root @ b21cb147824a in /final
$ mkdir build && cd build

# root @ b21cb147824a in /final/build
$ cmake ..
$ make

3. Copy the c files interested into the test folders

# root @ b21cb147824a in /final/build
$ cd ../test

4. Run the following commands

# root @ b21cb147824a in /final/test
$ make fuzz-all
$ make analyze-all

5. Reports and graphs are in /final/test/reports

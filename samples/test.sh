g++ test.cpp calc.cpp -fprofile-arcs -ftest-coverage 

./a.out

gcov test.cpp -bc
gcov calc.cpp -bc
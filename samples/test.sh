g++ test.cpp -fprofile-arcs -ftest-coverage 

./a.out

gcov test.cpp -bc
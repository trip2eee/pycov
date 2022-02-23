#include <iostream>

void foo(const int n)
{
    for(int i = 0; i < n; i++)
    {
        std::cout << "foo " << i << "\n";
    }
}

void bar(const int n)
{
    for(int i = 0; i < n; i++)
    {
        std::cout << "bar " << i << "\n";
    }
}


int main()
{
    int a = 10;
    if(a > 0)
    {
        std::cout << "a is greater than or equal to 10\n";
        foo(a);
    }
    else
    {
        std::cout << "a is less than 10\n";
        bar(a);
    }

    return 0;
}
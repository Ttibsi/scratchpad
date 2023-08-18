#include <fstream>
#include <iostream>

int main(void) {
    std::ifstream f (__FILE__);
    do {
        char buf = f.get();
        if (f.good()) std::cout << buf;
    } while (f);
}

#include <iostream>
#include <string.h>
#include <unistd.h>

// Quick way to check if the current user has write access to a given file

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {
        // man access
        int ret = access(argv[i], W_OK); // switch to R_OK for read access
        std::cout << argv[i] << ": " << strerror(errno) << "(" << ret << ")\n";
    }

    return 0;
}

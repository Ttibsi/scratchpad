#include <algorithm>
#include <array>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

// Needs to be compiled with c++20 
// Will print out the stdout result of the given shell command with no trailing
// newline char

std::string shell_exec(std::string cmd) {
    cmd += " 2>/dev/null";
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }

    std::erase_if(result, [](auto ch){
        return (ch == '\n' ||
        ch == '\r'); 
    });

    return result;
}

int main() {
    std::string o = shell_exec("git rev-parse --abbrev-ref HEAD");
    std::cout << o;
    return 0;
}

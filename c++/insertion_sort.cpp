// Compile with -std=c++23
#include <array>
#include <iostream>

template <std::size_t len>
consteval std::array<int, len> insertion_sort(std::array<int, len> a) {
    for (int i = 1; i < a.size(); i++) {
        int j = i - 1;
        const int k = a.at(i);

        while (j >= 0 && a.at(j) > k) {
            a.at(j + 1)  = a.at(j);
            j--;
        }

        a.at(j + 1) = k;
    }

    return a;
}

template <std::size_t len>
constexpr void print(const std::array<int, len>& a) {
    std::cout << "[";
    for (auto&& i: a) {
        std::cout << i << " ";
    }

    std::cout << "]\n";
}

int main() {
    constexpr std::array a = {64, 34, 25, 12, 22, 11, 90};
    print<a.size()>(a);
    constexpr std::array out = insertion_sort<a.size()>(a);
    print<out.size()>(out);
}

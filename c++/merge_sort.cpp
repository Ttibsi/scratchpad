#include <iostream>
#include <vector>

std::vector<int> merge(std::vector<int> v1, std::vector<int> v2) {
    std::vector<int> new_v = {};
    new_v.reserve(v1.size() + v2.size());

    int i = 0;
    int j = 0;
    while (i + j < v1.size() + v2.size()) {
        if (j == v2.size() || (i < v1.size() && v1.at(i) < v2.at(j))) {
            new_v.push_back(v1.at(i));
            i++;
        } else {
            new_v.push_back(v2.at(j));
            j++;
        }
    }

    return new_v;
}

std::vector<int> merge_sort(std::vector<int> v) {
    std::size_t len = v.size();
    if (len < 2) { return v; }

    std::size_t mid = int(len / 2);
    std::vector v1 = std::vector(v.begin(), v.begin() + mid);
    std::vector v2 = std::vector(v.begin() + mid, v.end());

    v1 = merge_sort(v1);
    v2 = merge_sort(v2);

    v = merge(v1, v2);
    return v;
}

int main() {
    std::vector<int> v = {1,2,5,27,8,1,0,7,6};
    v = merge_sort(v);

    for (auto&& i: v) { std::cout << i << " "; }
    std::cout << "\n";
}

#ifndef CONST_MAP_H
#define CONST_MAP_H

#include <algorithm>
#include <array>
#include <stdexcept>

// godbolt example usage: https://godbolt.org/z/ze8YoP7dc

template <typename K, typename V>
struct MapItem {
    K key;
    V value;
};

template <typename K, typename V, std::size_t Size>
class Map {
    private:
        std::array<MapItem<K, V>, Size> data;

    public:
        template<typename... Args>
        constexpr Map(Args&&... args) : data{{std::forward<Args>(args)...}} {}
        
        [[nodiscard]] consteval V at(const K& key) const {
            const auto it = std::find_if(
                begin(data),
                end(data),
                [&key](const auto &v) { return v.key == key; }
                );

            if (it != end(data)) {
                return it->value;
            } else {
                throw std::range_error("Not Found");
            }
        } 
};

# endif // CONST_MAP_H

// #include <string_view>
// using namespace std::literals::string_view_literals;
// static constexpr Map<std::string_view, int, 5> test = {
//    MapItem{"one"sv, 1},
//    MapItem{"two"sv, 2},
//    MapItem{"three"sv, 3},
//    MapItem{"four"sv, 4},
//    MapItem{"five"sv, 5}
//};



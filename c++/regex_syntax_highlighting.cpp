#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <regex>
#include <utility>

// To use: Compile it and pass the binary a python file as argv[1]
// This should be easily expandable to other languages and parts of the language 
// when needed - just add a new Token for the type of value being added, the
// colour for it, and the regex for it.

enum Language {
    PYTHON
};

enum Token {
    FUNC_CALL,
    NUMBER_LITERAL,
    STRING_LITERAL,
    COMMENT,
    KEYWORD,
    TYPE,
};

// can I create these at compile time - they don't change at runtime
static std::unordered_map<Token, std::string> default_theme = {
    {FUNC_CALL, "#6666ff"},
    {NUMBER_LITERAL, "#ff2222"},
    {STRING_LITERAL, "#22ff22"},
    {COMMENT, "#666666"},
    {KEYWORD, "#09D0EF"},
    {TYPE, "#C4A000"},
};


static std::unordered_map<Language, std::vector<std::pair<Token, std::string>>> hl_groups = {
    {PYTHON, {
        {NUMBER_LITERAL, "([0-9])"}, // This has to go first or it overwrites other escape codes
        // https://dev.to/xowap/the-string-matching-regex-explained-step-by-step-4lkp
        {STRING_LITERAL, R"str(("([^"\\]|\\.)*"))str" },
        {KEYWORD, "\\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\\b"},
        {COMMENT, "(# *.+)"},
        {FUNC_CALL, "(\\w+)(?=\\()"},
        {TYPE, "\\b(str|int|bool|tuple|list|dict|set|Any|Sequence|Union|None)(?![a-zA-Z])"},

    },}
};

std::vector<std::string> open_file(const std::string &file) {
    std::ifstream ifs(file);
    std::string line;
    std::vector<std::string> lines;

    if (ifs.peek() == std::ifstream::traits_type::eof()) { return { "" }; }
    while (std::getline(ifs, line)) { lines.push_back(line); }
    return lines;
}

std::string parse_colour(std::string raw) {
    std::string ret = "";

    int placeholder;
    placeholder = std::stoi(raw.substr(1,2), 0, 16);
    ret += std::to_string(placeholder) + ";";

    placeholder = std::stoi(raw.substr(3,2), 0, 16);
    ret += std::to_string(placeholder) + ";";

    placeholder = std::stoi(raw.substr(5,2), 0, 16);
    ret += std::to_string(placeholder) + "m";

    return ret;
}

// NOTE: When implmenting this into iris, make sure this is on the file contents
// as a single string, not as a vec of strings, so that multiline searches
// can occur (such as multiline strings/comments)
std::vector<std::string> regex_scan(std::vector<std::string> lines) {
    for (int i = 0; i < lines.size(); i++) {
        for (auto&& re : hl_groups[PYTHON]) {
            std::regex r;
            try {
                r = std::regex(re.second);
            } catch (const std::regex_error &e) {
                std::cout << "regex error: " << re.second << "\n";
            }
            std::smatch match; // string-match
            std::regex_search(lines[i], match, r);

            std::string ansi_colour = "\x1b[38;2;" + parse_colour(default_theme[re.first]);

            std::string res_text = ansi_colour + "$1\x1B[0m"; 
            std::string updated = std::regex_replace(lines[i], r, res_text);

            lines[i] = updated;
        }
    }

    return lines;
}

void cleanup(std::vector<std::string>& lines) {
    std::string close_suffix = "[0m";

    for (auto&& line: lines) {
        if (line.empty()) { continue; }
        int open_count = 0;

        for (int i = 0; i < line.size(); i++) {
            if (static_cast<int>(line.at(i)) == 27) {
                // close
                if (line.substr(i + 1, close_suffix.size()) == close_suffix) {
                    if (open_count > 1) {
                        line.replace(i, line.substr(i, line.size()).find("m") + 1, "");
                    }
                    open_count--;
                // open
                } else {
                    open_count++;
                    if (open_count > 1) {
                        line.replace(i, line.substr(i, line.size()).find("m") + 1, "");
                    }
                }
            }
        }
    }
}

int main(int argc, char** argv) {
    // Step 1: get file as vector of strings
    auto lines = open_file(argv[1]);

    // Step 2: get type of file
    std::string lang = "py";

    // Step 3: Scan each line and insert ansi colouring from regexes
    auto new_lines = regex_scan(lines);

    // Step 4: Double check there aren't any nested lines
    cleanup(new_lines);

    for (auto&& l: new_lines) { std::cout << l << "\n"; }
    return 0;
}

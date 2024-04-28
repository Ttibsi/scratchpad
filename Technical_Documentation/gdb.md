# How to debug c++ code
1. Compile with `-g` 
    - cmake: `add_compile_options("-g")`
2. `gdb ./myexe`
    - if we're debugging rawterm code, make sure to enable the `RAWTERM_DEBUG` env var as `1` or `true`
3. `tui enable` or `layout next` 
    - With the latter, press enter and you can see both the source code and the assembly
4. breakpoints!
    - see this link: http://www.gdbtutorial.com/gdb-breakpoints-example
    - Most commonly, you'll want to set a breakpoint on a specific line:
        `break myfile.cpp:12` is the syntax you want there
5. `run`
6. navigation
    - `next` goes to the next line of source code
    - `nexti` is the next instruction
    - `step` steps into a function call.
    - `continue` to continue standard execution until the next breakpoint
7. Print variables with `print` or `p`
8. Set variables with `set var=val`
    - reading this line off the gdbtutorial site, I think you can't have spaces?

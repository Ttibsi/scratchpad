import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0,0,"hello world!", curses.A_REVERSE)
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)

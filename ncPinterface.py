# ncPirate rewritten curses interface
# Opens magnet links in default torrent client
# Linux edition.
import ncPirate, curses, traceback, sys

class PirateList:
    def __init__(self, target = None):
        if target != None:
            self.results = ncPirate.pSearch(target)
        else:
            self.results = []
        self.size = len(self.results)
        self.pos = 0
        self.display_range = 0
        self.height, self.width = screen.getmaxyx()

    # Opens target magnet link in default application.
    def open_t(self, index):
        ncPirate.open_magnet(self.results[index][2])

    # Creates search Box, loads ncPirate search script.
    def new_search(self):
        curses.echo()
        curses.curs_set(1)
        search_window = curses.newwin( 5, 40, self.height // 2 - 5, self.width // 3 )
        search_window.box()
        search_window.addstr( 1 , 2, "Enter Search Query: (35 char max)" )
        search_window.refresh()

        target = search_window.getstr(3, 2, 35)
        self.results = ncPirate.pSearch(target)
        self.size = len(self.results)
        
        curses.curs_set(0)
        curses.noecho()
        del search_window
        screen.clear()
        self.draw_topbar()

    # Draws our results object.
    def draw(self):
        screen.addstr( 3, 2, "Torrent Name:", curses.A_BOLD )
        screen.addstr( 3, self.width - 20, "SEEDS", curses.A_BOLD)
        self.display_range = self.height - 6
        if self.size < self.display_range:
            self.display_range = self.size

        for i in range(self.display_range):
            if i == self.pos:
                text_mod = curses.A_STANDOUT
            else:
                text_mod = curses.A_NORMAL
            screen.addstr(5 + i, 2, "{0}. {1}".format(i + 1, self.results[i][1]), text_mod)
            screen.addstr(5 + i, self.width - 20, "{0}".format(self.results[i][0]))
        screen.refresh()

    def draw_topbar(self):
        screen.hline(2, 1, curses.ACS_HLINE, self.width - 3 )
        offset = 2
        new_option = "New Search"
        quit_option = "Quit"
        
        screen.box()
        screen.addstr(1, offset, new_option[0], curses.A_BOLD | curses.A_UNDERLINE)
        screen.addstr(1, offset + 1, new_option[1:], curses.A_NORMAL)
    
        offset += len(new_option) + 5
    
        screen.addstr(1, offset, quit_option[0], curses.A_BOLD | curses.A_UNDERLINE)
        screen.addstr(1, offset + 1, quit_option[1:], curses.A_NORMAL )
        
        screen.addstr(1, 30, "ncPirate v0.1", curses.A_STANDOUT)
        screen.refresh()

    def resize_screen(self):
        y, x = stdscr.getmaxyx()
        screen.clear()
        stdscr.clear()
        curses.resizeterm(y, x)
        self.height, self.width = screen.getmaxyx()
        stdscr.refresh()
        self.draw_topbar()

    def handle_input(self):
        c = stdscr.getch()
        if curses.is_term_resized(*stdscr.getmaxyx()) == True:
            self.resize_screen()
        if c == 258: # Down Arrow
            if self.pos < self.display_range - 1:
                self.pos += 1
            else:
                self.pos = 0
        elif c == 259: #Up arrow
            if self.pos > 0:
                self.pos -= 1
            else:
                self.pos = self.display_range - 1
        elif c == ord('\n'):
            self.open_t( self.pos )
        elif c == ord('n') or c == ord('N'):
            self.new_search()
            self.pos = 0
        elif c == ord('q') or c == ord('Q'):
            sys.exit() 

def main(stdscr):
    global screen
    height, width = stdscr.getmaxyx()
    screen = stdscr.subwin( height - 2, width -1, 0, 0)
    curses.curs_set(0)
    
    if len(sys.argv) > 1:
        pirate = PirateList(sys.argv[1])
        pirate.draw_topbar()
    else:
        pirate = PirateList()
        pirate.draw_topbar()
        pirate.new_search()
    
    while True:
        pirate.draw()
        pirate.handle_input()


if __name__ == '__main__':
   try:
       #initialize Curses engine
       stdscr = curses.initscr()
       curses.noecho()
       curses.cbreak()

       #Keypad mode allows arrow key input
       stdscr.keypad(1)
       main(stdscr) #Enters main loop
       # Clean up after loop
       stdscr.keypad(0)
       curses.echo()
       curses.nocbreak()
       curses.endwin()
   except:
       #Error handling, restores terminal to normal.
       stdscr.keypad(0)
       curses.echo()
       curses.nocbreak()
       curses.endwin()
       traceback.print_exc()


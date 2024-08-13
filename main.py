###
###
### Entry point, orchestrates GUI and simulation
###
###

import tkinter as tk
from gui.gui import GUI



def main():
    root= tk.Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
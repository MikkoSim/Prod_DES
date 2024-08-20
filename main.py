
import tkinter as tk
from gui.gui import GUI



def main():
    root= tk.Tk()
    #root.geometry("500x600")
    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
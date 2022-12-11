from View import View
from Controller import Controller
from Model import Model
import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        model = Model()
        view = View(self)
        controller = Controller(model, view)
        view.set_controller(controller)

    def main(self):
        self.mainloop()

if __name__ == '__main__':
    app = Application()
    app.main()

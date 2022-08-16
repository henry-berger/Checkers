from GUI import GUI

if __name__ == "__main__":
    app = GUI.start_QApplication()
    p = GUI.GUI()
    p.show()
    app.exec()
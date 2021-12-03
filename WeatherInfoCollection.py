from main import main

if __name__ == '__main__':
    main()

# WeatherInfoCollection.py --> main.py
# main.py  -->  1) databaseCollection()
#                   a) database.py (create the database)
#               2) win = Window()
#                   a) views.py  --> class Window(QMainWindow):
#               3) win.show()  --> display the application
#               4) win.exec()  --> executes the application and waits for the user to do something

# views.py  --> contains the data that allows to user to interact with the UI

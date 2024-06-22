import sys
import pymysql
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
import windo
#mysql -u root -p



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 打开数据库连接
    try:
        db = pymysql.connect(host='localhost', user='root', passwd='159951', port=3306, autocommit=False)
    except:
        print('something wrong!')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        cursor.execute("USE lab2")
    except Exception as e:
        print(f"ERROR:{e}")

    login_window = windo.LoginWindow(db, cursor)
    login_window.show()
    windows = windo.Main_Window(db, cursor)
    windows.show()
    
    sys.exit(app.exec())
    cursor.close()
    db.close()




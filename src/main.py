import sys
import pymysql
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QWidget
import windows
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


    windows = windows.Main_Window(db, cursor)
    windows.show()
    sys.exit(app.exec())
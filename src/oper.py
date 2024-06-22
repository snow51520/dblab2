def add_class(db, cursor, ID, name, point):
    try:
        cursor.execute("INSERT INTO Classes (ClassID, Name, Point) VALUES (%s, %s, %s)", (ID, name, point)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    

# 对课程的属性进行修改
def change_class(db, cursor, ID, num, newinf):
    if (num == 1):
        ope="UPDATE Classes SET Name = %s WHERE ClassID = %s"
    if (num == 2):
        ope="UPDATE Classes SET Point = %s WHERE ClassID = %s"
    try:
        cursor.execute(ope, (newinf, ID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return    

# 删除课程
def delete_class(db, cursor, ID):
    try:
        cursor.execute("DELETE FROM Classes WHERE ClassID = %s", (ID, )) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 修改课程号
def changeid_class(db, cursor, oldID, newID):
    try:
        cursor.execute("CALL updateClassID(%s, %s)", (oldID, newID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return


# 添加惩罚
def add_punishment(db, cursor, name):
    try:
        cursor.execute("INSERT INTO Punishments (PunishName) VALUES (%s)", (name, )) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    

# 删除惩罚
def delete_punishment(db, cursor, name):
    try:
        cursor.execute("DELETE FROM Punishments WHERE PunishName = %s", (name, )) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 创建获惩时间
def add_punishtime(db, cursor, sID, name, date):
    try:
        cursor.execute("INSERT INTO Punishtime (StudentID, PunishName, Date) VALUES (%s, %s, %s)", (sID, name, date)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 修改获惩时间
def change_punishtime(db, cursor, sID, name, newinf):
    try:
        cursor.execute("UPDATE Punishtime SET Date = %s WHERE StudentID = %s AND PunishName = %s", (newinf, sID, name)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return    

# 删除获惩时间
def delete_punishtime(db, cursor, sID, name):
    try:
        cursor.execute("DELETE FROM Punishtime WHERE StudentID = %s AND PunishName = %s", (sID, name)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
# 添加奖项
def add_prize(db, cursor, name, grade):
    try:
        cursor.execute("INSERT INTO Prizes (PrizeName, Grade) VALUES (%s, %s)", (name, grade)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    

# 删除奖项
def delete_prize(db, cursor, name):
    try:
        cursor.execute("DELETE FROM Prizes WHERE PrizeName = %s", (name, )) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 创建获奖时间
def add_prizetime(db, cursor, sID, name, date):
    try:
        cursor.execute("INSERT INTO Prizetime (StudentID, PrizeName, Date) VALUES (%s, %s, %s)", (sID, name, date)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 修改获奖时间
def change_prizetime(db, cursor, sID, name, newinf):
    try:
        cursor.execute("UPDATE Prizetime SET Date = %s WHERE StudentID = %s AND PrizeName = %s", (newinf, sID, name)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return    

# 删除获奖时间
def delete_prizetime(db, cursor, sID, name):
    try:
        cursor.execute("DELETE FROM Prizetime WHERE StudentID = %s AND PrizeName = %s", (sID, name)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
# 查询某个学生的基本信息
def select_student_baseinfo(db, cursor, ID):
    try:
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (ID, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询某个学生获得的奖项
def select_student_prizes(db, cursor, ID):
    try:
        cursor.execute("SELECT * FROM Prizetime WHERE StudentID = %s", (ID, )) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询某个学生获得的惩罚
def select_student_punish(db, cursor, ID):
    try:
        cursor.execute("SELECT * FROM Punishtime WHERE StudentID = %s", (ID, )) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询某个学生的全部成绩
def select_student_score(db, cursor, ID):
    try:
        cursor.execute("SELECT * FROM Scores WHERE StudentID = %s", (ID, )) 
        Scores = cursor.fetchall()
        return Scores
    except Exception as e:
        print(f"ERROR:{e}")
        return
        
# 查询某个学生在某门课上的成绩
def select_student_class_score(db, cursor, sID, cID):
    try:
        cursor.execute("SELECT * FROM Scores WHERE StudentID = %s AND ClassID = %s", (sID, cID)) 
        Score = cursor.fetchone()
        return Score
    except Exception as e:
        print(f"ERROR:{e}")
        return

# 查询某个学生某个奖项
def select_student_prize_one(db, cursor, ID, name):
    try:
        cursor.execute("SELECT * FROM Prizetime WHERE StudentID = %s AND PrizeName = %s", (ID, name)) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询某个学生某个惩罚
def select_student_punish_one(db, cursor, ID, name):
    try:
        cursor.execute("SELECT * FROM Punishtime WHERE StudentID = %s AND PunishName = %s", (ID, name)) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return

# 查询学生列表
def select_students_all(db, cursor):
    try:
        cursor.execute("SELECT * FROM Students") 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询课程列表
def select_classes_all(db, cursor):
    try:
        cursor.execute("SELECT * FROM Classes") 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return

# 查询奖项列表
def select_prize_all(db, cursor):
    try:
        cursor.execute("SELECT * FROM Prizes") 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 查询惩罚列表
def select_punish_all(db, cursor):
    try:
        cursor.execute("SELECT * FROM Punishments") 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 按名字查询学生
def select_students_name(db, cursor, name):
    try:
        cursor.execute("SELECT * FROM Students WHERE Name = %s", (name, )) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 按课程号查询课程
def select_class_ID(db, cursor, ID):
    try:
        cursor.execute("SELECT * FROM Classes WHERE ClassID = %s", (ID, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 按名字查询奖项
def select_prize_name(db, cursor, name):
    try:
        cursor.execute("SELECT * FROM Prizes WHERE PrizeName = %s", (name, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return
    
# 按名字查询惩罚
def select_punish_name(db, cursor, name):
    try:
        cursor.execute("SELECT * FROM Punishments WHERE PunishName = %s", (name, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"ERROR:{e}")
        return

# 添加学生
def add_student(db, cursor, ID, name, Age, major, image):
    try:
        cursor.execute("INSERT INTO Students (StudentID, Name, Age, Major, Photo) VALUES (%s, %s, %s, %s, %s)", (ID, name, Age, major, image)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    

# 对学生的属性进行修改
def change_student(db, cursor, ID, num, newinf):
    if (num == 1):
        ope = "UPDATE Students SET Name = %s WHERE StudentID = %s"
    if (num == 2):
        ope = "UPDATE Students SET Age = %s WHERE StudentID = %s"
    if (num == 3):
        ope = "UPDATE Students SET Major = %s WHERE StudentID = %s"
    if (num == 4):
        ope = "UPDATE Students SET Photo = %s WHERE StudentID = %s"
    try:
        cursor.execute(ope, (newinf, ID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return    

# 删除学生
def delete_student(db, cursor, ID):
    try:
        cursor.execute("DELETE FROM Students WHERE StudentID = %s", (ID, )) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 创建成绩
def add_score(db, cursor, sID, cID, Score):
    try:
        cursor.execute("INSERT INTO Scores (StudentID, ClassID, Score) VALUES (%s, %s, %s)", (sID, cID, Score)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 修改成绩
def change_score(db, cursor, sID, cID, newinf):
    try:
        cursor.execute("UPDATE Scores SET Score = %s WHERE StudentID = %s AND ClassID = %s", (newinf, sID, cID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return    

# 删除成绩
def delete_score(db, cursor, sID, cID):
    try:
        cursor.execute("DELETE FROM Scores WHERE StudentID = %s AND ClassID = %s", (sID, cID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 修改学号
def changeid_student(db, cursor, oldID, newID):
    try:
        cursor.execute("CALL updateStudentID(%s, %s)", (oldID, newID)) 
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

# 查询已获得总学分
def get_total_points(db, cursor, ID):
    try:
        cursor.execute("SELECT GetTotalPoints(%s) as TotalCredits", (ID, )) 
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"ERROR:{e}")
        return
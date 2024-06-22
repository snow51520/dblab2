import pymysql

# 初始化表格
def init(db, cursor):

    # 删除表
    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Scores
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Punishtime
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Prizetime
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Prizes
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Punishments
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
    try:
        cursor.execute( """
        DROP TABLE IF EXISTS Classes
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return


    try:
        cursor.execute("""
        DROP TABLE IF EXISTS Students 
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
    # 创建表
    try:
        cursor.execute("""
        CREATE TABLE Students (
        StudentID CHAR(12) PRIMARY KEY,
        Name VARCHAR(64) NOT NULL,
        Age INT NOT NULL,
        Major VARCHAR(64) NOT NULL,
        Photo LONGBLOB
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Classes (
        ClassID CHAR(12) PRIMARY KEY,
        Name VARCHAR(64) NOT NULL,
        Point INT NOT NULL
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Scores (
        StudentID CHAR(12) NOT NULL,
        ClassID CHAR(12) NOT NULL,
        Score INT,
        PRIMARY KEY (StudentID, ClassID),
        CONSTRAINT Scores_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
        CONSTRAINT Scores_cforeign FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Punishments (
        PunishName VARCHAR(64) NOT NULL,
        PRIMARY KEY (PunishName)
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Punishtime (
        StudentID CHAR(12) NOT NULL,
        PunishName VARCHAR(64) NOT NULL,
        Date DATE,
        PRIMARY KEY (PunishName),
        CONSTRAINT Punishtime_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
        CONSTRAINT Punishtime_pforeign FOREIGN KEY (PunishName) REFERENCES Punishments(PunishName)
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Prizes (
        PrizeName VARCHAR(64) NOT NULL,
        Grade VARCHAR(64),
        PRIMARY KEY (PrizeName)
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
        CREATE TABLE Prizetime (
        StudentID CHAR(12) NOT NULL,
        PrizeName VARCHAR(64) NOT NULL,
        Date DATE,
        PRIMARY KEY (PrizeName),
        CONSTRAINT Prizetime_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
        CONSTRAINT Prizetime_pforeign FOREIGN KEY (PrizeName) REFERENCES Prizes(PrizeName)
        )
        """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
# 存储过程:修改学号
    try:
        cursor.execute("DROP PROCEDURE IF EXISTS updateStudentID")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    try:
        cursor.execute("""
    CREATE PROCEDURE updateStudentID(IN old_id CHAR(12), IN new_id CHAR(12))
    BEGIN
        ALTER TABLE Scores
        DROP FOREIGN KEY Scores_sforeign;
        
        UPDATE Scores
        SET StudentID = new_id
        WHERE StudentID = old_id;
        
        ALTER TABLE Punishtime
        DROP FOREIGN KEY Punishtime_sforeign;
        
        UPDATE Punishtime
        SET StudentID = new_id
        WHERE StudentID = old_id;

        ALTER TABLE Prizetime
        DROP FOREIGN KEY Prizetime_sforeign;
        
        UPDATE Prizetime
        SET StudentID = new_id
        WHERE StudentID = old_id;

        UPDATE Students
        SET StudentID = new_id
        WHERE StudentID = old_id;
        
        ALTER TABLE Scores
        ADD CONSTRAINT Scores_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);

        ALTER TABLE Punishtime
        ADD CONSTRAINT Punishtime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);

        ALTER TABLE Prizetime
        ADD CONSTRAINT Prizetime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        cursor.execute("""
        ALTER TABLE Scores
        ADD CONSTRAINT Scores_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);
        """)
        cursor.execute("""
        ALTER TABLE Punishtime
        ADD CONSTRAINT Punishtime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);
        """)
        cursor.execute("""
        ALTER TABLE Prizetime
        ADD CONSTRAINT Prizetime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);
        """)
        db.rollback()
        return
# 存储过程:修改课程号

    try:
        cursor.execute("DROP PROCEDURE IF EXISTS updateClassID")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
    CREATE PROCEDURE updateClassID(IN old_id CHAR(12), IN new_id CHAR(12))
    BEGIN
        ALTER TABLE Scores
        DROP FOREIGN KEY Scores_cforeign;
        
        UPDATE Scores
        SET ClassID = new_id
        WHERE ClassID = old_id;

        UPDATE Classes
        SET ClassID = new_id
        WHERE ClassID = old_id;
        
        ALTER TABLE Scores
        ADD CONSTRAINT Scores_cforeign FOREIGN KEY (ClassID) REFERENCES Classes (ClassID);
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        cursor.execute("""
        ALTER TABLE Scores
        ADD CONSTRAINT Scores_cforeign FOREIGN KEY (ClassID) REFERENCES Classes (ClassID);
        """)
        return
# 存储函数:查询已获得的学生总学分

    try:
        cursor.execute("DROP Function IF EXISTS GetTotalPoints")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
    CREATE FUNCTION GetTotalPoints (student_id CHAR(12)) RETURNS INT
    DETERMINISTIC
    BEGIN
        DECLARE total_points INT;
        SELECT SUM(Classes.Point) INTO total_points
        FROM Classes
        WHERE ClassID IN (SELECT ClassID FROM Scores WHERE Scores.StudentID = student_id);
        RETURN total_points;
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
# 触发器:删除学生，课程，惩罚，奖项时自动删除相关成绩，日期

    try:
        cursor.execute("DROP TRIGGER IF EXISTS trg_delete_student")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
    try:
        cursor.execute("""
    CREATE TRIGGER trg_delete_student
    BEFORE DELETE ON Students
    FOR EACH ROW
    BEGIN
        SELECT COUNT(*) INTO @count FROM Scores WHERE StudentID = OLD.StudentID;
        
        IF @count > 0 THEN
            DELETE FROM Scores WHERE StudentID = OLD.StudentID;
        END IF;
                
        SELECT COUNT(*) INTO @count FROM Punishtime WHERE StudentID = OLD.StudentID;
        
        IF @count > 0 THEN
            DELETE FROM Punishtime WHERE StudentID = OLD.StudentID;
        END IF;
                
        SELECT COUNT(*) INTO @count FROM Prizetime WHERE StudentID = OLD.StudentID;
        
        IF @count > 0 THEN
            DELETE FROM Prizetime WHERE StudentID = OLD.StudentID;
        END IF;
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("DROP TRIGGER IF EXISTS trg_delete_class")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
    
    try:
        cursor.execute("""
    CREATE TRIGGER trg_delete_class
    BEFORE DELETE ON Classes
    FOR EACH ROW
    BEGIN
        SELECT COUNT(*) INTO @count FROM Scores WHERE ClassID = OLD.ClassID;
        
        IF @count > 0 THEN
            DELETE FROM Scores WHERE ClassID = OLD.ClassID;
        END IF;
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("DROP TRIGGER IF EXISTS trg_delete_punish")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
    CREATE TRIGGER trg_delete_punish
    BEFORE DELETE ON Punishments
    FOR EACH ROW
    BEGIN
        SELECT COUNT(*) INTO @count FROM Punishtime WHERE PunishName = OLD.PunishName;
        
        IF @count > 0 THEN
            DELETE FROM Punishtime WHERE PunishName = OLD.PunishName;
        END IF;  
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("DROP TRIGGER IF EXISTS trg_delete_prize")
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return

    try:
        cursor.execute("""
    CREATE TRIGGER trg_delete_prize
    BEFORE DELETE ON Prizes
    FOR EACH ROW
    BEGIN               
        SELECT COUNT(*) INTO @count FROM Prizetime WHERE PrizeName = OLD.PrizeName;
        
        IF @count > 0 THEN
            DELETE FROM Prizetime WHERE PrizeName = OLD.PrizeName;
        END IF;
    END
    """)
        db.commit()
    except Exception as e:
        print(f"ERROR:{e}")
        db.rollback()
        return
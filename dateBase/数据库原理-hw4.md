1.Student（Sno,Sname,Ssex,Sage,Sdept)

   Course（Cno,Cname,Cpno,Ccredit,Teacher）

   SC（Sno,Cno,Grade）

   1）找出平均成绩最高的学生的学号；

```mysql
SELECT Sno FROM SC 
GROUP BY Sno
HAVING AVG(Grade) >=ALL
	(SELECT AVG(Grade) FROM SC
     GROUP BY Sno
    );
```



   2）将没有选课的学生从学生表中删除；  

```mysql
DELETE FROM Student
WHERE Sno NOT IN
	(SELECT Sno FROM SC
     GROUP BY Sno
	);
```



   3）查询出选修至少两门课程的学生学号；

```mysql
SELECT Sno FROM SC
GROUP BY Sno
HAVING COUNT(*) >= 2;
```



   4）查询选择了刘老师所有课程的学生学号；

```mysql
SELECT Sno FROM SC X
GROUP BY Sno
HAVING NOT EXISTS
	(SELECT * FROM Course
     WHERE Teacher LIKE '刘%'
     		AND NOT EXISTS
     		(SELECT * FROM SC Y
             WHERE Y.Sno = X.Sno AND
             		Y.Cno = Course.Cno
            )
    );
```



   5) 按平均成绩的降序给出所有课程都及格的学生及其平均成绩。

```MYSQL
SELECT Sno,AVG(Grade) FROM SC X
GROUP BY Sno
HAVING Sno NOT IN
	(SELECT DISTINCT Sno FROM SC Y
     WHERE Y.Grade < 60
    )
ORDER BY AVG(Grade) DESC;
```



   6) 定义一个平均成绩大于85分的学生成绩视图；

```MYSQL
CREATE VIEW S_G(Gavg)
AS 
SELECT AVG(Grade) FROM SC
GROUP BY Sno
HAVING AVG(Grade) >=85;
```



   7) 表S中男同学的每一年龄组（超过50人）有多少人？要求查询结果按人数升序排列，人数相同按年龄降序排列。

```MYSQL
SELECT Sage,COUNT(*) FROM Student
GROUP BY Sage
HAVING COUNT(*) > 50
ORDER BY COUNT(*) ASC,Sage DESC;
```


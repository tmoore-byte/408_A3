CREATE TABLE Students(StudentID int,
    FirstName varchar(60) ,
    LastName varchar(60),
    GPA smallint,
    Major varchar(60),
    FacultyAdvisor varchar(60),
    Address varchar(100),
    City varchar(60),
    State varchar(60),
    ZipCode varchar(60),
    MobileNumber varchar(60),
    isDeleted smallint,
    PRIMARY KEY (StudentID));


insert into Students
values(1, 't','m' , '5', 'm', 'f', 'a', 'c', 'c', 'z', 11111111,5);
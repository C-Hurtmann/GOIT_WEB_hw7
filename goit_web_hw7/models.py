from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


#engine = create_engine("postgresql+psycopg2://czagorodnyi:Szk6zynbGNWtPT%40@localhost:5432/postgres")
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

Base = declarative_base()

grades = Table("grades",
               Base.metadata,
               Column("id", Integer, primary_key=True),
               Column("grade", Integer, nullable=False),
               Column("date", Date, nullable=False),
               Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE", onupdate="CASCADE")),
               Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE", onupdate="CASCADE")))


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    title = Column(String(10), nullable=False, unique=True)
    students = relationship("Student", secondary="grades", backref="groups")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    birthday = Column(Date)
    phone = Column(String(12))
    email = Column(String(20))
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="NO ACTION", onupdate="CASCADE"))


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False, unique=True)
    subjects = relationship("Subject", secondary="grades", backref="teachers")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    

#class Grade(Base):
#    __tablename__ = "grades"
#    id = Column(Integer, primary_key=True)
#    grade = Column(Integer, nullable=False)
#    date = Column(Date, nullable=False)
#    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
#    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))

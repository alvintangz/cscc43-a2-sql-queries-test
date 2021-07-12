import peewee

db = peewee.PostgresqlDatabase(
    "postgres",
    user="postgres",
    password="Password@123",
    host="localhost",
    port="5432",
    autorollback=True
)


class BaseModel(peewee.Model):
    class Meta:
        database = db
        schema = 'a2'


class Department(BaseModel):
    """
    The department table contains the departments at the university
    """
    dcode = peewee.FixedCharField(primary_key=True, max_length=3)
    dname = peewee.CharField(null=False, max_length=20)

    class Meta:
        db_table = 'department'


class Student(BaseModel):
    """
    The student table contains information about the students at the
    university.
    - sid is the student number.
    - sex is either 'M' or 'F'
    - yearofstudy is number of years the student has been studying at the
    university.
    """
    sid = peewee.IntegerField(primary_key=True)
    slastname = peewee.FixedCharField(null=False, max_length=20)
    sfirstname = peewee.FixedCharField(null=False, max_length=20)
    sex = peewee.FixedCharField(null=False, max_length=1)
    age = peewee.IntegerField(null=False)
    dcode = peewee.ForeignKeyField(
        Department,
        on_delete="RESTRICT",
        column_name="dcode"
    )
    yearofstudy = peewee.IntegerField(null=False)

    class Meta:
        db_name = 'student'


class Instructor(BaseModel):
    """
    The instructor table contains information about the instructors at the
    university.
    - iid is the instructor employee id.
    - idegree is the highest post-graduate degree held by the instructor
    (e.g., PhD, MSC)
    - an instructor can only be associated with one department.
    """
    iid = peewee.IntegerField(primary_key=True)
    ilastname = peewee.FixedCharField(null=False, max_length=20)
    ifirstname = peewee.FixedCharField(null=False, max_length=20)
    idegree = peewee.FixedCharField(null=False, max_length=5)
    dcode = peewee.FixedCharField(max_length=3, null=False)

    class Meta:
        db_name = 'instructor'
        constraints = [
            peewee.SQL('FOREIGN KEY (dcode) REFERENCES a2.department(dcode) ON DELETE RESTRICT)'),
        ]


class Course(BaseModel):
    """
    The course table contains the courses offered at the university.
    """
    cid = peewee.IntegerField()
    dcode = peewee.ForeignKeyField(
        Department,
        on_delete="RESTRICT",
        to_field="dcode",
        column_name="dcode"
    )
    cname = peewee.FixedCharField(null=False, max_length=20)

    class Meta:
        db_name = 'course'
        primary_key = peewee.CompositeKey('cid', 'dcode')


class CourseSection(BaseModel):
    """
    The courseSection table contains the sections that are offered
    for courses at the university for each semester of each year.
    Semester values are '9' fall, '1' winter, and '5' summer.
    """
    csid = peewee.IntegerField(primary_key=True)
    # FOREIGN KEYS - https://github.com/coleifer/peewee/issues/270
    cid = peewee.IntegerField(null=False)
    dcode = peewee.FixedCharField(max_length=3, null=False)
    year = peewee.IntegerField(null=False)
    semester = peewee.IntegerField(null=False)
    section = peewee.FixedCharField(max_length=5, null=False)
    iid = peewee.ForeignKeyField(Instructor, to_field="iid", column_name="iid")

    class Meta:
        db_name = 'courseSection'
        constraints = [
            peewee.SQL('UNIQUE(cid, dcode, year, semester, section)'),
            peewee.SQL('FOREIGN KEY(cid, dcode) REFERENCES a2.course(cid, dcode)')
        ]


class StudentCourse(BaseModel):
    """
    The studentCourse table contains the courses a student has enrolled in,
    and their grade. the grade is maintained as an integer value from 0 to 100.
    """
    sid = peewee.ForeignKeyField(Student, to_field="sid", column_name="sid")
    csid = peewee.ForeignKeyField(
        CourseSection,
        to_field="csid",
        column_name="csid"
    )
    grade = peewee.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        default=0.00
    )

    class Meta:
        db_name = 'studentCourse'
        primary_key = peewee.CompositeKey('sid', 'csid')


class Prerequisites(BaseModel):
    """
    The prerequisites table contains the prerequisites for each course.
    There may be more than one per course.  The course for which the
    prerequisite applies is identified by (cid, dcode). The prerequisite for
    that course is identified by (pcid, pcode).
    """
    # FOREIGN KEYS - https://github.com/coleifer/peewee/issues/270
    cid = peewee.IntegerField(null=False)
    dcode = peewee.FixedCharField(max_length=3, null=False)
    pcid = peewee.IntegerField(null=False)
    pdcode = peewee.FixedCharField(max_length=3, null=False)

    class Meta:
        db_name = 'prerequisites'
        primary_key = peewee.CompositeKey('cid', 'dcode', 'pcid', 'pdcode')
        constraints = [
            peewee.SQL('FOREIGN KEY (cid, dcode) REFERENCES a2.course(cid, dcode)'),
            peewee.SQL('FOREIGN KEY (pcid, pdcode) REFERENCES a2.course(cid, dcode)')
        ]

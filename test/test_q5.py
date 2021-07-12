import unittest

from test.utils.mixins import *
from test.utils.enums import Semester
from test.utils.generic_data import DEPARTMENTS, INSTRUCTORS, COURSES, STUDENTS


# Largest year/term value is 2021 Fall
COURSE_SECTIONS = [
    {
        "csid": 1,
        "cid": 1,
        "dcode": "CSC",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 2,
        "cid": 2,
        "dcode": "CSC",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 3,
        "cid": 1,
        "dcode": "CSC",
        "year": 2021,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 4,
        "cid": 1,
        "dcode": "CSC",
        "year": 2021,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 5,
        "cid": 3,
        "dcode": "AST",
        "year": 2021,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 3
    },
    {
        "csid": 6,
        "cid": 4,
        "dcode": "MGM",
        "year": 2015,
        "semester": Semester.SUMMER.value,
        "section": "LEC01",
        "iid": 4
    },
]


class QueryFiveTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query5"
    query = """
    --Query 5
    """

    def setUp(self):
        """Connect to the database."""
        db.connect()
        self._create_instances(Department, DEPARTMENTS)
        self._create_instances(Course, COURSES)
        self._create_instances(Instructor, INSTRUCTORS)
        self._create_instances(Student, STUDENTS)
        self._create_instances(CourseSection, COURSE_SECTIONS)

    def tearDown(self):
        """Disconnect to the database."""
        self._drop_generated_table()
        self._destroy_all_instances()
        db.close()

    def test_columns(self):
        self._execute_query()
        results = self._get_generated_table_columns()
        logging.info(results)

        self.assertEqual(len(results), 5)
        self.assertEqual(results[0], "dept")
        self.assertEqual(results[1], "sid")
        self.assertEqual(results[2], "sfirstname")
        self.assertEqual(results[3], "slastname")
        self.assertEqual(results[4], "avggrade")

    def test_one_student_in_one_dept_taking_one_course(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 4,
                    "csid": 1,
                    "grade": 80,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["avggrade"], 80)
        self.assertEqual(results[0]["dept"], "Business")
        self.assertEqual(results[0]["sid"], 4)
        self.assertEqual(results[0]["sfirstname"], "George")
        self.assertEqual(results[0]["slastname"], "Li")

    def test_one_student_in_one_dept_taking_two_courses(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 4,
                    "csid": 1,
                    "grade": 80,
                },
                {
                    "sid": 4,
                    "csid": 6,
                    "grade": 90,
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["avggrade"], 85)
        self.assertEqual(results[0]["dept"], "Business")
        self.assertEqual(results[0]["sid"], 4)
        self.assertEqual(results[0]["sfirstname"], "George")
        self.assertEqual(results[0]["slastname"], "Li")

    def test_two_students_in_one_dept_taking_three_courses_with_one_course_in_current_semester(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 4,
                    "csid": 2,
                    "grade": 70,
                },
                {
                    "sid": 4,
                    "csid": 6,
                    "grade": 80,
                },
                {
                    "sid": 4,
                    "csid": 3,
                    "grade": 91,
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["avggrade"], 75)
        self.assertEqual(results[0]["dept"], "Business")
        self.assertEqual(results[0]["sid"], 4)
        self.assertEqual(results[0]["sfirstname"], "George")
        self.assertEqual(results[0]["slastname"], "Li")

    def test_one_student_in_one_dept_taking_one_course_and_one_student_in_another_dept_taking_one_course(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 50,
                },
                {
                    "sid": 5,
                    "csid": 1,
                    "grade": 51,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 1,
                    "sfirstname": "Alvin",
                    "slastname": "Tang",
                    "avggrade": 50,
                },
                {
                    "dept": "Astronomy",
                    "sid": 5,
                    "sfirstname": "Kelly",
                    "slastname": "Smith",
                    "avggrade": 51,
                }
            ]
        )

    def test_two_students_in_one_dept_each_taking_one_course_and_one_student_in_another_dept_taking_one_course_all_with_diff_grades(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 50,
                },
                {
                    "sid": 2,
                    "csid": 6,
                    "grade": 60,
                },
                {
                    "sid": 5,
                    "csid": 1,
                    "grade": 51,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 2,
                    "sfirstname": "Sonya",
                    "slastname": "Zhang",
                    "avggrade": 60,
                },
                {
                    "dept": "Astronomy",
                    "sid": 5,
                    "sfirstname": "Kelly",
                    "slastname": "Smith",
                    "avggrade": 51,
                }
            ]
        )

    def test_two_students_in_one_dept_and_one_student_in_another_dept_each_taking_three_courses_with_one_course_in_current_semester(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 50,
                },
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 60,
                },
                {
                    "sid": 1,
                    "csid": 3,
                    "grade": 75,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 60,
                },
                {
                    "sid": 2,
                    "csid": 2,
                    "grade": 70,
                },
                {
                    "sid": 2,
                    "csid": 3,
                    "grade": 75,
                },
                {
                    "sid": 5,
                    "csid": 1,
                    "grade": 51,
                },
                {
                    "sid": 5,
                    "csid": 5,
                    "grade": 52,
                },
                {
                    "sid": 5,
                    "csid": 3,
                    "grade": 70,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 2,
                    "sfirstname": "Sonya",
                    "slastname": "Zhang",
                    "avggrade": 65,
                },
                {
                    "dept": "Astronomy",
                    "sid": 5,
                    "sfirstname": "Kelly",
                    "slastname": "Smith",
                    "avggrade": 51.5,
                }
            ]
        )

    def test_two_students_in_one_dept_and_one_student_in_another_dept_each_taking_one_course_with_same_grades(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 80,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 80,
                },
                {
                    "sid": 5,
                    "csid": 5,
                    "grade": 70,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 1,
                    "sfirstname": "Alvin",
                    "slastname": "Tang",
                    "avggrade": 80,
                },
                {
                    "dept": "Computer Science",
                    "sid": 2,
                    "sfirstname": "Sonya",
                    "slastname": "Zhang",
                    "avggrade": 80,
                },
                {
                    "dept": "Astronomy",
                    "sid": 5,
                    "sfirstname": "Kelly",
                    "slastname": "Smith",
                    "avggrade": 70,
                }
            ]
        )

    def test_two_students_in_one_dept_and_one_student_in_another_dept_each_taking_two_courses_with_same_avg_grades(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 50,
                },
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 100,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 70,
                },
                {
                    "sid": 2,
                    "csid": 2,
                    "grade": 80,
                },
                {
                    "sid": 5,
                    "csid": 1,
                    "grade": 74,
                },
                {
                    "sid": 5,
                    "csid": 5,
                    "grade": 74,
                },
                {
                    "sid": 3,
                    "csid": 1,
                    "grade": 74,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 1,
                    "sfirstname": "Alvin",
                    "slastname": "Tang",
                    "avggrade": 75,
                },
                {
                    "dept": "Computer Science",
                    "sid": 2,
                    "sfirstname": "Sonya",
                    "slastname": "Zhang",
                    "avggrade": 75,
                },
                {
                    "dept": "Astronomy",
                    "sid": 5,
                    "sfirstname": "Kelly",
                    "slastname": "Smith",
                    "avggrade": 74,
                }
            ]
        )

    def test_three_students_in_one_dept_with_two_student_having_same_avg_grade(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 100,
                },
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 80,
                },
                {
                    "sid": 1,
                    "csid": 4,
                    "grade": 90,
                },
                {
                    "sid": 3,
                    "csid": 1,
                    "grade": 90,
                },
                {
                    "sid": 3,
                    "csid": 3,
                    "grade": 50,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 89,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "dept": "Computer Science",
                    "sid": 1,
                    "sfirstname": "Alvin",
                    "slastname": "Tang",
                    "avggrade": 90,
                },
                {
                    "dept": "Computer Science",
                    "sid": 3,
                    "sfirstname": "Balaji",
                    "slastname": "Babu",
                    "avggrade": 90,
                },
            ]
        )

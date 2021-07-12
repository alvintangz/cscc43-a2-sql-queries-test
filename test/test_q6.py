import unittest

from test.utils.mixins import *
from test.utils.enums import Semester
from test.utils.generic_data import DEPARTMENTS, INSTRUCTORS, COURSES, STUDENTS, PREREQUISITES

COURSE_SECTIONS = [
    {
        "csid": 1,
        "cid": 1,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 2,
        "cid": 2,
        "dcode": "CSC",
        "year": 2017,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 3,
        "cid": 2,
        "dcode": "CSC",
        "year": 2017,
        "semester": Semester.WINTER.value,
        "section": "LEC02",
        "iid": 2
    },
    {
        "csid": 4,
        "cid": 6,
        "dcode": "CSC",
        "year": 2018,
        "semester": Semester.SUMMER.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 5,
        "cid": 3,
        "dcode": "AST",
        "year": 2020,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 3
    },
    {
        "csid": 6,
        "cid": 5,
        "dcode": "AST",
        "year": 2021,
        "semester": Semester.SUMMER.value,
        "section": "LEC01",
        "iid": 4
    },
    {
        "csid": 7,
        "cid": 7,
        "dcode": "AST",
        "year": 2021,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 4
    },
    {
        "csid": 8,
        "cid": 6,
        "dcode": "CSC",
        "year": 2018,
        "semester": Semester.SUMMER.value,
        "section": "LEC02",
        "iid": 1
    },
    {
        "csid": 9,
        "cid": 6,
        "dcode": "CSC",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
]


class QuerySixTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query6"
    query = """
    --Query 6
    """

    def setUp(self):
        """Connect to the database."""
        db.connect()
        self._create_instances(Department, DEPARTMENTS)
        self._create_instances(Course, COURSES)
        self._create_instances(Instructor, INSTRUCTORS)
        self._create_instances(Student, STUDENTS)
        self._create_instances(CourseSection, COURSE_SECTIONS)
        self._create_instances(Prerequisites, PREREQUISITES)

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
        self.assertEqual(results[0], "fname")
        self.assertEqual(results[1], "lname")
        self.assertEqual(results[2], "cname")
        self.assertEqual(results[3], "year")
        self.assertEqual(results[4], "semester")

    def test_students_that_take_all_prereqs(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 3, # cid: 2 (Algorithm Design)
                    "grade": 75
                },
                {
                    "sid": 1,
                    "csid": 4, # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 2,
                    "csid": 2, # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4, # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 5, # cid: 3 (Intro to Astronomy)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 6, # cid: 5 (Secondary Astronomy)
                    "grade": 60
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 0)

    def test_one_student_that_does_not_take_prereq_for_a_course(self):
        self._create_instances(
            StudentCourse,
            [
                # {
                #     "sid": 1,
                #     "csid": 3,  # cid: 2 (Algorithm Design)
                #     "grade": 75
                # },
                {
                    "sid": 1,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 2,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 5,  # cid: 3 (Intro to Astronomy)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Alvin",
                    "lname": "Tang",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                }
            ]
        )

    def test_one_student_that_does_not_take_one_of_two_prereqs_for_a_course(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 2,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 5,  # cid: 3 (Intro to Astronomy)
                    "grade": 76
                },
                # {
                #     "sid": 3,
                #     "csid": 6,  # cid: 5 (Secondary Astronomy)
                #     "grade": 60
                # },
                {
                    "sid": 3,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                }
            ]
        )

    def test_one_student_that_does_not_take_all_prereqs_for_a_course(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 2,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 3,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                # {
                #     "sid": 3,
                #     "csid": 6,  # cid: 5 (Secondary Astronomy)
                #     "grade": 60
                # },
                {
                    "sid": 3,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                }
            ]
        )

    def test_one_student_that_does_not_take_at_least_one_prereq_for_two_courses(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 2,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 3,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                {
                    "sid": 3,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                },
                {
                    "sid": 3,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                },
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Secondary Astronomy",
                    "year": 2021,
                    "semester": Semester.SUMMER.value
                }
            ]
        )

    def test_one_student_that_does_not_take_one_prereq_for_two_courses(
                self
        ):
            self._create_instances(
                StudentCourse,
                [
                    # {
                    #     "sid": 3,
                    #     "csid": 2,  # cid: 2 (Algorithm Design)
                    #     "grade": 49
                    # },
                    {
                        "sid": 3,
                        "csid": 4,  # cid: 6 (Algorithm Design 2)
                        "grade": 76
                    },
                    # {
                    #     "sid": 3,
                    #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                    #     "grade": 76
                    # },
                    {
                        "sid": 3,
                        "csid": 6,  # cid: 5 (Secondary Astronomy)
                        "grade": 60
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
                        "fname": "Balaji",
                        "lname": "Babu",
                        "cname": "Algorithm Design 2",
                        "year": 2018,
                        "semester": Semester.SUMMER.value
                    },
                    {
                        "fname": "Balaji",
                        "lname": "Babu",
                        "cname": "Secondary Astronomy",
                        "year": 2021,
                        "semester": Semester.SUMMER.value
                    }
                ]
            )

    def test_two_students_that_each_do_not_take_prereqs_for_two_courses(self):
        self._create_instances(
            StudentCourse,
            [
                # {
                #     "sid": 1,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 1,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 1,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                {
                    "sid": 1,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                },
                # {
                #     "sid": 3,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 3,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 3,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                {
                    "sid": 3,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                },
                {
                    "sid": 1,
                    "csid": 1,  # cid: 1 (Intro to Databases)
                    "grade": 51
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Alvin",
                    "lname": "Tang",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Alvin",
                    "lname": "Tang",
                    "cname": "Secondary Astronomy",
                    "year": 2021,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Secondary Astronomy",
                    "year": 2021,
                    "semester": Semester.SUMMER.value
                }
            ]
        )

    def test_one_student_that_does_take_prereq_for_a_course_and_one_student_that_does_not(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 56
                },
                {
                    "sid": 1,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 3,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 3,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 90
                },
                {
                    "sid": 1,
                    "csid": 1,  # cid: 1 (Intro to Databases)
                    "grade": 51
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
            ]
        )

    def test_three_students_that_each_do_not_take_at_least_one_prereq_for_at_least_one_course(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 2,
                    "csid": 2,  # cid: 2 (Algorithm Design)
                    "grade": 49
                },
                {
                    "sid": 2,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 1,
                    "csid": 5,  # cid: 3 (Intro to Astronomy)
                    "grade": 76
                },
                # {
                #     "sid": 1,
                #     "csid": 6,  # cid: 5 (Secondary Astronomy)
                #     "grade": 60
                # },
                {
                    "sid": 1,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                },
                # {
                #     "sid": 2,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                # {
                #     "sid": 2,
                #     "csid": 6,  # cid: 5 (Secondary Astronomy)
                #     "grade": 60
                # },
                {
                    "sid": 2,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                },
                # {
                #     "sid": 3,
                #     "csid": 5,  # cid: 3 (Intro to Astronomy)
                #     "grade": 76
                # },
                {
                    "sid": 3,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                },
                {
                    "sid": 3,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
                },
                {
                    "sid": 4,
                    "csid": 5,  # cid: 3 (Intro to Astronomy)
                    "grade": 76
                },
                {
                    "sid": 4,
                    "csid": 6,  # cid: 5 (Secondary Astronomy)
                    "grade": 60
                },
                {
                    "sid": 4,
                    "csid": 7,  # cid: 7 (Third Astronomy)
                    "grade": 80
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
                    "fname": "Alvin",
                    "lname": "Tang",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                },
                {
                    "fname": "Sonya",
                    "lname": "Zhang",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                },
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Third Astronomy",
                    "year": 2021,
                    "semester": Semester.FALL.value
                },
                {
                    "fname": "Balaji",
                    "lname": "Babu",
                    "cname": "Secondary Astronomy",
                    "year": 2021,
                    "semester": Semester.SUMMER.value
                }
            ]
        )

    def test_two_students_that_each_do_not_take_prereqs_for_one_course_in_diff_sections(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                # {
                #     "sid": 1,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 1,
                    "csid": 4,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 2,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 40
                # },
                {
                    "sid": 2,
                    "csid": 8,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 3,
                    "csid": 3,  # cid: 2 (Algorithm Design)
                    "grade": 40
                },
                {
                    "sid": 3,
                    "csid": 8,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
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
                    "fname": "Alvin",
                    "lname": "Tang",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Sonya",
                    "lname": "Zhang",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
            ]
        )

    def test_one_student_that_each_do_not_take_prereqs_for_one_course_in_two_diff_years_and_semesters(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                # {
                #     "sid": 2,
                #     "csid": 3,  # cid: 2 (Algorithm Design)
                #     "grade": 40
                # },
                {
                    "sid": 2,
                    "csid": 8,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 2,
                    "csid": 9,  # cid: 6 (Algorithm Design 2)
                    "grade": 35
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
                    "fname": "Sonya",
                    "lname": "Zhang",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Sonya",
                    "lname": "Zhang",
                    "cname": "Algorithm Design 2",
                    "year": 2019,
                    "semester": Semester.FALL.value
                },
            ]
        )

    def test_two_students_with_same_name_do_not_take_prereqs_for_one_course(
            self
    ):
        self._create_instances(
            StudentCourse,
            [
                # {
                #     "sid": 5,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 5,
                    "csid": 8,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                # {
                #     "sid": 6,
                #     "csid": 2,  # cid: 2 (Algorithm Design)
                #     "grade": 49
                # },
                {
                    "sid": 6,
                    "csid": 8,  # cid: 6 (Algorithm Design 2)
                    "grade": 76
                },
                {
                    "sid": 1,
                    "csid": 1,  # cid: 1 (Intro to Databases)
                    "grade": 51
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self._assert_records_equal(
            results,
            expected=[
                {
                    "fname": "Kelly",
                    "lname": "Smith",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
                {
                    "fname": "Kelly",
                    "lname": "Smith",
                    "cname": "Algorithm Design 2",
                    "year": 2018,
                    "semester": Semester.SUMMER.value
                },
            ]
        )

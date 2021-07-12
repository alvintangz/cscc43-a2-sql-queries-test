import unittest
from test.utils.mixins import *
from test.utils.generic_data import DEPARTMENTS, STUDENTS, INSTRUCTORS, COURSES
from test.utils.enums import Semester


COURSE_SECTIONS = [
    {
        "csid": 1,
        "cid": 1,
        "dcode": "CSC",
        "year": 2015,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 2,
        "cid": 2,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 3,
        "cid": 1,
        "dcode": "CSC",
        "year": 2017,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 4,
        "cid": 2,
        "dcode": "CSC",
        "year": 2020,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 2
    },
    {
        "csid": 5,
        "cid": 1,
        "dcode": "CSC",
        "year": 2020,
        "semester": Semester.FALL.value,
        "section": "LEC02",
        "iid": 1
    },
    {
        "csid": 6,
        "cid": 2,
        "dcode": "CSC",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 7,
        "cid": 2,
        "dcode": "CSC",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC02",
        "iid": 1
    },
    {
        "csid": 8,
        "cid": 3,
        "dcode": "AST",
        "year": 2019,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 3
    }
]


class QueryThreeTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query3"
    query = """
    --Query 3
    """

    def setUp(self):
        """Connect to the database."""
        db.connect()
        self._create_instances(Department, DEPARTMENTS)
        self._create_instances(Course, COURSES)
        self._create_instances(Student, STUDENTS)
        self._create_instances(Instructor, INSTRUCTORS)
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

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "year")
        self.assertEqual(results[1], "enrollment")

    def test_no_cs_enrollment_between_2016_and_2020(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 80
                },
                {
                    "sid": 4,
                    "csid": 8,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 0)

    def test_one_cs_enrollment_in_2016(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 2,
                    "grade": 80
                },
                {
                    "sid": 4,
                    "csid": 8,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2016)
        self.assertEqual(results[0]["enrollment"], 1)

    def test_multiple_cs_enrollments_in_2016(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 2,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 2,
                    "grade": 55,
                },
                {
                    "sid": 4,
                    "csid": 8,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2016)
        self.assertEqual(results[0]["enrollment"], 3)

    def test_multiple_cs_enrollments_in_2020(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 4,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 4,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 4,
                    "grade": 55,
                },
                {
                    "sid": 4,
                    "csid": 8,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2020)
        self.assertEqual(results[0]["enrollment"], 3)

    def test_multiple_cs_enrollments_in_2017(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 3,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 3,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 2,
                    "grade": 55,
                },
                {
                    "sid": 4,
                    "csid": 4,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2017)
        self.assertEqual(results[0]["enrollment"], 2)

    def test_multiple_cs_enrollments_in_2020_diff_sections(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 4,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 5,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 2,
                    "grade": 55,
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2020)
        self.assertEqual(results[0]["enrollment"], 2)

    def test_multiple_cs_enrollments_in_2019_diff_sections(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 4,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 5,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 6,
                    "grade": 55,
                },
                {
                    "sid": 4,
                    "csid": 7,
                    "grade": 55,
                },
                {
                    "sid": 1,
                    "csid": 7,
                    "grade": 55,
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2019)
        self.assertEqual(results[0]["enrollment"], 3)

    def test_two_cs_enrollments_in_2016_and_two_in_2020(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 4,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 2,
                    "grade": 55,
                },
                {
                    "sid": 4,
                    "csid": 5,
                    "grade": 80
                },
                {
                    "sid": 1,
                    "csid": 8,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["year"], 2016)
        self.assertEqual(results[0]["enrollment"], 2)
        self.assertEqual(results[1]["year"], 2020)
        self.assertEqual(results[1]["enrollment"], 2)

    def test_two_cs_enrollment_in_2016_and_three_in_2015(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 1,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 1,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 1,
                    "grade": 55,
                },
                {
                    "sid": 1,
                    "csid": 2,
                    "grade": 80.3
                },
                {
                    "sid": 2,
                    "csid": 2,
                    "grade": 52
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2016)
        self.assertEqual(results[0]["enrollment"], 2)

    def test_multiple_cs_enrollments_in_2020_diff_courses(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1,
                    "csid": 4,
                    "grade": 92,
                },
                {
                    "sid": 2,
                    "csid": 5,
                    "grade": 80
                },
                {
                    "sid": 3,
                    "csid": 3,
                    "grade": 55,
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2020)
        self.assertEqual(results[0]["enrollment"], 2)

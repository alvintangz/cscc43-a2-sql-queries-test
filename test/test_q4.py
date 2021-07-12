import unittest

from test.utils.mixins import *
from test.utils.enums import Semester
from test.utils.generic_data import DEPARTMENTS, INSTRUCTORS, COURSES


class QueryFourTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query4"
    query = """
    --Query 4
    """

    def setUp(self):
        """Connect to the database."""
        db.connect()
        self._create_instances(Department, DEPARTMENTS)
        self._create_instances(Course, COURSES)
        self._create_instances(Instructor, INSTRUCTORS)

    def tearDown(self):
        """Disconnect to the database."""
        self._drop_generated_table()
        self._destroy_all_instances()
        db.close()

    def test_columns(self):
        self._execute_query()
        results = self._get_generated_table_columns()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "cname")

    def test_no_cs_courses_in_summer_semester(self):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 2
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC02",
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
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.FALL.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 3,
                    "dcode": "AST",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 0)

    def test_one_cs_course_in_summer_semester_and_other_semesters(self):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 2
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC02",
                    "iid": 1
                },
                {
                    "csid": 3,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2021,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 4,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.FALL.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 3,
                    "dcode": "AST",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 0)

    def test_one_cs_course_taught_by_ast_professor_in_only_summer_semester(
            self
    ):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 2
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC02",
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
                    "year": 2019,
                    "semester": Semester.FALL.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["cname"], "Algorithm Design")

    def test_one_cs_course_in_only_two_summer_semesters_diff_years(self):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 2
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC02",
                    "iid": 1
                },
                {
                    "csid": 3,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2021,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 4,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 3,
                    "dcode": "AST",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["cname"], "Algorithm Design")

    def test_two_cs_courses_both_in_only_two_summer_semesters_diff_years(self):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC02",
                    "iid": 1
                },
                {
                    "csid": 3,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2021,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 4,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2014,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 3,
                    "dcode": "AST",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 2)
        expected = ["Algorithm Design", "Intro to Databases"]
        self.assertIn(results[0]["cname"], expected)
        if results[0]["cname"] in expected:
            expected.remove(results[0]["cname"])
        self.assertIn(results[1]["cname"], "Intro to Databases")
        if results[1]["cname"] in expected:
            expected.remove(results[1]["cname"])
        self.assertEqual(len(expected), 0)

    def test_one_cs_course_only_taught_in_summer_semester_diff_everything(
            self
    ):
        self._create_instances(
            CourseSection,
            [
                {
                    "csid": 1,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2018,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 2,
                    "cid": 1,
                    "dcode": "CSC",
                    "year": 2019,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC02",
                    "iid": 2
                },
                {
                    "csid": 3,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2021,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 1
                },
                {
                    "csid": 4,
                    "cid": 2,
                    "dcode": "CSC",
                    "year": 2014,
                    "semester": Semester.SUMMER.value,
                    "section": "LEC01",
                    "iid": 3
                },
                {
                    "csid": 5,
                    "cid": 3,
                    "dcode": "AST",
                    "year": 2019,
                    "semester": Semester.WINTER.value,
                    "section": "LEC01",
                    "iid": 3
                }
            ]
        )
        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertIn(results[0]["cname"], "Intro to Databases")

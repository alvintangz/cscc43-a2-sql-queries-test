import unittest
from test.utils.mixins import *
from test.utils.generic_data import DEPARTMENTS


class QueryTwoTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query2"
    query = """
    --Query 2
    """

    def setUp(self):
        """Connect to the database."""
        db.connect()
        self._create_instances(Department, DEPARTMENTS)

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
        self.assertEqual(results[0], "num")

    def test_no_fourth_year_female_students_in_cs_dept(self):
        """
        No female students
        """
        self._create_instances(
            Student,
            [
                {
                    "sid": 1,
                    "slastname": "A1",
                    "sfirstname": "A2",
                    "sex": "F",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 3
                },
                {
                    "sid": 2,
                    "slastname": "B1",
                    "sfirstname": "B2",
                    "sex": "M",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 3,
                    "slastname": "C1",
                    "sfirstname": "C2",
                    "sex": "M",
                    "age": 21,
                    "dcode": "MGM",
                    "yearofstudy": 4
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['num'], 0)

    def test_fourth_year_female_students_not_in_cs_dept(self):
        """
        No female students
        """
        self._create_instances(
            Student,
            [
                {
                    "sid": 1,
                    "slastname": "A1",
                    "sfirstname": "A2",
                    "sex": "F",
                    "age": 22,
                    "dcode": "AST",
                    "yearofstudy": 4
                },
                {
                    "sid": 2,
                    "slastname": "B1",
                    "sfirstname": "B2",
                    "sex": "M",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 3,
                    "slastname": "C1",
                    "sfirstname": "C2",
                    "sex": "F",
                    "age": 21,
                    "dcode": "MGM",
                    "yearofstudy": 4
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['num'], 0)

    def test_fourth_year_female_student_in_cs_dept(self):
        """
        No female students
        """
        self._create_instances(
            Student,
            [
                {
                    "sid": 1,
                    "slastname": "A1",
                    "sfirstname": "A2",
                    "sex": "F",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 2,
                    "slastname": "B1",
                    "sfirstname": "B2",
                    "sex": "M",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 3,
                    "slastname": "C1",
                    "sfirstname": "C2",
                    "sex": "F",
                    "age": 21,
                    "dcode": "MGM",
                    "yearofstudy": 4
                },
                {
                    "sid": 4,
                    "slastname": "D1",
                    "sfirstname": "D2",
                    "sex": "M",
                    "age": 19,
                    "dcode": "AST",
                    "yearofstudy": 4
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['num'], 1)

    def test_two_fourth_year_female_students_in_cs_dept(self):
        """
        No female students
        """
        self._create_instances(
            Student,
            [
                {
                    "sid": 1,
                    "slastname": "A1",
                    "sfirstname": "A2",
                    "sex": "F",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 2,
                    "slastname": "B1",
                    "sfirstname": "B2",
                    "sex": "F",
                    "age": 22,
                    "dcode": "CSC",
                    "yearofstudy": 4
                },
                {
                    "sid": 3,
                    "slastname": "C1",
                    "sfirstname": "C2",
                    "sex": "F",
                    "age": 21,
                    "dcode": "MGM",
                    "yearofstudy": 4
                },
                {
                    "sid": 4,
                    "slastname": "D1",
                    "sfirstname": "D2",
                    "sex": "M",
                    "age": 19,
                    "dcode": "AST",
                    "yearofstudy": 4
                },
                {
                    "sid": 5,
                    "slastname": "E1",
                    "sfirstname": "E2",
                    "sex": "F",
                    "age": 21,
                    "dcode": "CSC",
                    "yearofstudy": 3
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['num'], 2)

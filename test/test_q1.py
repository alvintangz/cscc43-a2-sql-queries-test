import unittest
from test.utils.mixins import *
from test.utils.generic_data import DEPARTMENTS


class QueryOneTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query1"
    query = """
    --Query 1
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
        self.assertEqual(results[0], "dname")

    def test_all_phd_degrees(self):
        """
        Should have an empty table.
        """
        self._create_instances(
            Instructor,
            [
                {"iid": 1, "ilastname": "Tang", "ifirstname": "Alvin",
                 "idegree": "PhD", "dcode": "CSC"},
                {"iid": 2, "ilastname": "Bang", "ifirstname": "Blvin",
                 "idegree": "PhD", "dcode": "CSC"},
                {"iid": 3, "ilastname": "Cang", "ifirstname": "Clvin",
                 "idegree": "PhD", "dcode": "AST"},
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 0)

    def test_one_dept_with_highest_non_phd_instructors(self):
        self._create_instances(
            Instructor,
            [
                {"iid": 1, "ilastname": "A1", "ifirstname": "A2",
                 "idegree": "MsC", "dcode": "CSC"},
                {"iid": 2, "ilastname": "B1", "ifirstname": "B2",
                 "idegree": "MsC", "dcode": "CSC"},
                {"iid": 3, "ilastname": "C1", "ifirstname": "C2",
                 "idegree": "MsC", "dcode": "AST"},
                {"iid": 4, "ilastname": "D1", "ifirstname": "D2",
                 "idegree": "PhD", "dcode": "CSC"},
                {"iid": 5, "ilastname": "E1", "ifirstname": "E2",
                 "idegree": "MsC", "dcode": "MGM"},
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["dname"], "Computer Science")

    def test_two_depts_with_highest_non_phd_instructors(self):
        self._create_instances(
            Instructor,
            [
                {"iid": 1, "ilastname": "A1", "ifirstname": "A2",
                 "idegree": "MsC", "dcode": "CSC"},
                {"iid": 2, "ilastname": "B1", "ifirstname": "B2",
                 "idegree": "MsC", "dcode": "CSC"},
                {"iid": 3, "ilastname": "C1", "ifirstname": "C2",
                 "idegree": "MsC", "dcode": "AST"},
                {"iid": 4, "ilastname": "D1", "ifirstname": "D2",
                 "idegree": "PhD", "dcode": "CSC"},
                {"iid": 5, "ilastname": "E1", "ifirstname": "E2",
                 "idegree": "MsC", "dcode": "MGM"},
                {"iid": 6, "ilastname": "F1", "ifirstname": "F2",
                 "idegree": "MsC", "dcode": "MGM"},
                {"iid": 7, "ilastname": "G1", "ifirstname": "G2",
                 "idegree": "MsC", "dcode": "MGM"},
                {"iid": 8, "ilastname": "H1", "ifirstname": "H2",
                 "idegree": "FsC", "dcode": "CSC"},
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)

        expected = ["Business", "Computer Science"]
        self.assertEqual(len(results), len(expected))

        self.assertIn(results[0]["dname"], expected)
        expected.remove(results[0]["dname"])

        self.assertIn(results[1]["dname"], expected)
        expected.remove(results[1]["dname"])

        self.assertEqual(len(expected), 0)

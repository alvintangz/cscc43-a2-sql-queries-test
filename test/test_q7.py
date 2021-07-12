import unittest

from test.utils.mixins import *
from test.utils.enums import Semester
from test.utils.generic_data import DEPARTMENTS, INSTRUCTORS, COURSES, STUDENTS, PREREQUISITES


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
        "cid": 1,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.SUMMER.value,
        "section": "LEC02",
        "iid": 1
    },
    {
        "csid": 3,
        "cid": 3,
        "dcode": "AST",
        "year": 2015,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 4,
        "cid": 2,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.SUMMER.value,
        "section": "LEC01",
        "iid": 3
    },
    {
        "csid": 5,
        "cid": 2,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 3
    },
    {
        "csid": 6,
        "cid": 6,
        "dcode": "CSC",
        "year": 2021,
        "semester": Semester.FALL.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 7,
        "cid": 1,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.WINTER.value,
        "section": "LEC01",
        "iid": 1
    },
    {
        "csid": 8,
        "cid": 1,
        "dcode": "CSC",
        "year": 2016,
        "semester": Semester.WINTER.value,
        "section": "LEC02",
        "iid": 1
    },
]


class QuerySevenTestCase(unittest.TestCase, SqlQueriesTestCaseMixin):
    table = "query7"
    query = """
    --Query 7
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

        self.assertEqual(len(results), 4)
        self.assertEqual(results[0], "cname")
        self.assertEqual(results[1], "semester")
        self.assertEqual(results[2], "year")
        self.assertEqual(results[3], "avgmark")


    # TEST 1: One course with no CS students and students in other departments (should return nothing)

    def test_one_course_with_no_cs_students_and_students_in_other_depts(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 4,
                    "csid": 1,
                    "grade": 70,
                },
                {
                    "sid": 7,
                    "csid": 1,
                    "grade": 60,
                },
                {
                    "sid": 5,
                    "csid": 1,
                    "grade": 60,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)
        self.assertEqual(len(results), 0)
    
    # TEST 2: One course with 2 CS students (and students in other departmartments)

    def test_two_offerings_of_one_course_with_two_cs_students(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 1, # cid: 1
                    "grade": 70,
                },
                {
                    "sid": 2, # CS student
                    "csid": 2, # cid: 1
                    "grade": 70,
                },
                {
                    "sid": 4, # MGM student
                    "csid": 1, # cid: 1
                    "grade": 70,
                }
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)
        self.assertEqual(len(results), 0)

    # TEST 3: Two courses with 3 CS students (should return expected results, highest and lowest course session avgs)
    
    def test_two_course_offerings_same_course_with_three_cs_students(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 80,
                },
                {
                    "sid": 2, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 70,
                },
                {
                    "sid": 3, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 90,
                },
                {
                    "sid": 1, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 60,
                },
                {
                    "sid": 2, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 70,
                },
                {
                    "sid": 3, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 100,
                },
                {
                    "sid": 6, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 100,
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
                    "cname": "Intro to Databases",
                    "semester": Semester.SUMMER.value,
                    "year": 2016,
                    "avgmark": 82.5,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 80.0,
                }
            ]
        )

    # TEST 4: One course section with 3 CS students (should return expected results, highest and lowest course session avgs)
    
    def test_course_section_with_three_cs_students(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 80,
                },
                {
                    "sid": 2, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 70,
                },
                {
                    "sid": 3, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 90,
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
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 80.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 80.0,
                }
            ]
        )

    # TEST 5: Courses with CS students and courses with no CS students (should omit courses with no cs students, and return expected results for courses with cs students)

    def test_course_with_cs_students_and_course_with_no_cs_students(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 80,
                },
                {
                    "sid": 2, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 70,
                },
                {
                    "sid": 3, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 90,
                },
                {
                    "sid": 4, # Non CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 60,
                },
                {
                    "sid": 5, # Non CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 70,
                },
                {
                    "sid": 7, # Non CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 100,
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
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 80.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 80.0,
                }
            ]
        )
        
    # TEST 6: Courses with CS students, where there is a tie (highest and lowest avgs are equal)
    def test_one_course_offering_with_at_least_three_cs_students_both_tied(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 3, # Course 3 (Fall)
                    "grade": 50,
                },
                {
                    "sid": 2, # CS student
                    "csid": 3, # Course 3 (Fall)
                    "grade": 60,
                },
                {
                    "sid": 3, # CS student
                    "csid": 3, # Course 3 (Fall)
                    "grade": 70,
                },
                {
                    "sid": 4, # MGM student
                    "csid": 3, # Course 3 (Fall)
                    "grade": 80,
                },
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 55,
                },
                {
                    "sid": 4, # MGM student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 60,
                },
                {
                    "sid": 5, # AST student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 65,
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
                    "cname": "Intro to Astronomy",
                    "semester": Semester.FALL.value,
                    "year": 2015,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Astronomy",
                    "semester": Semester.FALL.value,
                    "year": 2015,
                    "avgmark": 65.0,
                }
            ]
        )        

    # TEST 7: Course offerings with CS students (multiple highest avgs and multiple lowest avgs)

    def test_course_offerings_for_one_course_with_cs_students_multiple_lowest_and_highest(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 50,
                },
                {
                    "sid": 2, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 60,
                },
                {
                    "sid": 3, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 70,
                },
                {
                    "sid": 4, # MGM student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 80,
                },
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 30,
                },
                {
                    "sid": 2, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 40,
                },
                {
                    "sid": 3, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 50,
                },
                {
                    "sid": 6, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 100
                },
                {
                    "sid": 1, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 95
                },
                {
                    "sid": 2, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 90
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
                    "cname": "Intro to Databases",
                    "semester": Semester.WINTER.value,
                    "year": 2016,
                    "avgmark": 95.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 40.0,
                },
            ]
        )

    # TEST 8: Courses with CS students, but course session is in current semester

    def test_course_with_cs_students_but_in_current_semester(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 6, # Current Semester
                    "grade": 50,
                },
                {
                    "sid": 2, # CS student
                    "csid": 6, # Current Semester
                    "grade": 60,
                },
                {
                    "sid": 3, # CS student
                    "csid": 6, # Current Semester
                    "grade": 70,
                },
            ]
        )

        self._execute_query()
        results = self._get_generated_table()
        logging.info(results)
        self.assertEqual(len(results), 0)

    def test_course_offering_in_current_semester_and_not_current_semester(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 6, # Current Semester
                    "grade": 50,
                },
                {
                    "sid": 2, # CS student
                    "csid": 6, # Current Semester
                    "grade": 60,
                },
                {
                    "sid": 3, # CS student
                    "csid": 6, # Current Semester
                    "grade": 70,
                },
                {
                    "sid": 6, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 100
                },
                {
                    "sid": 1, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 95
                },
                {
                    "sid": 2, # CS student
                    "csid": 7, # Course 1 (Winter)
                    "grade": 90
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
                    "cname": "Intro to Databases",
                    "semester": Semester.WINTER.value,
                    "year": 2016,
                    "avgmark": 95.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.WINTER.value,
                    "year": 2016,
                    "avgmark": 95.0,
                },
            ]
        )

    def test_course_offerings_with_cs_students_all_tie(self):
        self._create_instances(
            StudentCourse,
            [
                {
                    "sid": 1, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 50,
                },
                {
                    "sid": 2, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 60,
                },
                {
                    "sid": 3, # CS student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 70,
                },
                {
                    "sid": 4, # MGM student
                    "csid": 2, # Course 1 (Summer)
                    "grade": 80,
                },
                {
                    "sid": 1, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 60,
                },
                {
                    "sid": 2, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 70,
                },
                {
                    "sid": 3, # CS student
                    "csid": 1, # Course 1 (Fall)
                    "grade": 65,
                },
                {
                    "sid": 6, # CS student
                    "csid": 3, # Course 3 (Fall 2015)
                    "grade": 65
                },
                {
                    "sid": 1, # CS student
                    "csid": 3, # Course 3 (Fall 2015)
                    "grade": 65
                },
                {
                    "sid": 2, # CS student
                    "csid": 3, # Course 3 (Fall 2015)
                    "grade": 65
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
                    "cname": "Intro to Databases",
                    "semester": Semester.SUMMER.value,
                    "year": 2016,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.SUMMER.value,
                    "year": 2016,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Databases",
                    "semester": Semester.FALL.value,
                    "year": 2019,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Astronomy",
                    "semester": Semester.FALL.value,
                    "year": 2015,
                    "avgmark": 65.0,
                },
                {
                    "cname": "Intro to Astronomy",
                    "semester": Semester.FALL.value,
                    "year": 2015,
                    "avgmark": 65.0,
                },
            ]
        )

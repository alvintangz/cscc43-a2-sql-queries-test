import logging
import copy

from typing import List, Dict, Any
from test.utils.database import *


class SqlQueriesTestCaseMixin:
    query = None
    table = None

    def _execute_query(self):
        """
        Executes the current query that's being tested.
        """
        db.execute_sql("SET search_path TO A2;")
        db.execute_sql(self.query)

    def _get_generated_table(self) -> List[Dict[str, Any]]:
        """
        After running `self._execute_query()`, use this to retrieve the
        rows (with column names) of the table that was created.
        """
        neat_table = []
        try:
            db.execute_sql("SET search_path TO A2;")
            cursor = db.execute_sql(f"SELECT * FROM {self.table}")
            columns = [column[0] for column in cursor.description]
            # Get bpchar type - so we can strip
            bpchar_type = db.execute_sql(
                "SELECT oid FROM pg_type WHERE typname = 'bpchar'"
            ).fetchall()[0][0]
            for row in cursor.fetchall():
                row_dict = dict()
                for idx, item in enumerate(row):
                    row_dict[columns[idx]] = item
                    if cursor.description[idx][1] == bpchar_type:
                        row_dict[columns[idx]] = item.rstrip()
                neat_table.append(row_dict)
        except Exception:
            db.close()
        return neat_table

    def _get_generated_table_columns(self) -> List[str]:
        """
        After running `self._execute_query()`, use this to retrieve the
        column names of the table that was created.
        """
        if self.table is None:
            print("Table doesn't exist")
            exit()

        db.execute_sql("SET search_path TO A2;")
        cursor = db.execute_sql(f"SELECT * FROM {self.table}")
        return [column[0] for column in cursor.description]

    def _create_instances(self, model, data):
        """
        Creates multiple instances (or rows) of `model` type in the database.
        Returns these instances back.
        """
        created = []
        for instance in data:
            created.append(model.create(**instance))
        return created

    def _destroy_instances(self, model, instances):
        """
        Deletes multiple instances of `model` type in the database.
        """
        for instance in instances:
            model.delete_instance(instance)

    def _destroy_all_instances(self):
        """
        Clears all the tables in the database.
        """
        db.execute_sql(
            """
                SET search_path TO A2;
                DELETE FROM prerequisites;
                DELETE FROM studentCourse;
                DELETE FROM courseSection;
                DELETE FROM course;
                DELETE FROM instructor;
                DELETE FROM student;
                DELETE FROM department;
            """
        )

    def _drop_generated_table(self):
        """
        Drops the table named `self.table` in the database if exists.
        """
        db.execute_sql(
            f"""
                SET search_path TO A2;
                DROP TABLE IF EXISTS {self.table};
            """
        )

    def _save_generated_table_as(self, table_name):
        """
        After running `self._execute_query()`, use this to save the table
        in the database with name `table_name`.
        """
        db.execute_sql(
            f"""
                SET search_path TO A2;
                DROP TABLE IF EXISTS {table_name};
                CREATE TABLE {table_name} AS (SELECT * FROM {self.table});
            """
        )

    def _assert_records_equal(self, actual, expected):
        """
        Asserts that `expected` is equal to `actual`. `actual` and `expected`
        are a list of dictionaries, with each dictionary representing a record
        in the generated database.
        """
        self.assertEqual(len(actual), len(expected))

        # re_actual is `actual` but reformatted to match indexes of expected
        re_actual = []
        for expected_item in expected:
            for actual_item in actual:
                if expected_item == actual_item:
                    re_actual.append(actual_item)
                    break

        self.assertEqual(len(actual), len(re_actual))
        # This may be pointless, but let's do it...
        for idx in range(0, len(expected)):
            self.assertEqual(re_actual[idx], expected[idx])

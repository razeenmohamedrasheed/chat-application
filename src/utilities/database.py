import psycopg2

class Database():
    def __init__(self):
        self.conn = psycopg2.connect(
            database='chatapplication',
            user='postgres',
            password='Admin',
            host="127.0.0.1",
            port=5432

        )

    def insert_query(self, table, columns, values, auto_commit=True):
        """
        Inserts a new record into the specified table.

        Args:
            table (str): The name of the table.
            columns (list): List of column names.
            values (list): List of values corresponding to the columns.
            auto_commit (bool): Whether to commit the transaction immediately. Default is True.
        """
        cursor = self.conn.cursor()
        try:
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            cursor.execute(query, values)
            if auto_commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # Rollback on error to maintain database integrity
            raise e
        finally:
            cursor.close()  # Ensure the cursor is closed in all cases

    def select_query(self, table_name):
        """
        Executes a SELECT query to fetch all rows from the specified table.

        Args:
            table_name (str): The name of the table to query.

        Returns:
            list: A list of tuples containing the rows retrieved from the table.

        Raises:
            Exception: If an error occurs during query execution.
        """
        # Create a cursor object to interact with the database
        cursor = self.conn.cursor()
        try:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)

            # Get column names from the cursor
            column_names = [desc[0] for desc in cursor.description]

            # Fetch all rows and map to dictionaries
            results = [dict(zip(column_names, row)) for row in cursor.fetchall()]

            return results

        except Exception as e:
            # Rollback the transaction in case of any error to maintain database integrity
            self.conn.rollback()
            raise e  # Re-raise the exception for the caller to handle

        finally:
            # Ensure the cursor is always closed to release resources
            cursor.close()



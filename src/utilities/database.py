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

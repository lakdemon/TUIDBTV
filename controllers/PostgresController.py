import psycopg
from psycopg import ProgrammingError
from textual.containers import Grid
from textual.validation import Number
from textual.widgets import Label, Input

from controllers.DBController import DBController


class PostgresController(DBController):
    def __init__(self, _dbname, _user, _password, _host, _port):
        self.connection = psycopg.connect(dbname=_dbname, user=_user, password=_password, host=_host,
                                          port=_port)

    def executeQuery(self, query_text):
        try:
            data = self.connection.cursor().execute(query_text).fetchall()
            self.connection.commit()
            return data
        except:
            self.connection.commit()
            raise

    def executeQueryWithHeaders(self, query_text):
        try:
            cursor = self.connection.cursor()
            try:
                data = cursor.execute(query_text).fetchall()
            except ProgrammingError:
                data = []
            header_data = tuple(column_name[0] for column_name in cursor.description or [])
            data.insert(0, header_data)
            return data
        except Exception as e:
            self.connection.rollback()
            raise e

    def getSchemaNames(self):
        return self.executeQuery("SELECT distinct table_schema FROM information_schema.tables")

    def getTableNamesBySchema(self, schemaName):
        return self.executeQuery(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schemaName}'")

    def getTablePreview(self, schemaName, tableName):
        data = self.executeQuery(f"SELECT * FROM {schemaName}.{tableName} limit 100")
        cutted_data = []
        for row in data:
            cutted_data.append(
                tuple(
                    str(cell)[:50] for cell in row
                )
            )
        headers = self.executeQuery(
            f"SELECT column_name from information_schema.columns where table_name = '{tableName}'")
        tableData = []
        headerData = tuple(column_name[0] for column_name in headers)
        tableData.append(headerData)
        for row in cutted_data:
            tableData.append(row)
        return tableData

    @staticmethod
    def get_connection_form():
        return Grid(
            Label("Username"),
            Input(placeholder="postgres", id="userName", classes="CONNECTION_DATA_FIELD"),
            Label("Password"),
            Input(placeholder="", id="password", password=True, classes="CONNECTION_DATA_FIELD"),
            Label("Hostname/IP"),
            Input(placeholder="localhost", id="hostName", classes="CONNECTION_DATA_FIELD"),
            Label("Port"),
            Input(placeholder="5432", id="port", validators=[Number()], classes="CONNECTION_DATA_FIELD"),
            Label("Database"),
            Input(placeholder="public", id="database", classes="CONNECTION_DATA_FIELD"),
            id="connection_form"
        )
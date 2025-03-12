import sqlite3

class ErrorMapper:
    error_codes = {
        ValueError: "Error 301 - Value Error",
        FileNotFoundError: "Error 302 - File Not Found",
        sqlite3.OperationalError: "Error 303 - Operational Error",
        sqlite3.DatabaseError: "Error 304 - Database Error",
        sqlite3.IntegrityError: "Error 305 - Integrity Error",
        sqlite3.ProgrammingError: "Error 306 - Syntax or Invalid Operation",
        sqlite3.DataError: "Error 307 - Data Error",
        sqlite3.NotSupportedError: "Error 308 - Undefined non-fatal issue",
        sqlite3.InterfaceError: "Error 309 - Database Connection Error",
        sqlite3.Warning: "Error 399 - Not Supported Error",
}
    @staticmethod
    def get_error_message(error):
        return ErrorMapper.error_codes.get(error, f'Unexpected error occurred: {error}')


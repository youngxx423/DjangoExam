"""Project package init.

Prefer mysqlclient (MySQLdb). Fall back to PyMySQL only when MySQLdb
is unavailable.
"""

try:
    import MySQLdb  # noqa: F401
except Exception:
    import pymysql

    pymysql.install_as_MySQLdb()

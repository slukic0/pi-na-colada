# import json
import sqlite3 as sql3

from datetime import datetime, timezone

apiKey = "a808bbf30202728efca23e099a4eecc7"

dbconnect = sql3.connect("pumpLogger.db", check_same_thread=False)

dbconnect.row_factory = sql3.Row

cursor = dbconnect.cursor()


def write_to_SQL_Table(status: str, severity: str, info: str):
    '''
    Write to local SQL table
    status: OK or ERROR
    severity: INFO, WARN, or ERROR
    info: any addtional information
    '''
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS Pump_Status(time DATETIME, status STRING, severity STRING, info STRING);')
    dbconnect.commit()

    now = datetime.now(timezone.utc)

    if info != "":
        cursor.execute('''insert into Pump_Status values  (?, ?, ?, ?)''',
                       (now, status, severity, info))
    else:
        cursor.execute('''insert into Pump_Status (time, status, severity) values  (?, ?, ?)''',
                       (now, status, severity))

    dbconnect.commit()


def read_SQL_table(severity):
    '''
    READ local SQL table
    severity: INFO, WARN, or ERROR
    '''
    row = cursor.execute(
        "SELECT * FROM Pump_Status WHERE severity = ? ORDER BY time DESC", (severity,))
    dbconnect.commit()

    records = row.fetchall()
    response = []
    for row in records:
        response.append(
            {"time": row[0], "status": row[1], "severity": row[2], "info": row[3]})

    return response

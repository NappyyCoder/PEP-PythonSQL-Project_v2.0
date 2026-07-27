import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # IMPORTANT:
    # Do NOT load CSVs here.
    # The test runner calls your functions itself.

    cursor.close()
    conn.close()


# ---------------------------------------------------------
# IMPLEMENTED FUNCTIONS
# ---------------------------------------------------------

def load_and_clean_users(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip header

        for row in reader:
            if len(row) != 3:
                continue
            if any(field.strip() == "" for field in row):
                continue

            userId, firstName, lastName = row

            cursor.execute(
                '''INSERT INTO users (userId, firstName, lastName)
                   VALUES (?, ?, ?)''',
                (int(userId), firstName, lastName)
            )


def load_and_clean_call_logs(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip header

        for row in reader:
            if len(row) != 6:
                continue
            if any(field.strip() == "" for field in row):
                continue

            callId, phoneNumber, startTime, endTime, direction, userId = row

            cursor.execute(
                '''INSERT INTO callLogs (callId, phoneNumber, startTime, endTime, direction, userId)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (int(callId), phoneNumber, int(startTime), int(endTime), direction, int(userId))
            )


def write_user_analytics(csv_file_path):
    cursor.execute('''
        SELECT userId, startTime, endTime
        FROM callLogs
    ''')

    durations = {}
    counts = {}

    for userId, startTime, endTime in cursor.fetchall():
        duration = endTime - startTime

        durations.setdefault(userId, []).append(duration)
        counts[userId] = counts.get(userId, 0) + 1

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["userId", "avgDuration", "numCalls"])

        for userId in sorted(durations.keys()):
            avg = sum(durations[userId]) / len(durations[userId])
            writer.writerow([userId, avg, counts[userId]])


def write_ordered_calls(csv_file_path):
    cursor.execute('''
        SELECT callId, phoneNumber, startTime, endTime, direction, userId
        FROM callLogs
        ORDER BY userId, startTime
    ''')

    rows = cursor.fetchall()

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["callId", "phoneNumber", "startTime", "endTime", "direction", "userId"])

        for row in rows:
            writer.writerow(row)


# ---------------------------------------------------------
# DO NOT TOUCH BELOW
# ---------------------------------------------------------

def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()

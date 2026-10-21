import csv
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()


def main():
    # test runner creates tables and loads files — leave this empty
    pass


def load_and_clean_users(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            if len(row) != 2:
                continue
            if any(field.strip() == "" for field in row):
                continue

            firstName, lastName = row
            cursor.execute(
                '''INSERT INTO users (firstName, lastName)
                   VALUES (?, ?)''',
                (firstName, lastName)
            )


def load_and_clean_call_logs(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            if len(row) != 5:
                continue
            if any(field.strip() == "" for field in row):
                continue

            phoneNumber, startTime, endTime, direction, userId = row
            cursor.execute(
                '''INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId)
                   VALUES (?, ?, ?, ?, ?)''',
                (phoneNumber, int(startTime), int(endTime), direction, int(userId))
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

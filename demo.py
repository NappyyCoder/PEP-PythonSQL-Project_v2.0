"""Run the call-center pipeline on the sample files in resources/.

The graded test runner creates the SQLite tables and calls the functions in
src/main/main.py itself. This script performs that setup for a local run.
"""

import os

from src.main.main import (
    cursor,
    load_and_clean_call_logs,
    load_and_clean_users,
    write_ordered_calls,
    write_user_analytics,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(ROOT, "resources")


def create_tables():
    cursor.execute("DROP TABLE IF EXISTS callLogs")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute(
        """CREATE TABLE users (
               userId INTEGER PRIMARY KEY,
               firstName TEXT,
               lastName TEXT
           )"""
    )
    cursor.execute(
        """CREATE TABLE callLogs (
               callId INTEGER PRIMARY KEY,
               phoneNumber TEXT,
               startTime INTEGER,
               endTime INTEGER,
               direction TEXT,
               userId INTEGER,
               FOREIGN KEY (userId) REFERENCES users(userId)
           )"""
    )


def main():
    create_tables()

    users_path = os.path.join(RESOURCES, "users.csv")
    calls_path = os.path.join(RESOURCES, "callLogs.csv")
    analytics_path = os.path.join(RESOURCES, "userAnalytics.csv")
    ordered_path = os.path.join(RESOURCES, "orderedCalls.csv")

    load_and_clean_users(users_path)
    load_and_clean_call_logs(calls_path)
    write_user_analytics(analytics_path)
    write_ordered_calls(ordered_path)

    user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    call_count = cursor.execute("SELECT COUNT(*) FROM callLogs").fetchone()[0]

    print("Python SQL API with File I/O")
    print("Call center data pipeline")
    print()
    print(f"Users loaded:     {user_count}")
    print(f"Call logs loaded: {call_count}")
    print("Analytics file:   resources/userAnalytics.csv")
    print("Ordered calls:    resources/orderedCalls.csv")
    print()
    print("userId  avgDuration  numCalls")
    print("------  -----------  --------")
    with open(analytics_path, newline="") as handle:
        next(handle)
        for line in handle:
            user_id, average, count = line.strip().split(",")
            print(f"{user_id:<6}  {average:<11}  {count}")

    print()
    print("Ordered call logs (userId, then startTime)")
    print("callId  phoneNumber   startTime   endTime     direction  userId")
    with open(ordered_path, newline="") as handle:
        next(handle)
        for line in handle:
            call_id, phone, start, end, direction, user_id = line.strip().split(",")
            print(
                f"{call_id:<6}  {phone:<12}  {start:<10}  {end:<10}  "
                f"{direction:<9}  {user_id}"
            )


if __name__ == "__main__":
    main()

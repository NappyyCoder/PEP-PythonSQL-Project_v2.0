# Python SQL API with File I/O

Repo: [https://github.com/NappyyCoder/Python-SQL-API-with-File-IO](https://github.com/NappyyCoder/Python-SQL-API-with-File-IO)

Wiki (architecture): [https://github.com/NappyyCoder/Python-SQL-API-with-File-IO/wiki](https://github.com/NappyyCoder/Python-SQL-API-with-File-IO/wiki)

## Project Description

Backend app for a fake call center. It tracks users (agents) and call logs, loads them from CSV into an in-memory SQLite database, and exports two report files.

Input files live in `resources/`:

- `users.csv` — first and last name
- `callLogs.csv` — phone number, start/end time, direction, user id

Bad rows get skipped (wrong number of columns or blank fields). Good rows go into SQLite. Then the program writes:

- `userAnalytics.csv` — per user: average call length and how many calls they had
- `orderedCalls.csv` — all calls sorted by user, then by start time

There’s no UI. Everything runs from the command line. The functions you grade are in `src/main/main.py`. I added `demo.py` so you can create the tables locally and run the full flow on the sample CSVs. More detail on tables and data flow is on the [wiki Architecture page](https://github.com/NappyyCoder/Python-SQL-API-with-File-IO/wiki/Architecture) (same content as `docs/wiki/Architecture.md` in the repo).

## Technologies Used

- Python 3.13 (3.10+ works)
- SQLite 3.45 via built-in `sqlite3` (`:memory:` database)
- `csv` and `unittest` from the standard library

No pip packages. Runs on your machine only (not AWS/GCP specific). Works on Mac, Linux, and Windows.

## Features

- Import and clean user data from CSV into `users`
- Import and clean call data from CSV into `callLogs`
- SQLite auto-increments `userId` and `callId`
- Build user analytics (avg duration + call count)
- Export sorted call log CSV
- Unit tests in `src/test/lab_test.py`

### To-do list

- Persist DB to a file instead of only in memory
- CLI flags for custom CSV paths
- Validate phone numbers and timestamps
- Round `avgDuration` for cleaner reports

## Getting Started

You need Git and Python 3.10+.

![How data flows through the app](docs/images/architecture.png)

**Mac / Linux**

```bash
git clone https://github.com/NappyyCoder/Python-SQL-API-with-File-IO.git
cd Python-SQL-API-with-File-IO
python3 demo.py
python3 -m unittest src.test.lab_test -v
```

**Windows**

```bat
git clone https://github.com/NappyyCoder/Python-SQL-API-with-File-IO.git
cd Python-SQL-API-with-File-IO
py -3 demo.py
py -3 -m unittest src.test.lab_test -v
```

If `py -3` doesn’t work on Windows, try `python`. On Mac/Linux use `python3`.

`demo.py` overwrites `resources/userAnalytics.csv` and `resources/orderedCalls.csv`. Tests use the smaller files under `src/test/`.

Note: `main()` in `src/main/main.py` stays empty on purpose — the Revature test runner creates tables and calls the loader/export functions for you.

## Usage

From the project folder:

Mac / Linux: `python3 demo.py`

Windows: `py -3 demo.py`

On the bundled data you should see 5 users and 15 calls loaded (after cleaning). Output goes to the terminal and the two CSV files under `resources/`.

![Example demo output](docs/images/sample-output.png)

Sample analytics:

```csv
userId,avgDuration,numCalls
1,105.0,4
2,40.0,5
3,70.0,1
4,55.0,2
5,100.0,3
```

`avgDuration` = average of `(endTime - startTime)` in seconds for that user.

Ordered calls file header:

```csv
callId,phoneNumber,startTime,endTime,direction,userId
```

Sort order: `userId` ASC, then `startTime` ASC.

Run tests only:

```bash
python3 -m unittest src.test.lab_test -v
```

```bat
py -3 -m unittest src.test.lab_test -v
```

## Contributors

Solo project — [NappyyCoder](https://github.com/NappyyCoder)

## License

MIT — see [LICENSE](LICENSE).

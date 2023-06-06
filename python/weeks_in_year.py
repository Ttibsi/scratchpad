import datetime

def main():
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)
    weeks_passed = (today - year_start).days // 7
    print(f"Weeks passed so far this year: {weeks_passed}")

if __name__ == '__main__':
    raise SystemExit(main())

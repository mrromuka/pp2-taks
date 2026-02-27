#1
from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)
print(new_date)
#2
from datetime import datetime, timedelta

today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#3
from datetime import datetime

now = datetime.now()
no_microseconds = now.replace(microsecond=0)

print(no_microseconds)
#4
from datetime import datetime

date1_str = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")
date2_str = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

diff_seconds = abs((date2 - date1).total_seconds())
print(f"Difference in seconds: {diff_seconds}")



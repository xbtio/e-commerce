from datetime import datetime
import pytz

# Get the current UTC time
utc_now = datetime.utcnow()

# Specify the UTC+3 time zone
utc_plus_3 = pytz.timezone('Europe/Moscow')  # or 'Asia/Riyadh' or another UTC+3 time zone

# Convert the UTC time to UTC+3
utc_plus_3_time = utc_now.replace(tzinfo=pytz.utc).astimezone(utc_plus_3)

print("UTC+3 time:", utc_plus_3_time)

# convert it to str in format YYYY-MM-DD/HH:MM:SS 
utc_plus_3_time = utc_plus_3_time.strftime("%Y-%m-%d/%H:%M:%S")
print("UTC+3 time:", utc_plus_3_time)
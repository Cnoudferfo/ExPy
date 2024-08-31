from datetime import datetime
import pytz

# Define the date strings
date1 = "2024/8/30 下午 11:08"
date2 = "2024-08-30 23:08:02+00:00"

# Replace "下午" with "PM" and "上午" with "AM"
date1 = date1.replace("下午", "PM").replace("上午", "AM")
print("date1=", date1)

# Parse date1 (assuming it's in local time and using a custom format)
date1_parsed = datetime.strptime(date1, "%Y/%m/%d %p %I:%M")
print(f"date1_parsed={date1_parsed}")

# Parse date2 (assuming it's in ISO 8601 format)
date2_parsed = datetime.fromisoformat(date2)
print(f"date2_parsed={date2_parsed}")

# Convert date1 to UTC (assuming local time is UTC+8)
local_tz = pytz.timezone('Asia/Taipei')
date1_localized = local_tz.localize(date1_parsed)
date1_utc = date1_localized.astimezone(pytz.utc)

# Ensure date2 is in UTC
date2_utc = date2_parsed.astimezone(pytz.utc)

# Truncate date2 to remove seconds for comparison
date2_truncated = date2_utc.replace(second=0, microsecond=0)

# Format both dates to the same string format
date1_str = date1_parsed.strftime("%Y-%m-%d %H:%M")
date2_str = date2_truncated.strftime("%Y-%m-%d %H:%M")

# Compare the formatted date strings
print("Date1:", date1_str)
print("Date2:", date2_str)
print("Are the dates equal?", date1_str == date2_str)
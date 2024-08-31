from datetime import datetime

# Define the date strings
date1 = "2024/8/30 下午 11:08"
date2 = "2024-08-30 23:08:02+00:00"

# Replace "下午" with "PM" and "上午" with "AM"
date1 = date1.replace("下午", "PM").replace("上午", "AM")
print("date1=", date1)

# Parse date1 (using a custom format)
date1_parsed = datetime.strptime(date1, "%Y/%m/%d %p %I:%M")
print(f"date1_parsed={date1_parsed}")

# Parse date2 (assuming it's in ISO 8601 format)
date2_parsed = datetime.fromisoformat(date2)
print(f"date2_parsed={date2_parsed}")

# Truncate date2 to remove seconds for comparison
date2_truncated = date2_parsed.replace(second=0, microsecond=0)

# Format both dates to the same string format
date1_str = date1_parsed.strftime("%Y-%m-%d %H:%M:%S")
date2_str = date2_truncated.strftime("%Y-%m-%d %H:%M:%S")

# Compare the formatted date strings
print("Date1:", date1_str)
print("Date2:", date2_str)
print("Are the dates equal?", date1_str == date2_str)
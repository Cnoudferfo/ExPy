# Define the dropped data
dropped_data = ['寄件者\t主旨\t收到日期\t大小\t', '曾嘉明\tTry from apple\t2024/8/30 下午 11:08\t2,884,169\t']

# Split the header and data rows
header = dropped_data[0].strip().split('\t')
data = dropped_data[1].strip().split('\t')

# Create a dictionary from the header and data values
email_dict = dict(zip(header, data))

# Access the values
sender = email_dict['寄件者']
subject = email_dict['主旨']
received_time = email_dict['收到日期']
size = email_dict['大小']

print("Sender:", sender)
print("Subject:", subject)
print("Received Time:", received_time)
print("Size:", size)
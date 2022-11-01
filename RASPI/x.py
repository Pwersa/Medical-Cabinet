
# Import datetime module
import datetime
 
# Get current date and time
dt = datetime.datetime.now()
 
# This is going to remove the milliseconds
x = dt.replace(microsecond=0)
print(x)
#
# import datetime
#
# now = datetime.date.today()
#
# print (now)

from datetime import datetime
from datetime import timedelta

N = 2

date_N_days_ago = datetime.now() - timedelta(N)

print (datetime.now().date())
print (date_N_days_ago.date())


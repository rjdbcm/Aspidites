from Aspidites._vendor.contracts.test_registrar import fail, good, syntax_fail
from datetime import datetime

date = datetime(2021, 3, 21)

good('dtz(2021,3,21,GMT)', date.astimezone())
fail('dtz', date)
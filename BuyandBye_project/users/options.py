# Users option choices
from datetime import date

current_date = date.today()

YEARS = [x for x in range(1920, current_date.year + 1)]

STATE_CHOICES = (
    ("Province 1", "Province 1"),
    ("Province 2", "Province 2"),
    ("Province 3 (Bagmati)", "Province 3 (Bagmati)"),
    ("Province 4 (Gandaki)", "Province 4 (Gandaki)"),
    ("Province 5", "Province 5"),
    ("Province 6 (Karnali)", "Province 6 (Karnali)"),
    ("Province 7 (Sudurpaschim)", "Province 7 (Sudurpaschim)"),
)

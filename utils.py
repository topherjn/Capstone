# created finally to modularize turning month, day, year into 
# "TIMEID" need to go back and factor to use in all places needed
def make_timeid(year, month, day):
    timeid = str(year) + str(month).rjust(2,'0') + str(day).rjust(2,'0')
    return timeid
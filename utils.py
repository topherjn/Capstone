# created finally to modularize turning month, day, year into 
# "TIMEID" need to go back and factor to use in all places needed
def make_timeid(year, month, day):
    if day != 0:
        timeid = str(year) + str(month).rjust(2,'0') + str(day).rjust(2,'0')
    else: 
        timeid = str(year) + str(month).rjust(2,'0')
        
    return timeid

# restrict user input to integers
def get_integer(prompt):
    value = input(prompt)
    try:
        return int(value)
    except ValueError:
        print(f"{value} invalid: Try again.")
        return get_integer(prompt)
#!/usr/bin/env python3
''' SpaceAgeCalc allows a users to calcuate a persons age on various different planets. The user
    may enter the persons age as a dob or simple a value for their age.

    Author: Murray Watson
    Email: murster972@yahoo.com
    Python Version: 3.5.2 '''

try:
    import sys, os
    from datetime import datetime
except:
    print("The following modules are required to run this program: sys, os and datetime")
    sys.exit(-1)


class SpaceAgeCalc:
    def __init__(self):
        self.earth_years = {"Mercury": 0.2408467, "Venus": 0.61519726, "Earth": 1,
                            "Mars": 1.8808158, "Jupiter": 11.862615, "Saturn": 29.447498,
                            "Uranus": 84.016846, "Neptune": 164.79132, "Pluto": 248}
        self.planets = [p for p in self.earth_years]
        self.months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        clear_scr = lambda: os.system("cls") if sys.platform == "win32" else os.system("clear")

        try:
            while True:
                clear_scr()
                opt = input("---Welcome to SpaceCalc!---\n[1] - Calculate Space Age\n[2] - Show Planet Conversions\n[3] - Exit\nOption: ").strip()

                if opt == "1":
                    age_opt = input("\nAge [1] or DoB [2]: ").strip()

                    if age_opt == "1":
                        age = self.get_age()
                    elif age_opt == "2":
                        age = self.get_dob()
                    else:
                        print("\n[-] Invalid Option.")
                        p = input("\nPress enter to continue...")
                        continue

                    if age == -1:
                        p = input("\nPress enter to continue...")
                        continue

                    p = self.get_planets()

                    if p == -1:
                        p = input("\nPress enter to continue...")
                        continue

                    space_age = self.calc_space_age(age, p)

                    print("\nYour space ages are...")

                    print("\n   {0:7}  |  Age (yr)".format("Planet"))
                    print("-" * 24)

                    for p in space_age: print("   {0:7}  |  {1}".format(p, space_age[p]))


                elif opt == "2":
                    print("\nPlanet - Plane Name\nYears - one earth year on the planet\n")

                    print("\n  {0:7}  |  Years".format("Planet"))
                    print("-" * 26)

                    for i in self.planets: print("  {0:7}  |  {1}".format(i, self.earth_years[i]))

                elif opt == "3":
                    print("Goodebye!")
                    sys.exit(0)

                else:
                    print("\n[-] Invalid option.")

                pause = input("\nEnter to continue...")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            sys.exit(0)

    ' Gets and validates users age '
    def get_age(self):
        print("""Age Format:
        yr - Years, mn - Months, wk - Weeks, dy - Days, mi - Minutes, sc - Seconds
        Indicators follow a numerical value and can be used together, e.g. 1Yr2mn3dY4mi0.003Sc
        would be 1 year 2 months 3 days 4 minutes and 0.003 seconds.
        Format is not case sensitive. age cannot be more than 100 chars long""")

        age = input("\nAge: ").strip()

        if not age or len(age) > 100:
            print("[-] length of age input must be >1 and <=100.")
            return -1

        #verifys age input is of valid syntax and converts to years
        indicators = ["yr", "mn", "wk", "dy", "mi", "sc"]
        values = {i:0 for i in indicators}

        i = 0
        val = ""
        err = [0, "Age"]

        while i < len(age):
            v = age[i]
            try:
                if not self.is_numeric(v) and v != '.':
                    #indicators are in char pairs, so one char will occur after another if valid
                    ind = (v + age[i + 1]).lower()

                    if ind not in indicators or not self.is_numeric(val):
                        err = [1, "Value/s" if not self.is_numeric(val) else "Indicator/s"]
                        break

                    values[ind] += float(val)
                    val = ""
                    i += 2

                else:
                    val += v
                    i += 1
            except IndexError:
                #catches any trailing chars at end of age
                #or any single letter age inputs
                err[0] = 1
                break

        #checks for any errs set already
        #"." catches single dots as inputs and is_numeric(age[-1]) any values
        #without indicators at end of age input
        if err[0] or self.is_numeric(age[-1]) or val == ".":
            print("Invalid {}: {}".format(err[1], age))
            return -1

        age = [values[indicators[i]] for i in range(len(indicators))]
        total_years = self.get_earth_years(age)

        return total_years

    ''' Gets and validates users DoB, then converts to age
        :output age: returns dob converted to age in years '''
    def get_dob(self):
        print("\nPlease enter your DoB in the format DD:MM:YYYY, e.g. 01:01:1990, is the 1st of Jan 1990. Minimum dob available is 01:01:1000")
        dob = input("\nDoB: ").strip().split(":")

        if len(dob) != 3:
            print("Invalid DoB: {}".format(":".join(dob)))
            return -1

        #checks dob is valid
        try:
            d, m, y = tuple(map(int, dob))

            tmp_m = [] + self.months

            #leap years
            if y % 4 == 0 and (y % 100 != 0 or (y % 100 == 0 and y % 400 == 0)):
                tmp_m[1] = 29

            if  not 1 <= m <= 12 or not 1 <= d < tmp_m[m -  1] or y < 1000: raise ValueError

        except ValueError:
            print("Invalid DOB: {}".format(":".join(dob)))
            return -1

        age = self.calc_age((d, m, y))

        if age == -1:
            print("Invalid DoB. DoB must be valid and cannot be current or future date: {}".format(dob))
            return -1

        return self.get_earth_years([age["y"], age["m"], age["d"], 0, 0, 0])

    ''' Converts age from years, months, weeks etc, to all earth years
        :param age: list of age values [year, month, week, day, minute, second]:
        :output total_years: age converted to years '''
    def get_earth_years(self, age):
        #convert age values to earth years
        #ind_conv = [yr, mn, wk, dy, mi, sc]
        ind_conv = [1, 12, 52.143, 365.25, 525960, 31557600]
        total_years = 0

        for i in range(len(ind_conv)):
            total_years += age[i] / ind_conv[i]

        return total_years

    '''Calculates age from dob
       :param dob: tuple (day, month, year)
       :output age: age calculated from dob'''
    def calc_age(self, dob):
        #NOTE: uses local date, so age will be incorrect if local date is not upto date
        #      counts current day towards age
        cur_date = datetime.now()
        cd, cm, cy = cur_date.day, cur_date.month, cur_date.year
        d, m, y = dob

        #changes 29th of feb to 28th so non leap years are counted
        d = 28 if m == 2 and d == 29 else d

        age = {"y": 0, "d": 0, "m": 0}

        #for whe dob occurs on last day of month
        last_day = 1 if d == self.months[m - 1] else 0

        #checks dob is not current date
        if dob == (cd, cm, cy): return -1

        if y == cur_date.year:
            age["y"] = 0
        elif y < cur_date.year:
            age["y"] = cy - y

            if cm < m or (cm == m and cd < d):
                age["y"] -= 1
        else:
            return -1

        if m == cm:
            if d == cm:
                age["m"] = 0
                age["d"] = 0
            elif d > cd:
                age["m"] = 0
                age["d"] = cd - d
            else:
                age["m"] = 11
                age["d"] = cd

                tmp = self.months[(cm - 1) - 1 if cm == 1 else 11] - d
                age["d"] += tmp if tmp > 0 else 0

        else:
            age["m"] = cm - m if m < cm else 12 - (d - cm)

            if (d == cd and not last_day) or (last_day and self.month[cm] == cd):
                age["d"] = 0

            elif (not last_day and d > cd) or (last_day and self.month[cm] != cd):
                age["m"] -= 1
                age["d"] = cd

                tmp = self.months[cm - 2 if cm == 1 else 11] - d
                age["d"] += tmp if tmp > 0 else 0

            else:
                age["d"] = d - cd

        return age

    ' Gets and validates users planet selection '
    def get_planets(self):
        #planet input
        print("\nAvailable Planets: {}\nTo enter multiple planets leave a space between each, e.g. Mars earth Pluto, names are not case sensitive".format(", ".join(self.planets)))
        p = input("\nPlanet Input (leave blank for all): ").strip()

        #all planets if none provided
        p = self.planets if not p else [i.lower().title() for i in p.split()]

        #verify planet input
        for i in p:
            if i not in self.planets:
                print("\n[-] Contains Invalid Planet/s: {}".format(", ".join(p)))
                print("Please ensure your syntax is correct for multiple planets, i.e a space between each planet name.")
                return -1

        return p

    '''Calculates the age for each planet passed
       :param age: age in earth years
       :param planets: list of planets
       :output planet_ages: List of tuples containing age on each planet'''
    def calc_space_age(self, age, planet):
        planet_ages = {}

        for i in planet: planet_ages[i] = round(age / self.earth_years[i], 3)

        return planet_ages


    ''' Checks if a string is a numeric value
        :param s: string to check
        :output boolean: true if s is numeric else false'''
    def is_numeric(self, s):
        try:
            n = float(s)
            return 1
        except:
            return 0

if __name__ == '__main__':
    s = SpaceAgeCalc()

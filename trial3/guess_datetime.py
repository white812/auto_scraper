__author__ = 'yingbozhan'

from util import longestSubstringFinder, inline_xpath_decoration

GUESS_TIME = 1
GUESS_DATE = 2
GUESS_DATETIME = 3
GUESS_NONE = 0

def get_inline_xpath_for_datetime(xpath_from_code, xpath_to_code, dates, times, segment_path):
    if len(dates)!=2: return None, None
    xpath_dates = []
    xpath_times = []
    for date in dates:
        xpath_dates.append(date.replace(segment_path, '.'))

    if times is None:
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[1]))>0:
            return inline_xpath_decoration(xpath_dates[0]), inline_xpath_decoration(xpath_dates[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[0]))>0:
            return inline_xpath_decoration(xpath_dates[1]), inline_xpath_decoration(xpath_dates[0])
    else:
        if len(times)!=2: return None, None
        for time in times:
            xpath_times.append(time.replace(segment_path, '.'))
        xpath_times = list(xpath_times)
        date_from_str = ''
        time_from_str = ''
        date_to_str = ''
        time_to_str = ''

        if len(longestSubstringFinder(xpath_from_code, xpath_dates[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[1]))>0:
            date_from_str, date_to_str = inline_xpath_decoration(xpath_dates[0]), inline_xpath_decoration(xpath_dates[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[0]))>0:
            date_from_str, date_to_str = inline_xpath_decoration(xpath_dates[1]), inline_xpath_decoration(xpath_dates[0])

        if len(longestSubstringFinder(xpath_from_code, xpath_times[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_times[1]))>0:
            time_from_str, time_to_str = inline_xpath_decoration(xpath_times[0]), inline_xpath_decoration(xpath_times[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_times[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_times[0]))>0:
            time_from_str, time_to_str = inline_xpath_decoration(xpath_times[1]), inline_xpath_decoration(xpath_times[0])

        if time_from_str == '' or time_to_str =='' or date_from_str=='' or date_to_str=='':
            return None, None
        else:
            return date_from_str+'+'+time_from_str, date_to_str+'+'+time_to_str


def verify_date_time(xpath, root, namespace):
    #possible results: date only, time only, date time, None.
    values = set()
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        values.add(''.join(x for x in value if x.isalpha() or x.isdigit()))

    date_guess = 0
    time_guess = 0
    datetime_guess = 0

    for value in values:
        if len(value) < 4: return GUESS_NONE #not date/time

        #counting numeric/alpha
        alpha = 0
        numeric = 0
        for x in value:
            if x.isalpha(): alpha += 1
            else: numeric += 1

        if numeric == 0: return GUESS_NONE
        if alpha >=4: return GUESS_NONE

        if alpha<=2:
            if numeric >=8: datetime_guess +=1
            elif numeric>6: date_guess +=1
            else: time_guess+=1
        else:
            if numeric<=6: date_guess+=1
            else: datetime_guess +=1

    if max(date_guess, time_guess, datetime_guess)!=0:
        if time_guess == max(date_guess, time_guess, datetime_guess): return GUESS_TIME
        if date_guess == max(date_guess, time_guess, datetime_guess): return GUESS_DATE
        if datetime_guess == max(date_guess, time_guess, datetime_guess): return GUESS_DATETIME
    else:
        return GUESS_NONE


def get_xpath_for_datetime(xpath_for_datetimes, useful_path, root, segment_path, namespace):
    date_time_path_guess = [set(), set(), set(), set()]
    for xpath in xpath_for_datetimes:
        guess_value = verify_date_time(xpath, root, namespace)
        date_time_path_guess[guess_value].add(xpath)

    #todo complete time format guess
    #date time combined
    if len(date_time_path_guess[GUESS_DATETIME]) >= 2:
        return date_time_path_guess[GUESS_DATETIME], None
    #date time split
    elif len(date_time_path_guess[GUESS_DATE]>=2) and len(date_time_path_guess[GUESS_TIME])>=2:
        return date_time_path_guess[GUESS_DATE], date_time_path_guess[GUESS_TIME]
    else:
        #todo not able to guess a pair of time/date
        #try useful path
        date_time_path_guess = [set(), set(), set(), set()]
        for xpath in xpath_for_datetimes:
            guess_value = verify_date_time(xpath, root, namespace)
            date_time_path_guess[guess_value].add(xpath)
            if len(date_time_path_guess[GUESS_DATETIME]) >= 2:
                return date_time_path_guess[GUESS_DATETIME], None
            #date time split
            elif len(date_time_path_guess[GUESS_DATE]>=2) and len(date_time_path_guess[GUESS_TIME])>=2:
                return date_time_path_guess[GUESS_DATE], date_time_path_guess[GUESS_TIME]

        return None, None

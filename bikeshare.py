import time
import pandas as pd
import numpy as np

from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = { 'all': -1, 'january': 1, 'february': 2, 'march': 3, 'april': 4,
               'may': 5, 'june': 6, 'july': 7,'august': 8, 'september': 9,
               'october': 10, 'november': 11, 'december': 12}
DAY_DATA = { 'all': -1, 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
             'friday': 4, 'saturday': 5, 'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input('\nPlease enter the Name of a City you would like to explore:\n'\
                         'Chicago, New York City or Washington?\n').lower()
            city = CITY_DATA[city]
            break
        except:
            print('\nThere must be a mistake! Please make sure the spelling is correct.')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nPlease enter the Name of a Month you would like to explore:\n'\
                          'All, January, February, March, April, May, June, July, August, '\
                          'September, October, November or December?\n').lower()
            month = MONTH_DATA[month]
            break
        except:
            print('\nThere must be a mistake! Please make sure the spelling is correct.')
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nPlease enter the Name of a Day you would like to explore: \n'\
                        'All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').lower()
            day = DAY_DATA[day]
            break
        except:
            print('\nThere must be a mistake! Please make sure the spelling is correct.')
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # import csv
    df = pd.read_csv(city)

    # create datetimes
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # evaluate month, day if specified in get_filters()
    if month > -1:
        df = df[df['Start Time'].dt.month == month]
    if day > -1:
        df = df[df['Start Time'].dt.dayofweek == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['Start Time'].dt.month.value_counts()) > 1:
        month_values = df['Start Time'].dt.month.value_counts()
        month_common_num = month_values.index[0]
        month_common_count = month_values.iloc[0]
        for month, num in MONTH_DATA.items():
            if num == month_common_num:
                month_common_name = month
        print('\nThe most common month is:\n{}'.format(month_common_name.title()))
        print('\nIt has a total number of bike rentals:\n{}\n'.format(month_common_count))
        print(' '*15 + '* '*3)

    # display the most common day of week
    if len(df['Start Time'].dt.dayofweek.value_counts()) > 1:
        day_values = df['Start Time'].dt.dayofweek.value_counts()
        day_common_num = day_values.index[0]
        day_common_count = day_values.iloc[0]
        for day, num in DAY_DATA.items():
            if num == day_common_num:
                day_common_name = day
        print('\nThe most common day is: \n{}'.format(day_common_name.title()))
        print('\nIt has a total number of bike rentals: \n{}\n'.format(day_common_count))
        print(' '*15 + '* '*3)

    # display the most common start hour
    if len(df['Start Time'].dt.hour.value_counts()) > 0:
        hour_values = df['Start Time'].dt.hour.value_counts()
        hour_common = hour_values.index[0]
        hour_common_count = hour_values.iloc[0]
        hour_common = rewrite_time(hour_common) # helperfunction
        print('\nThe most common start hour is: \n{}'.format(hour_common))
        print('\nIt has a total number of bike rentals: \n{}\n'.format(hour_common_count))
    else:
        print('\nYour query has no result!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if (
        len(df['Start Station'].value_counts()) > 0 and
        len(df['End Station'].value_counts()) > 0
        ):
        # display most commonly used start station
        start_station_values = df['Start Station'].value_counts()
        start_station_common = start_station_values.index[0]
        start_station_common_count = start_station_values.iloc[0]
        print('\nThe most common Start Station is at:\n{}'.format(start_station_common))
        print('\nThe total number of Trips who started here is:\n{}\n'.format(start_station_common_count))
        print(' '*15 + '* '*3)

        # display most commonly used end station
        end_station_values = df['End Station'].value_counts()
        end_station_common = end_station_values.index[0]
        end_station_common_count = end_station_values.iloc[0]
        print('\nThe most common End Station is at:\n{}'.format(end_station_common))
        print('\nThe total number of Trips who ended here is:\n{}\n'.format(end_station_common_count))
        print(' '*15 + '* '*3)

        # display most frequent combination of start station and end station trip
        start_end_station = 'from \'' + df['Start Station'] + '\'\nto   \'' + df['End Station'] + '\''
        start_end_station_values = start_end_station.value_counts()
        start_end_station_common = start_end_station_values.index[0]
        start_end_station_common_count = start_end_station_values.iloc[0]
        print('\nThe most common combination of start to end station is:\n{}'.format(start_end_station_common))
        print('\nThe total number of Trips with that combination ist:\n{}\n'.format(start_end_station_common_count))
    else:
        print('\nYour query has no result!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if (
        df['Trip Duration'].sum() > 0 and
        df['Trip Duration'].mean() > 0
        ):
        # display total travel time
        duration_total = df['Trip Duration'].sum()
        duration_total_dayformat = str(timedelta(seconds=int(duration_total)))
        print('\nThe total travel time is:\n{}\n'.format(duration_total_dayformat))
        print(' '*15 + '* '*3)

        # display mean travel time
        duration_mean = df['Trip Duration'].mean()
        duration_mean_dayformat = str(timedelta(seconds=int(duration_mean)))
        print('\nThe mean travel time is:\n{}\n'.format(duration_mean_dayformat))
    else:
        print('\nYour query has no result!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    if len(df['User Type'].value_counts()) > 0:
        user_types = df['User Type'].fillna('Unclassified')
        user_type_values = user_types.value_counts()
        for i in range(0, len(user_type_values)):
            user, number = user_type_values.index[i], user_type_values.iloc[i]
            print('\nThe user type \'{}\' has a total number of:\n{}'.format(user, number))
        print('\n' + ' '*15 + '* '*3)
    else:
        print('\nYour query has no result!\n')

    try:
        if (
            len(df['Gender'].value_counts()) > 0 and
            len(df['Birth Year'].value_counts()) > 0
            ):
            # display counts of gender
            gender_values = df['Gender'].value_counts()
            for i in range(0, len(gender_values)):
                gender, number = gender_values.index[i], gender_values.iloc[i]
                print('\nThe gender \'{}\' has a total number of:\n{}'.format(gender, number))
            print('\n' + ' '*15 + '* '*3)

            # display earliest, most recent, and most common year of birth
            birth_year_values = df['Birth Year'].value_counts()
            print('\nThe most common year of birth is:\n{}'.format(int(birth_year_values.index[0])))
            print('\nThe most recent year of birth is:\n{}'.format(int(birth_year_values.index.max())))
            print('\nThe earliest year of birth is:\n{}'.format(int(birth_year_values.index.min())))
    except:
        pass

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, count=0):
    """ Displays raw data of the csv in five steps """

    while df[df.columns[0]].iloc[0:].count() >= count+5:
        see_data = input('\nWould you like to continue seeing individual trip data? Enter yes or no.\n')
        if see_data.lower() == 'yes':
            for i in range(5):
                print('\n\nTrip Data {}:\n'.format(count+i+1))
                for j in range(len(df.columns)):
                    actual_column = df.columns[j]
                    actual_row_value = df[actual_column].iloc[i]
                    print('\'{}\': {}'.format(actual_column, actual_row_value))
            count += 5
        else:
            break


def rewrite_time(hour):
    """
    Helperfunction that converts an 24 hour time into a 12 hour time

    Args:
        (int) hour - number between 0 and 24, otherwise returns the input

    Returns:
        (str) hour - string with the converted time with 'AM/PM' appended
    """

    if hour in {0,24}:
        hour = '12 AM'
    elif 0 < hour < 12:
        hour = str(hour) + ' AM'
    elif hour == 12:
        hour = '12 PM'
    elif 12 < hour < 24:
        hour = hour - 12
        hour = str(hour) + ' PM'
    return hour


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

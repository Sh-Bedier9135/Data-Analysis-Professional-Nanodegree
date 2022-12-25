# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 14:30:27 2020

@author: Shady
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city(chicago, new york city or washington)?')
    while True: 
        city =input().lower()
        if city in ['chicago','new york city','washington']:
            break
        else:
            print("Sorry, Enter valid city")

    # get user input for month (all, january, february, ... , june)
    print('Which month(january,february,march,april,may,june,all)?')
    while True: 
        month =input().lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june','all']:
            break
        else:
            print("Sorry,Enter valid month")  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Which day(sunday,monday,tuesday,wednesday,thursday,friday,saturday,all)?')
    while True: 
        day =input().lower()
        if day in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
            break
        else:
            print("Sorry, Enter valid day")

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Day Of Week:', popular_day_of_week)

    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    MC_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', MC_start_station)

    # display most commonly used end station
    MC_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', MC_end_station)

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    MF_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', MF_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()

    print('Total Travel Time:', tot_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print()
    types_of_users = df.groupby('User Type',as_index=False).count()
    print('Data has {} types of users:'.format(len(types_of_users)))
    for i in range(len(types_of_users)):
        print('{}s - {}'.format(types_of_users['User Type'][i], types_of_users['Start Time'][i]))

    # TO DO: Display counts of gender
    print()
    if 'Gender' not in df:
        print(' Gender data not avilable for this city')
    else:
        gender_of_users = df.groupby('Gender',as_index=False).count()
        print('Genders of users distributed in the data as:')
        for i in range(len(gender_of_users)):
            print('{}s - {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))
        print('Gender data for {} users is not available.'.format(len(df)-gender_of_users['Start Time'][0]-gender_of_users['Start Time'][1]))
    print()
    # TO DO: Display earliest, most recent, and most common year of birth
    print('Birth Year Stats:')
    if 'Birth Year' not in df:
        print('Birth year data not avilable for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    display_rows = input('Do you want to see raw data? yes/no ').lower()
    print()
    if display_rows=='yes':
        display_rows=True
    elif display_rows=='no':
        display_rows=False
    else:
        print('Sorry,Enter valid answer ')
        display_data(df)
        return

    if display_rows:
        while 1:
            for i in range(5):
                print(df.iloc[i])
                print()
            display_rows = input('display another five? yes/no ').lower()
            if display_rows=='yes' :
                continue
            elif display_rows=='no':
                break
            else:
                print('Sorry,Enter valid answer ')
                return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

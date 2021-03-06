import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze, or "all" to apply no month filter
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    if city != 'All Cities':
        df = pd.read_csv(CITY_DATA[city])
    else:
        df = pd.DataFrame()
        for key in CITY_DATA:
            df = df.append(pd.read_csv(CITY_DATA[key]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All Months':      
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'All Days':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    print(df['day_of_week'].unique())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        (dict) time_stats_dict - popular month/day of week/hour statistics
    """
    popular_month = df['month'].mode()[0]

    popular_day = df['day_of_week'].mode()[0]

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    time_stats_dict = {
        'popular_month':popular_month, 
        'popular_day':popular_day, 
        'popular_hour':popular_hour
        }
    return time_stats_dict


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

        Args:
        (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        (dict) station_stats_dict - popular start station/ end station/ route statistics
    """
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    
    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ';' + df['End Station']
    popular_route = df['route'].mode()[0]
    route_from = popular_route.split(';')[0]
    route_end = popular_route.split(';')[1]

    station_stats_dict = {
        'popular_start_station': popular_start_station, 
        'popular_end_station': popular_end_station, 
        'route_from': route_from,
        'route_end': route_end
    }
    return station_stats_dict


def convert_to_d_h_m_s(seconds):
    """Return the tuple of days, hours, minutes and seconds.
    The original function can be found in:
    https://codereview.stackexchange.com/questions/120577/seconds-days-hours-minutes-and-seconds
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return days, hours, minutes, seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (dataframe) df - Pandas DataFrame containing city data filtered by month and day
        df['Trip Duration']: in seconds
    Returns:
        (dict) trip_stats_dict - total/average travel time statistics
    """
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_days, total_hours, total_mins, total_secs = convert_to_d_h_m_s(total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_days, mean_hours, mean_mins, mean_secs = convert_to_d_h_m_s(mean_travel_time)

    trip_stats_dict = {
        'total_days': int(total_days),
        'total_hours': int(total_hours),
        'total_mins': int(total_mins),
        'total_secs': int(total_secs),
        'mean_mins': int(mean_mins),
        'mean_secs': int(mean_secs)
    }
    return trip_stats_dict


def user_stats(df, check):
    """Displays statistics on bikeshare users."""

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    if check:
    # Display counts of gender
        user_gender = df['Gender'].value_counts()
        
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        popular_birth_year = df['Birth Year'].mode()[0]
    
        user_stats_dict = {
            'subscribers': user_type[0], 
            'customers':user_type[1],
            'male': user_gender[0],
            'female': user_gender[1], 
            'earliest_birth_year': int(earliest_birth_year), 
            'most_recent_birth_year': int(most_recent_birth_year), 
            'popular_birth_year': int(popular_birth_year)
        }
    else:
            user_stats_dict = {
            'subscribers': user_type[0], 
            'customers':user_type[1], 
            'male': 'N.A.', 
            'female': 'N.A.', 
            'user_gender': 'N.A.', 
            'earliest_birth_year': 'N.A.', 
            'most_recent_birth_year': 'N.A.', 
            'popular_birth_year': 'N.A.'
            }
        
    return user_stats_dict


def stats_calculator(city, month, day):
    start_time = time.time()

    df = load_data(city, month, day)
    time_stats_dict = time_stats(df)
    station_stats_dict = station_stats(df)
    trip_stats_dict = trip_duration_stats(df)

    if city == "Washington":
        user_stats_dict = user_stats(df, False)
    else:
        user_stats_dict = user_stats(df, True)

    time_delta = time.time() - start_time

    stats_result_dict = {
        **time_stats_dict, 
        **station_stats_dict,
        **trip_stats_dict,
        **user_stats_dict,
        'time_delta':time_delta}
    
    print(stats_result_dict)
    return stats_result_dict


if __name__ == "__main__":
	stats_calculator('new york city','june','monday')

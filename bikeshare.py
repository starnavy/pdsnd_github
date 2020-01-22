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

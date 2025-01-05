import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Please enter the name of your city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from Chicago, New York City, or Washington.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Please enter a month (January, February, ..., June) or 'all' for no filter: ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid entry. Please choose a valid month (January to June) or 'all'.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Please enter a day of the week (Monday, Tuesday, ..., Sunday) or 'all' for no filter: ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid day. Please choose a valid day or 'all'.")

    print(f"\nFilters applied:\nCity: {city.title()}, Month: {month.title()}, Day: {day.title()}")
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_raw_data(df):
    """Displays 5 rows of raw data at a time based on user request."""
    print("\nRaw data is available to view.")
    row_index = 0
    while True:
        raw_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if raw_data == 'yes':
            print(df.iloc[row_index: row_index + 5])
            row_index += 5
            if row_index >= len(df):
                print("No more data to display.")
                break
        elif raw_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"The most common month is: {months[most_common_month - 1]}")

    most_common_day = df['day_of_week'].mode()[0].title()
    print(f"The most common day of the week is: {most_common_day}")

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {most_common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    df['trip_combination'] = df['Start Station'] + " -> " + df['End Station']
    most_common_trip = df['trip_combination'].mode()[0]
    print(f"The most frequent combination of trips is: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time / 3600
    print(f"The total travel time is: {total_travel_time} seconds ({total_travel_time_hours:.2f} hours)")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time:.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of user types:")
        print(user_types)
    else:
        print("User Type data is not available in this dataset.")

    if 'Gender' in df.columns:
        if df['Gender'].isnull().all():
            print("Gender column is present but contains no data.")
        else:
            df['Gender'] = df['Gender'].fillna('Unknown')
            gender_counts = df['Gender'].value_counts()
            print("\nCounts of gender:")
            print(gender_counts)
    else:
        print("Gender data is not available in this dataset.")

    if 'Birth Year' in df.columns:
        if df['Birth Year'].isnull().all():
            print("Birth Year column is present but contains no data.")
        else:
            earliest_birth_year = int(df['Birth Year'].min())
            most_recent_birth_year = int(df['Birth Year'].max())
            most_common_birth_year = int(df['Birth Year'].mode()[0])
            print("\nBirth Year Stats:")
            print(f"Earliest birth year: {earliest_birth_year}")
            print(f"Most recent birth year: {most_recent_birth_year}")
            print(f"Most common birth year: {most_common_birth_year}")
    else:
        print("Birth Year data is not available in this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
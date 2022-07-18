# %%
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
    while True:
        try:
            city = str(input("Please enter the city name: ")).lower()
        except ValueError:
            print("That's not a valid city name.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Please enter the month: ")).lower()
        except ValueError:
            print("That's not a valid month.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Please enter the day of week: ")).lower()
        except ValueError:
            print("That's not a valid day of week.")
            continue
        else:
            break

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
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    if month not in valid_months:
        print("Bad month provided.")
        exit()
    if day not in valid_days:
        print("Bad day provided")
        exit()
    try:
        full_df = pd.read_csv(CITY_DATA[city])
    except:
        print("Bad city provided.")
        exit()
    full_df['day_of_week'] = pd.to_datetime(full_df['Start Time']).dt.day_name().str.lower()
    full_df['month'] = pd.to_datetime(full_df['Start Time']).dt.month_name().str.lower()
    full_df['start_hour'] = pd.to_datetime(full_df['Start Time']).dt.hour
    if (month == "all") & (day == "all"):
        df = full_df
    elif month == 'all':
        df = full_df[full_df['day_of_week'] == day]
    elif day == 'all':
        df = full_df[full_df['month'] == month]
    else:
        df = full_df[(full_df['day_of_week'] == day) & (full_df['month'] == month)]
    return df
# %%

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel, inclding:
        - Most common month
        - Most common day of week
        - Most common start hour
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"The most common month in the data is {df['month'].mode()[0]}")


    # display the most common day of week
    print(f"The most common day of week in the data is {df['day_of_week'].mode()[0]}")

    # display the most common start hour
    print(f"The most common start hour in the data is {df['start_hour'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# %%
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip including:
        - Most common start station
        - Most common end station
        - Most  common combination of start/end station
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most common start station in the data is {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"The most common end station in the data is {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    start_stop = df['Start Station'] + "|" + df['End Station']
    most_common_trip = start_stop.mode()[0]
    most_common_trip_start = most_common_trip.split("|")[0]
    most_common_trip_end = most_common_trip.split("|")[1]
    print(f"The most frequent combination of start station and end station is {most_common_trip_start} to {most_common_trip_end}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# %%
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    print(f"Total travel time is {df['Travel Time'].sum()}")

    # display mean travel time
    print(f"Mean travel time is {df['Travel Time'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types:\n {df['User Type'].value_counts()}")

    # Display counts of gender
    try:
        print(f"Counts of gender:\n {df['Gender'].value_counts()}")
    except KeyError:
        print('There is no gender data here')

    # Display earliest, most recent, and most common year of birth
    try:
        print(f"The earliest year of birth is {int(df['Birth Year'].min())}")
        print(f"The most recent year of birth is {int(df['Birth Year'].max())}")
        print(f"The most common year of birth is {int(df['Birth Year'].mode()[0])}")
    except KeyError:
        print("There is no Birth Year data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """Displays 5 rows of the raw dataframe and asks if user wants 5 more. Ends at end of data or if user doesn't input 'yes'"""
    while True:
        try:
            answer = str(input(f"There are {len(df)} rows of raw data. Would you like to see the raw data 5 lines at a time yes/no?")).lower()
        except ValueError:
            print("That is not a valid answer.")
            continue
        else:
            break
    if answer == 'no':
        exit()
    elif answer == 'yes':
        line = 0
        while answer == 'yes':
            total_lines = len(df)
            if total_lines - line < 5:
                print(df.iloc[line:])
                print("end of data")
                break
            else:
                print(df.iloc[line:line+5])
                line += 5
                while True:
                    try:
                        answer = str(input("Would you like to see 5 more lines yes/no?")).lower()
                    except ValueError:
                        print("That is not a valid answer.")
                        continue
                    else:
                        break
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

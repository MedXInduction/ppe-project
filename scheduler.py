import os

import geocoder
import pandas as pd
import requests

import mixpanel as mp

MIXPANEL_API_KEY = os.environ.get('MIXPANEL_API_KEY')
MIXPANEL_API_SECRET = os.environ.get('MIXPANEL_API_SECRET')
keys = (MIXPANEL_API_KEY, MIXPANEL_API_SECRET)

DATA_LOCATION = './data/ppe-responses.csv'
HOSPITALS_LOCATION = './data/hospital_locations.csv'
FINAL_LOCATION = './data/ppe-merged-responses.csv'
START_DATE = '22 April, 2020'
REFRESH_EVENTS = False
REFRESH_LOCATIONS = False


def geocode_hospital_list(dataframe):
    """
    Take in a dataframe exported from Mixpanel which must have a non-index column called 'hospital'
    This will typically be a time series of events each of which has an associated hospital name

    Use Google Places API to try to locate lat, long and address of each item
    Finally saves the final data frame locally and returns it

    Note: Google API key must be present in env variable
    TODO save the data frame remotely (S3/DigitalOcean Space)
    """
    hospital_df = pd.DataFrame(dataframe['hospital'].value_counts)
    hospital_df["lat"] = ""
    hospital_df["lon"] = ""
    hospital_df["location"] = ""
    hospital_df["address"] = ""

    with requests.Session() as session:
        for x in range(len(hospital_df)):
            query_submission = hospital_df.index[x] + ', UK'
            response = geocoder.google(query_submission, session=session)
            hospital_df['location'][x] = response.latlng
            hospital_df['address'][x] = response.address
            hospital_df['lat'][x] = hospital_df['location'][x][0]
            hospital_df['lon'][x] = hospital_df['location'][x][1]

    hospital_df.to_csv(HOSPITALS_LOCATION)
    return hospital_df


def get_mixpanel_events(event_names='ppe-survey-1', start_date=START_DATE):
    """Get mixpanel events

    Keyword arguments
    @param event_names - can be string or array of strings representing events of interest (default 'ppe-survey-1')
    @param start_date -  date to start collection from (default 22/04/22)

    Uses the Mixpanel class to remotely retrieve one one event of interest from a certain date
    Saves the data locally and return the data frame

    TODO save the data frame remotely (S3/DigitalOcean Space)
    """
    remote_df = mp.read_events(
        keys,
        events=event_names,
        start=start_date,
        exclude_mp=False,
        columns=['time', 'mp_country_code', 'hospital', 'sufficient-supply', 'distinct_id']
    )

    remote_df = tidy_data(remote_df)
    remote_df.to_csv(DATA_LOCATION)
    return remote_df


def tidy_data(dataframe):
    """
    Tidy remote or locally restored data
    Filters by GB only, removes first 6 rows
    """
    tidied_df = dataframe.sort_values('time', ascending=True)
    tidied_df = tidied_df[tidied_df["mp_country_code"] == 'GB'][6:]
    tidied_df['year'] = pd.DatetimeIndex(tidied_df['time']).year
    tidied_df['month'] = pd.DatetimeIndex(tidied_df['time']).month
    tidied_df['day'] = pd.DatetimeIndex(tidied_df['time']).day
    tidied_df['hour'] = pd.DatetimeIndex(tidied_df['time']).hour
    tidied_df.set_index('time', inplace=True)

    return tidied_df


def get_local():
    """
    Take local events csv and turns return data frame
    """

    local_df = pd.read_csv(DATA_LOCATION,
                           index_col='hospital',
                           parse_dates=['time']
                           )

    return tidy_data(local_df)


def main():
    """
    Retrieves and formats event data and merges it with hospital location data resulting in located data that can be
    safely mapped.

    1. Get remote or local copy of survey results
    2. Get unique hospitals
    3. Use Google Places API to get lat, long info
    4. Merge the locations back into the events ready for plotting
    5. Save to csv for consumption by app.py
    """

    if REFRESH_EVENTS:
        local_df = get_mixpanel_events('ppe-survey-1', START_DATE)
    else:
        local_df = get_local()

    if REFRESH_LOCATIONS:
        geocoded_hospitals_df = geocode_hospital_list(local_df)
    else:
        geocoded_hospitals_df = pd.read_csv(HOSPITALS_LOCATION, index_col='address')

    # inner merge between the tables
    merged_df = pd.merge(left=local_df, how='left', right=geocoded_hospitals_df, left_on='hospital',
                         right_on='hospital')
    merged_df.set_index('time', inplace=True)

    # save the merged data back to a csv
    merged_df.to_csv(FINAL_LOCATION)


if __name__ == "__main__":
    main()

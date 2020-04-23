import os

import geocoder
import pandas as pd
import requests
import streamlit as st

import mixpanel as mp

# CONSTANTS
MIXPANEL_API_KEY = os.environ.get('MIXPANEL_API_KEY')
MIXPANEL_API_SECRET = os.environ.get('MIXPANEL_API_SECRET')
keys = (MIXPANEL_API_KEY, MIXPANEL_API_SECRET)
DATA_LOCATION = './data/2304-ppe-survey.csv'
HOSPITALS_LOCATION = './data/hospital_locations.csv'
START_DATE = '22/04/2020'
FORCE_REFRESH = True
TEMP_CSV = '2304-ppe-survey.csv'


def geocode_hospital_list(dataframe):
    """
    Take in a dataframe exported from Mixpanel which must have a column called 'hospital'
    This will typically be a time series of events each of which has an associated hospital name

    Use Google Places API to try to locate lat, long and address of each item
    Finally saves the final data frame locally and returns it
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


def get_remote(event_names, start_date):
    """
    @param event_names - can be string or array of strings representing events of interest
    @param start_date -  date to start collection from

    Uses the Mixpanel class to remotely retrieve one one event of interest from a certain date
    Saves the data locally and return the data frame

    TODO save the data frame remotely (S3/DigitalOcean Space)
    """
    start_date = START_DATE
    remote_df = mp.read_events(
        keys,
        events=event_names,
        start=start_date,
        exclude_mp=False
    )

    remote_df.set_index('time', inplace=True)
    remote_df.to_csv(DATA_LOCATION)
    return remote_df


def main():
    """
    Retrieves and formats event data and merges it with hospital location data resulting in located data that can be
    safely mapped.
    """
    # if os.path.isfile(DATA_LOCATION) & FORCE_REFRESH != True:
    #     local_df = pd.read_csv(DATA_LOCATION,
    #                            index_col='hospital',
    #                            usecols=['time', 'mp_country_code', '$city', '$region', 'hospital', 'sufficient-supply'],
    #                            parse_dates=['time']
    #                            )
    # else:
    local_df = get_remote('ppe-survey-1', START_DATE)
    gb_df = local_df
    st.dataframe(gb_df)
    # gb_df = local_df[local_df["mp_country_code"] == 'GB']
    # total = data.isnull().sum().sort_values(ascending=False)
    # percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)
    # missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Missing Percent'])
    # missing_data['Missing Percent'] = missing_data['Missing Percent'].apply(lambda x: x * 100)
    # missing_data.loc[missing_data['Missing Percent'] > 10][:10]
    # st.write(gb_df)

    # location_df = pd.read_csv(HOSPITALS_LOCATION, index_col='address')
    # st.write(location_df)
    #
    # merged_inner = pd.merge(left=gb_df, how='left', right=location_df, left_on='hospital', right_on='hospital')
    # merged_inner.set_index('time', inplace=True)
    # st.write(merged_inner)


if __name__ == "__main__":
    main()

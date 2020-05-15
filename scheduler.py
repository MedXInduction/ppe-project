import os
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

def main():

    remote_df = mp.read_events(
        keys,
        events='ppe-survey-1',
        start=START_DATE,
        exclude_mp=False,
        columns=['time', 'mp_country_code', 'hospital', 'sufficient-supply', 'distinct_id']
    )
    remote_df.to_csv(DATA_LOCATION)

    local_df = pd.read_csv(DATA_LOCATION,
                           index_col='distinct_id',
                           parse_dates=['time']
                           )

    gb_df = local_df[local_df["mp_country_code"] == 'GB'][6:]
    gb_df['year'] = pd.DatetimeIndex(gb_df['time']).year
    gb_df['month'] = pd.DatetimeIndex(gb_df['time']).month
    gb_df['day'] = pd.DatetimeIndex(gb_df['time']).day
    gb_df['hour'] = pd.DatetimeIndex(gb_df['time']).hour
    gb_df['day_month'] = pd.DatetimeIndex(gb_df['time']).to_period('D')

    geocoded_hospitals_df = pd.read_csv(HOSPITALS_LOCATION, index_col='address')
    merged_df = pd.merge(left=gb_df, how='left', right=geocoded_hospitals_df, left_on='hospital',
                         right_on='hospital')
    merged_df.set_index('time', inplace=True)
    merged_df.dropna(subset=['lat', 'lon'], inplace=True)

    merged_df.to_csv(FINAL_LOCATION)


if __name__ == "__main__":
    main()

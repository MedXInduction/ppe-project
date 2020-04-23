import time
import pandas as pd 
import scheduler
import mixpanel as mp
import streamlit as st
import geocoder
import os
import requests

MIXPANEL_API_KEY = os.environ.get('MIXPANEL_API_KEY')
MIXPANEL_API_SECRET = os.environ.get('MIXPANEL_API_SECRET')
keys = (MIXPANEL_API_KEY, MIXPANEL_API_SECRET)

@st.cache(suppress_st_warning=False)
def get_remote():
	start_date = '21/04/2020'
	remote_df = mp.read_events(
		keys,
		events='Directory',
		start=start_date,
		exclude_mp=False
	)
	remote_df.to_csv('./data/directory-events.csv')
	return remote_df

def main():
	# response = get_remote()
	local_df = pd.read_csv('./data/directory-events.csv', 
		index_col=0,
		usecols=['time', 'mp_country_code', '$city', '$region', 'hospital'],
		parse_dates=['time']
	)

	gb_df = local_df[local_df["mp_country_code"] == 'GB']
	st.write(gb_df)

	location_df = pd.read_csv('./data/hospital_locations.csv', index_col='address')

	st.write(location_df)

	merged_inner = pd.merge(left=gb_df, how='left', right=location_df, left_on='hospital', right_on='hospital')
	
	merged_inner.set_index('time', inplace=True)
	st.write(merged_inner)



	# get out all the unique hospitals
	# hospital_df = pd.DataFrame(gb_df['hospital'].value_counts())
	
	# create new data fields
	# hospital_df["lat"] = ""
	# hospital_df["lon"] = ""
	# hospital_df["location"] = ""
	# hospital_df["address"] = ""

	# use a session to loop through dataframe and get as much info as possible
	# using geocoder
	# with requests.Session() as session:	
	# 	for x in range(len(hospital_df)):
	# 		query_submission = hospital_df.index[x] + ', UK'
	# 		response = geocoder.google(query_submission, session=session)
	# 		hospital_df['location'][x] = response.latlng
	# 		hospital_df['address'][x] = response.address
	# 		hospital_df['lat'][x] = hospital_df['location'][x][0]
	# 		hospital_df['lon'][x] = hospital_df['location'][x][1]
			
	# let's see what we end up with
	# st.write(hospital_df)
	# hospital_df.to_csv('./data/hospital_locations.csv')

	

if __name__ == "__main__":
  main()
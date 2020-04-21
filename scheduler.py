import time
import pandas as pd 
import schedule
timestr = time.strftime("%Y%m%d-%H%M%S")

confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
recovered_cases_url ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
death_cases_url ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def get_n_melt_data(data_url,case_type):
    df = pd.read_csv(data_url)
    melted_df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
    melted_df.rename(columns={"variable":"Date","value":case_type},inplace=True)
    return melted_df

def merge_data(confirm_df,recovered_df,deaths_df):
	new_df = confirm_df.join(recovered_df['Recovered']).join(deaths_df['Deaths'])
	return new_df

def fetch_data():
	"""Fetch and Prep"""
	confirm_df = get_n_melt_data(confirmed_cases_url,"Confirmed")
	recovered_df = get_n_melt_data(recovered_cases_url,"Recovered")
	deaths_df = get_n_melt_data(death_cases_url,"Deaths")
	print("Merging Data")
	final_df = merge_data(confirm_df,recovered_df,deaths_df)
	print("Preview Data")
	print(final_df.tail(5))
	filename = "covid19_merged_dataset_updated_{}.csv".format(timestr)
	print("Saving Dataset as {}".format(filename))
	final_df.to_csv(("./data/" + filename),index='False')
	print("Finished")

fetch_data()

# schedule.every().day.at("11:59").do(fetch_data)
# while True:
#    schedule.run_pending()
#    time.sleep(1)
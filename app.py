import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import seaborn as sns

sns.set(style="darkgrid")

MERGED_DATA_LOCATION = './data/ppe-merged-responses.csv'
MAPBOX_API_KEY = os.environ.get('MAPBOX_TOKEN')
LAST_UPDATE = '4th May, 0130'


@st.cache()
def load_data():
    return pd.read_csv(MERGED_DATA_LOCATION,
                       index_col='time',
                       parse_dates=['time'])


def render_sidebar():
    st.sidebar.subheader("Contact")
    st.sidebar.warning(
        """
        This is an [open source project](https://github.com/MedXInduction/ppe-project) and you are very welcome to
        contribute comments, questions, and further analysis.
        
        Anonymised data is contained within the code repository.

        For queries about this project please contact the project lead, Dr Ed Wallitt via ed.w@inductionhealthcare.com
        """
    )

    st.sidebar.subheader("Other PPE Projects")
    st.sidebar.markdown(
        """
            Be sure to check these great project as well:
        
            * [Frontline Map](http://frontline.live/)
            * [The Nead](https://www.thenead.co.uk/)
            * [Donate your PPE](https://www.donateyourppe.uk/)
        """
    )


def render_content_header():
    st.title("The Sentiment of UK Clinicians on Personal Protective Equipment Supply in April and May 2020 ")
    st.markdown("""*Dr Ed Wallitt (Chief Product Officer at Induction Healthcare Group*""")
    st.subheader("Last updated: " + LAST_UPDATE)
    st.markdown(
        """
        An open data project by the team at [Induction Healthcare](https://induction-app.com) and [
        Microguide](http://www.microguide.eu/) examining regional clinician sentiment around current supply of PPE 
        
        One of the best ways of tracking PPE availability is daily measuring of PPE sentiment - how do they and 
        their team feel about the supply of PPE that is available to them?
        
        Since the 22nd April we have been asking a simple question to our 40,000 weekly users:
        
        """
    )

    st.info("Do you feel you and your team have enough PPE today?")


def render_how_it_works():
    st.header("How it works?")
    st.markdown(
        """
    Induction Healthcare provides over 150,000 Frontline Healthcare Professionals with the resources and tools 
        to support their work. 

    Personal Protective Equipment (PPE from now on) includes masks, gloves and other clothing that must be worn by 
    healthcare professionals working with infected patients. It is requirement for them to work safely and to protect 
    the workforce and their families ([What is PPE?](https://www.bbc.co.uk/news/health-52254745)) 

    Since the 22nd April we have started collecting and sharing anonymous daily contributions measuring regional 
    clinician PPE sentiment. 

    **NOTE: this data represents the personal feelings/sentiment of individual Frontline UK Clinicians about the 
    availability and accessibility of PPE within their team. It does not directly measure supply** 
    
    """
    )

    st.image("./static/images/device-preview.png",
             caption="Method of data collection",
             width=300)


def render_initial_analysis(data):
    st.header("UK PPE Supply Responses")
    st.subheader("Do you feel you and your team have enough PPE today?")
    scoped_data = data.copy(deep=True)
    st.info("n = " + str(len(scoped_data)))

    sufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == True]
    insufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == False]

    data = pd.DataFrame(
        np.array([[len(sufficient_supply_df)], [len(insufficient_supply_df)]]),
        columns=['Total Responses'],
        index=['Yes', 'No']
    )

    st.bar_chart(data, use_container_width=True)


# @st.cache(persist=True, suppress_st_warning=True)
def render_results_map(data):
    scoped_data = data.copy(deep=True)
    midpoint = (np.average(scoped_data["lat"]), np.average(scoped_data["lon"]))

    sufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == 1]
    insufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == 0]

    st.header("PPE Negative Sentiment Map")

    st.markdown(
        """
        This map shows areas in the UK where Frontline Healthcare Workers are reporting that they feel they do not have 
        sufficient access to PPE. The taller the spike, the more demand is being reported in that region.
        
        The data is cumulative since the 22nd April, however you can view daily data using the filter below.
    """)
    st.success("Number reporting insufficient PPE supply sentiment (N) = " + str(len(insufficient_supply_df)) + "  (Total: " + str(len(scoped_data)) + ")")

    if st.checkbox('Filter by day'):
        day_to_filter = st.date_input('Date')
        insufficient_supply_df = insufficient_supply_df[insufficient_supply_df.index.date == day_to_filter]
        st.subheader(f'PPE supply sentiment on {day_to_filter}')

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        mapbox_key=MAPBOX_API_KEY,
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 5.3,
            "pitch": 40,
            "bearing": -22.1,
            "elevation_scale": 6
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=insufficient_supply_df,
                get_position=["lon", "lat"],
                elevation_scale=60,
                pickable=True,
                extruded=True,
                coverage=0.8,
                auto_highlight=True,
                radius=1500
            )
        ],
    ))


def render_supply_over_time(data):
    copy = data.copy()
    by_daily_supply = copy.groupby(['day_month', 'sufficient-supply']).size().unstack().reset_index()
    by_daily_supply['total'] = (by_daily_supply[True]) + (by_daily_supply[False])
    by_daily_supply['proportion'] = (by_daily_supply[False] / by_daily_supply['total']) * 100

    st.subheader('Trend in PPE sentiment over time')

    st.info(f"Average number of clinicians reporting per day: {round(by_daily_supply['total'].mean())}")

    ax = sns.lineplot(x="day_month", y='proportion', data=by_daily_supply)
    ax.set(
        xlabel='',
        ylabel='Percentage Reporting Insufficient Supply',
        ylim=(0, 100),
        title='Daily Trend in % '
              'Clinicians '
              'reporting '
              'insufficient '
              'supply')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot()
def main():
    data = load_data()
    render_sidebar()
    render_content_header()
    render_initial_analysis(data)
    render_supply_over_time(data)
    render_results_map(data)
    render_how_it_works()


if __name__ == "__main__":
    main()

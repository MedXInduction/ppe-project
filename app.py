import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import seaborn as sns

sns.set(style="darkgrid")

MERGED_DATA_LOCATION = './data/ppe-merged-responses.csv'
MAPBOX_API_KEY = os.environ.get('MAPBOX_TOKEN')
LAST_UPDATE = '8th May, 1840'


@st.cache()
def load_data():
    return pd.read_csv(MERGED_DATA_LOCATION,
                       index_col='time',
                       parse_dates=['time'])


def render_sidebar():
    st.sidebar.header("About This Project")
    st.sidebar.warning(
        """
        This project is produced without any agenda, and the author(s) are not seeking to test any 
        null or non-null hypothesis through the collection and publication of this data. 
        
        All interpretation of the results belong to the group performing an analysis, not the author(s) of this paper or
         of Induction Healthcare Group PLC. 
        
        This is an [open source project](https://github.com/MedXInduction/ppe-project), and researchers are very welcome to
        contribute comments, questions, and further analysis. Anonymised data is available on [Github](https://github.com/MedXInduction/ppe-project).

        For queries about this project please contact the project lead, Dr Ed Wallitt via ed.w@inductionhealthcare.com
        """
    )

    st.sidebar.subheader("Software used")
    st.sidebar.markdown(
        """
        Data collected from users of the [Induction App](https://induction-app.com)
        
        Data analysis and presentation using:
        
        * [Streamlit](https://www.streamlit.io/)
        * [Exploratory](https://exploratory.io/)
        """
    )

    st.sidebar.subheader("Other PPE Projects")
    st.sidebar.markdown(
        """
            More interesting projects on UK PPE availability/sentiment
        
            * [Frontline Map](http://frontline.live/)
            * [The Nead](https://www.thenead.co.uk/)
            * [Donate your PPE](https://www.donateyourppe.uk/)
        """
    )


def render_content_header():
    st.title("The Sentiment of UK Clinicians on Personal Protective Equipment Supply in April and May 2020 ")
    st.markdown("""Author:""")
    st.markdown("""*Dr Ed Wallitt MBBS BSc - Chief Product Officer at Induction Healthcare Group PLC*""")
    st.subheader("Last updated: " + LAST_UPDATE)
    st.warning("NEW: A more detailed data exploration is now available at "
               "https://exploratory.io/dashboard/CNw7BmT9hR/Frontline-PPE-Supply-Sentiment-AgF3AlA5zg")
    st.markdown(
        """
        An open data project by the team at [Induction Healthcare](https://induction-app.com) and [
        Microguide](http://www.microguide.eu/) examining regional daily clinician sentiment around PPE supply 
        
        One of the best ways of tracking PPE availability is daily measuring of PPE sentiment - how do individual clinicians and 
        their team(s) feel about the supply of PPE that is available to them on any given day?
        
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

    **NOTE: this data represents the personal feelings or sentiment of individual Frontline UK Clinicians about the 
    availability and accessibility of PPE within their team. It does not directly measure supply.** 
    
    """
    )

    st.image("./static/images/device-preview.png",
             caption="Method of data collection",
             width=300)


def render_initial_analysis(data):
    st.header("UK PPE Supply and Availability Sentiment Responses")
    st.subheader("Do you feel you and your team have enough PPE today?")
    scoped_data = data.copy(deep=True)
    st.info("n = " + str(len(scoped_data)))

    #sufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == True]
    #insufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == False]

    #data = pd.DataFrame(
    #    np.array([[len(sufficient_supply_df)], [len(insufficient_supply_df)]]),
    #    columns=['Total Responses'],
    #    index=['Yes', 'No']
    #)

    # st.bar_chart(data, use_container_width=True)
    st.markdown(
        """
        <iframe src="https://exploratory.io/viz/CNw7BmT9hR/Total-PPE-Responses-moG6tLn4zy?embed=true" width="500" height="375" frameborder="0"></iframe>
        <hr />
        """
    , unsafe_allow_html=True)


# @st.cache(persist=True, suppress_st_warning=True)
def render_results_map(data):
    # scoped_data = data.copy(deep=True)
    # midpoint = (np.average(scoped_data["lat"]), np.average(scoped_data["lon"]))

    # sufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == 1]
    # insufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == 0]

    st.header("PPE Supply Sentiment Map")

    st.markdown(
        """
        In this map each dot shows a hospital site. The darker the color, the more negative the 
        sentiment around PPE supply is, the lighter the  color the more positive. The larger the dot the more responses we have received from that location i.e. the 
        more confidence we can have in the shade of color.

        NOTE: This data is cumulative, and shows total since collection started on the 22nd April. If you wish to 
        filter by day you can enter a date below.
        """
    )

    st.markdown(
        """
        <iframe src="https://exploratory.io/viz/CNw7BmT9hR/Heatmap-of-Negative-Sentment-ZKX4OQh3Nj?embed=true" width="800" height="600" frameborder="0"></iframe>
        """
    , unsafe_allow_html=True)


    # if st.checkbox('Filter by day'):
    #     day_to_filter = st.date_input('Date')
    #     insufficient_supply_df = insufficient_supply_df[insufficient_supply_df.index.date == day_to_filter]
    #     st.subheader(f'PPE supply sentiment on {day_to_filter}')

    # st.pydeck_chart(pdk.Deck(
    #     map_style="mapbox://styles/mapbox/light-v9",
    #     mapbox_key=MAPBOX_API_KEY,
    #     initial_view_state={
    #         "latitude": midpoint[0],
    #         "longitude": midpoint[1],
    #         "zoom": 5.3,
    #         "pitch": 40,
    #         "bearing": -22.1,
    #         "elevation_scale": 6
    #     },
    #     layers=[
    #         pdk.Layer(
    #             "HexagonLayer",
    #             data=insufficient_supply_df,
    #             get_position=["lon", "lat"],
    #             elevation_scale=60,
    #             pickable=True,
    #             extruded=True,
    #             coverage=0.8,
    #             auto_highlight=True,
    #             radius=1500
    #         )
    #     ],
    # ))


def render_supply_over_time(data):
    copy = data.copy()
    by_daily_supply = copy.groupby(['day_month', 'sufficient-supply']).size().unstack().reset_index()
    by_daily_supply['total'] = (by_daily_supply[True]) + (by_daily_supply[False])
    by_daily_supply['proportion-negative'] = (by_daily_supply[False] / by_daily_supply['total']) * 100
    by_daily_supply['proportion-positive'] = (by_daily_supply[True] / by_daily_supply['total']) * 100

    # st.info(f"Average number of clinicians reporting per day: {round(by_daily_supply['total'].mean())}")

    #st.subheader('Trend in PPE sentiment over time')
    st.markdown(
    """
        <iframe
        src = "https://exploratory.io/viz/CNw7BmT9hR/PPE-Response-Sentiment-Split-Wud7CIF5gl?embed=true"
        width = "800"
        height = "600"
        frameborder = "0" ></iframe>
    """, unsafe_allow_html=True
    )

    # ax = sns.lineplot(x="day_month", y='proportion-negative', data=by_daily_supply)
    # ax = sns.lineplot(x="day_month", y='proportion-positive', data=by_daily_supply)
    # ax.set(
    #     xlabel='22nd April to ' + LAST_UPDATE.split(',')[0],
    #     ylabel='Cumulative Average Sentiment',
    #     ylim=(0, 100),
    #     title='Clinicians '
    #           'reporting '
    #           'positive and negative PPE '
    #           'supply '
    #           'sentiment')
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    # st.pyplot()

    if st.checkbox('View raw data'):
        st.table(by_daily_supply)


def render_worst_performers():
    st.header('Locations of PPE Sentiment Descending')
    st.markdown(
        """
        This figure shows in ascending order the bottom 170 hospital were positive sentiment towards PPE supply is being reported.
        """
    )
    # st.image('./static/images/negative_sentiment_performers.png', caption='Cumulative % Positive PPE Sentiment by Hospital Descending (n = 170)', use_column_width=True)

    st.markdown(
        """
        <iframe src="https://exploratory.io/viz/CNw7BmT9hR/PPE-Supply-Sentiment-by-Hospital-QKu9dYd9al?embed=true" width="800" height="600" frameborder="0"></iframe>
        """
    , unsafe_allow_html=True)

def main():
    data = load_data()
    render_sidebar()
    render_content_header()
    render_initial_analysis(data)
    render_supply_over_time(data)
    render_results_map(data)
    render_worst_performers()

    render_how_it_works()


if __name__ == "__main__":
    main()

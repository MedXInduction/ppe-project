import os
import time

import altair as alt
import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st
from folium.plugins import FastMarkerCluster

import mixpanel as mp

DATA_LOCATION = './data/2304-ppe-survey.csv'


def render_sidebar():
    st.sidebar.title("About PPE UK Live")
    st.sidebar.markdown(
        """
    An open data project by the team at [Induction Healthcare](https://induction-app.com)
    """

    )

    st.sidebar.subheader("Contact")
    st.sidebar.info(
        "This is an [open source project](https://github.com/MedXInduction/ppe-project) and you are very welcome to "
        "contribute comments, questions, and further analysis. "

        "For questions, access to the data, or  help with this project please feel free to contact us via "
        "contact@induction-app.com. "

    )

    st.sidebar.subheader("PPE Projects")
    st.sidebar.markdown(
        """
            While we prepare to launch our data analysis please checkout these great PPE projects:
        
            * [Frontline Map](http://frontline.live/)
            * [The Need](https://www.thenead.co.uk/)
            * [Donate your PPE](https://www.donateyourppe.uk/)
        """
    )


def render_content_header():
    st.title("PPE UK Live")
    st.markdown(
        """A public service project by the team behind the [Induction App](https://induction-app.com) and [Microguide](http://www.microguide.eu/)""")


def render_how_it_works():
    st.header("How it works?")
    st.markdown(
        """
    Induction Healthcare provides over 150,000 frontline healthcare professionals with the resources and tools to support their work.

    *Personal Protective Equipment* (PPE from now on) includes masks, gloves and other clothing that must be worn by healthcare professionals working with infected patients. 
    It is requirement for them to work safely and to protect the workforce and their families ([What is PPE?](https://www.bbc.co.uk/news/health-52254745))

    From 22nd April we started collecting and sharing anonymous contributions about the real-time regional availability of PPE direct from users of the Induction app.

    **NOTE: this data represents the personal feelings of individual frontline clinicians about the availability of PPE within their team. It does not directly measure supply**
    """
    )

    st.image("./static/images/device-preview.png",
             caption="In-app data collection",
             width=300)


def render_initial_analysis():
    st.header("Non-regional responses")
    st.markdown(
        """
        While we continue to gather enough geographic data across the UK, we are happy to share our qualitative responses so far.
        
        The following represents data gathered from UK clinicians since 1500 on 22nd April, 2020.
        
        **Last updated: 23rd April, 1735**
        """
    )

    st.subheader("Do you feel you and your team have enough PPE today?")
    st.info("n = 895")

    # static for the moment as MP not showing most recent events
    data = pd.DataFrame(
        np.array([[660], [235]]),
        columns=['total'],
        index=['Yes', 'No']
    )

    st.bar_chart(data, use_container_width=True)


    # data = pd.read_csv(DATA_LOCATION,
    #                    index_col='hospital',
    #                    usecols=['time', 'hospital', 'sufficient-supply', 'mp_country_code'],
    #                    parse_dates=['time'])
    # gb_data = data[data["mp_country_code"] == 'GB']
    # st.dataframe(gb_data)




# def render_results_map():
#     local_df = pd.read_csv(
#         './data/directory-events.csv',
#         index_col=0,
#         usecols=['time', 'mp_country_code', '$city', '$region', 'hospital'],
#         parse_dates=['time']
#     )
#
#     gb_df = local_df[local_df["mp_country_code"] == 'GB']
#     location_df = pd.read_csv('./data/hospital_locations.csv', index_col='address')
#
#     data = pd.merge(left=gb_df, how='left', right=location_df, left_on='hospital', right_on='hospital')
#     data.set_index('time', inplace=True)
#     midpoint = (np.average(data["lat"]), np.average(data["lon"]))
#
#     st.write(pdk.Deck(
#         map_style="mapbox://styles/mapbox/light-v9",
#         initial_view_state={
#             "latitude": midpoint[0],
#             "longitude": midpoint[1],
#             "zoom": 6,
#             "pitch": 35,
#         },
#         layers=[
#             pdk.Layer(
#                 "HexagonLayer",
#                 data=location_df,
#                 get_position=["lon", "lat"],
#                 radius=2000,
#                 elevation_scale=300,
#                 elevation_range=[0, 700],
#                 pickable=True,
#                 extruded=True,
#             ),
#         ],
#     ))


def main():
    render_sidebar()
    render_content_header()
    render_initial_analysis()
    # render_results_map()
    render_how_it_works()


if __name__ == "__main__":
    main()

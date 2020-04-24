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

MERGED_DATA_LOCATION = './data/ppe-merged-responses.csv'


def load_data():
    return pd.read_csv(MERGED_DATA_LOCATION,
                       index_col='time',
                       parse_dates=['time'])


def render_sidebar():
    st.sidebar.title("About PPE UK Live")
    st.sidebar.markdown(
        """An open data project by the team at [Induction Healthcare](https://induction-app.com) examining regional 
        clinician sentiment around their supply of PPE """

    )

    st.sidebar.subheader("Contact")
    st.sidebar.info(
        "This is an [open source project](https://github.com/MedXInduction/ppe-project) and you are very welcome to "
        "contribute comments, questions, and further analysis. "

        "For questions, access to the data, or  help with this project please feel free to contact us via "
        "contact@induction-app.com."
    )

    st.sidebar.subheader("PPE Projects")
    st.sidebar.markdown(
        """
            While we prepare to launch our data analysis please checkout these great PPE projects:
        
            * [Frontline Map](http://frontline.live/)
            * [The Nead](https://www.thenead.co.uk/)
            * [Donate your PPE](https://www.donateyourppe.uk/)
        """
    )


def render_content_header():
    st.title("PPE UK Live")
    st.markdown(
        """A public service project by the team behind the [Induction App](https://induction-app.com) and [
        Microguide](http://www.microguide.eu/)""")


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


def render_initial_analysis(data):
    st.header("Analysis")
    st.markdown(
        """
        The following represents data gathered from UK clinicians since 1500 on 22nd April, 2020.
        
        **Last updated: 24th April, 1100**
        """
    )

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


def render_results_map(data):

    scoped_data = data.copy(deep=True)
    midpoint = (np.average(scoped_data["lat"]), np.average(scoped_data["lon"]))

    sufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == True]
    insufficient_supply_df = scoped_data[scoped_data['sufficient-supply'] == False]

    st.subheader("Regional Demand")

    st.markdown(
        """
        This map shows areas in the UK where frontline staff are reporting that they feel they do not have 
        sufficient PPE supply. The taller the spike, the more demand is being reported in that region.
        
        **Last updated: 24th April, 1100**
    """)

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 6,
            "pitch": 40,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=insufficient_supply_df,
                get_position=["lon", "lat"],
                elevation_scale=50,
                pickable=True,
                extruded=True,
                coverage=1
            ),
        ],
    ))


def main():
    data = load_data()
    render_sidebar()
    render_content_header()
    render_results_map(data)
    render_initial_analysis(data)
    render_how_it_works()


if __name__ == "__main__":
    main()

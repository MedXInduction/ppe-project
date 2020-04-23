import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import os
import mixpanel as mp
import time
import altair as alt

def render_sidebar():
    st.sidebar.title("About this project")
    st.sidebar.markdown(
    """
    An open data project by the team at [Induction Healthcare](https://induction-app.com)
    """
    )

    st.sidebar.subheader("Contact")
    st.sidebar.info(
    "This is an open source project and you are very welcome to **contribute comments, questions, and further analysis**"

    "For questions, access to our data, or to help with this project please feel free to contact us via contact@induction-app.com"

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


def main():
    render_sidebar()

    st.title("PPE UK Live - Launching on 23rd April, 2020")
    st.info("Data collection is now live and we shall report back soon!")
    st.subheader("A public service project by the team behind the [Induction App](https://induction-app.com) and [Microguide](http://www.microguide.eu/)")

    st.header("How it works?")
    st.markdown(
    """
    Induction Healthcare provides over 150,000 frontline healthcare professionals with the resources and tools to support their work.

    *Personal Protective Equipment* (PPE from now on) includes masks, gloves and other clothing that must be worn by healthcare professionals working with infected patients. 
    It is requirement for them to work safely and to protect the workforce and their families ([What is PPE?](https://www.bbc.co.uk/news/health-52254745))

    Starting today, 22nd April, We are collecting and sharing anonymous contributions about the real-time regional availability of PPE direct from users of our products.
    """
    )

    local_df = pd.read_csv('./data/directory-events.csv', 
		index_col=0,
		usecols=['time', 'mp_country_code', '$city', '$region', 'hospital'],
		parse_dates=['time']
	)
    gb_df = local_df[local_df["mp_country_code"] == 'GB']
    location_df = pd.read_csv('./data/hospital_locations.csv', index_col='address')
    
    data = pd.merge(left=gb_df, how='left', right=location_df, left_on='hospital', right_on='hospital')
    data.set_index('time', inplace=True)

    # hour = st.slider("Hour to look at", 0, 23)
    # data = data[data.index.hour == hour]

    # st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    midpoint = (np.average(data["lat"]), np.average(data["lon"]))

    st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 6,
        "pitch": 35,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=location_df,
            get_position=["lon", "lat"],
            radius=2000,
            elevation_scale=300,
            elevation_range=[0,700],
            pickable=True,
            extruded=True,
        ),
    ],
))


if __name__ == "__main__":
  main()
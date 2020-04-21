import streamlit as st
import mixpanel as mp
import time


def main():
  st.sidebar.title("About this project")
  st.sidebar.markdown(
  """
  An open data project by the team at [Induction Healthcare](https://induction-app.com)
  """
    
)

  st.sidebar.subheader("Contact")
  st.sidebar.info(
    "This is an open source project and you are very welcome to **contribute** comments, questions, and further analysis"
    
    "For questions, access to our data, or to help with this project please feel free to contact us via contact@induction-app.com"
    
  )

  st.sidebar.subheader("PPE Projects")
  st.sidebar.markdown(
  """
  While we prepare to launch our data analysis please checkout other great PPE projects:

  * [Frontline Map](http://frontline.live/)
  * [The Need](https://www.thenead.co.uk/)
  * [Donate your PPE](https://www.donateyourppe.uk/)
  """
  )


  st.title("PPE UK Live - Coming on 21st April, 2020")
  st.subheader("A public service project by the team behind the [Induction App](https://induction-app.com) and [Microguide](http://www.microguide.eu/)")

  st.header("How it works?")
  st.markdown(
    """
    Induction Healthcare provides over 150,000 frontline healthcare professionals with the resources and tools to support their work.

    *Personal Protective Equipment* (PPE from now on) includes masks, gloves and other clothing that must be worn by healthcare professionals working with infected patients. 
    It is requirement for them to work safely and to protect the workforce and their families ([What is PPE?](https://www.bbc.co.uk/news/health-52254745))

    Starting today, 21st April, We are collecting and sharing anonymous contributions about the real-time regional availability of PPE direct from users of our products.
    """
  )

  st.image("./static/images/device-preview.png", 
            caption="In-app data collection", 
            width=300)

  #st.header("Contribute your PPE data")



  


if __name__ == "__main__":
  main()


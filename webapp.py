import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import pickle
import requests

#---Configuring the web apps's title name and its favicon
st.set_page_config(page_title =" Movie Recommendation System",page_icon =":computer:",layout="wide")

#----Making the navigation menu
with st.sidebar:
    choose =option_menu(
        "MR System",["Home","MR System","About us","Contact us"],
        icons = ["house","cpu","people","envelope"],
        menu_icon = "app-indicator",
        default_index = 0,
        styles={
        "container": {"padding": "5!important","background-color": "#040C6D"},
        "icon": {"color": "#FFFFFF ", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left","color": "#FFFFFF ", "margin":"0px", "--hover-color": "#373A5B "},
        "nav-link-selected": {"background-color": "#010318"},
    }
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#---Loading all the iamges used here
lottie_coding = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_cbemdbsc.json")
lottie_coding2 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_knvn3kk2.json")
logo = Image.open(r'image/logo2.png')
kishor = Image.open(r'image/kishork.png')
dhruv = Image.open(r'image/dhruv.png')
subhajit = Image.open(r'image/subhajit.png')
rimi = Image.open(r'image/rimi.png')
ankush = Image.open(r'image/ankush.png')
anna = Image.open(r'image/anna.png')

#--- Making the decision if-else to navigate through diffrent menus selected
#--if "Home " is selected --- its operational code
if choose == "Home":
    col1, col2 = st.columns( [0.8, 0.2])    
    with col1:               #---To display the header text using css style
        st.markdown(""" <style> .font { font-size:45px ; font-family: 'Cooper Black'; color: #009edc;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Movie Recommendation System</p>', unsafe_allow_html=True)
    with col2:               #---To display brand logo
        st.image(logo, width=90 )   

    col1, col2 = st.columns( [0.7, 0.3])
    with col1:
        st.subheader('What is Recommendation system ?')
        st.write("A recommendation system is a subclass of Information filtering Systems that seeks to predict the rating or the preference a user might give to an item. In simple words, it is an algorithm that suggests relevant items to users. Eg: In the case of Netflix which movie to watch, In the case of e-commerce which product to buy, or In the case of kindle which book to read, etc.")  
        st.subheader('Use-Cases Of Recommendation System') 
        st.write("""There are many use-cases of it. Some are

A. Personalized Content:  Helps to Improve the on-site experience by creating dynamic recommendations for different kinds of audiences like Netflix does.

B. Better Product search experience:  Helps to categories the product based on their features. Eg: Material, Season, etc.""")
    with col2:
        st_lottie(lottie_coding, height = 350, key =" coding") 

    st.header('TYPES OF RECOMMENDATION SYSTEM')
    st.subheader('1. Content-Based Filtering')
    st.write("In this type of recommendation system, relevant items are shown using the content of the previously searched items by the users. Here content refers to the attribute/tag of the product that the user like. In this type of system, products are tagged using certain keywords, then the system tries to understand what the user wants and it looks in its database and finally tries to recommend different products that the user wants.")
          
    st.subheader('2. Collaborative Based Filtering')
    st.write("""Recommending the new items to users based on the interest and preference of other similar users is basically collaborative-based filtering. 
                This overcomes the disadvantage of content-based filtering as it will use the user Interaction instead of content from the items used by the users. For this, it only needs the historical performance of the users. Based on the historical data, with the assumption that user who has agreed in past tends to also agree in future.""")
    st.header("CONCLUSION")
    st.write("This small article covered many topics related to recommendation engines like What are it and its use-cases. Apart from this different types of recommendation systems like content-based filtering and collaborative based filtering and in collaborative filtering also user-based as well as item-based along with its examples, advantages and disadvantages, and finally the evaluation metrics to evaluate the model.")


#--if "MR System " is selected --- its operational code[the main system of project]

elif choose == "MR System":
    def fetch_poster(movie_id): #--- Function made to fetch the poster of movies 

        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


    movies = pickle.load(open('movie_dict.pkl', 'rb')) #--- loading the pickle format data from jupyter notebook
    similarity = pickle.load(open('Similarity.pkl', 'rb'))


    def recommend(movie):   #--- Function that implements KNN using cosine similarity.
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        movie_list = sorted(list(enumerate(distances)),
                            reverse=True, key=lambda x: x[1])[1:16]
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:16]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters



    movie_list = movies['title'].values
    


    #--- Designing the header part of our function    
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               #---To display the header text using css style
            st.markdown("""  <style> .font { font-size:45px ; font-family: 'Cooper Black'; color: #009edc;} </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Movie Recommendation System</p>', unsafe_allow_html=True)    
    with col2:               #---To display brand logo
        st.image(logo, width=90 )


    apps = ['--Select--', 'Movie based']
    app_options = st.selectbox('Select application:', apps)

    if app_options == 'Movie based':
        selected_movie =st.selectbox('Select movie:', movie_list)

    #--- Recommending top 15 movies:
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(recommended_movie_posters[0])
            st.text(recommended_movie_names[0])

        with col2:
            st.image(recommended_movie_posters[1])
            st.text(recommended_movie_names[1])

        with col3:
            st.image(recommended_movie_posters[2])
            st.text(recommended_movie_names[2])
        with col4:
            st.image(recommended_movie_posters[3])
            st.text(recommended_movie_names[3])

        with col5:
            st.image(recommended_movie_posters[4])
            st.text(recommended_movie_names[4])

        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            st.image(recommended_movie_posters[5])
            st.text(recommended_movie_names[5])

        with col7:
            st.image(recommended_movie_posters[6])
            st.text(recommended_movie_names[6])

        with col8:
            st.image(recommended_movie_posters[7])
            st.text(recommended_movie_names[7])
        with col9:
            st.image(recommended_movie_posters[8])
            st.text(recommended_movie_names[8])

        with col10:
            st.image(recommended_movie_posters[9])
            st.text(recommended_movie_names[9])
        col10, col11, col12, col13, col14 = st.columns(5)
        with col10:
            st.image(recommended_movie_posters[10])
            st.text(recommended_movie_names[10])

        with col11:
            st.image(recommended_movie_posters[11])
            st.text(recommended_movie_names[11])

        with col12:
            st.image(recommended_movie_posters[12])
            st.text(recommended_movie_names[12])
        with col13:
            st.image(recommended_movie_posters[13])
            st.text(recommended_movie_names[13])

        with col14:
            st.image(recommended_movie_posters[14])
            st.text(recommended_movie_names[14])


elif choose == "About us":
    with st.container():
        st.markdown(""" <style> .font { font-size:45px ; font-family: 'Cooper Black'; color: #009edc;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About us and our project.</p>', unsafe_allow_html=True)  
        st.write("##")
        col1, col2 = st.columns([0.7,0.3])
        with col1:
            st.write("I am Kishor Kumar and along with my team-mates, we have developed this project 'Movie Recommendation System'. It is a machine learning project developed in python language using a web application framework called 'Streamlit'.")
            st.write("#")
            st.write("We have provided all the details below:")
            st.write("NAME :  Movie Recommendation System")
            st.write("TECHNOLOGY :  Supervised Machine Learning")
            st.write("LANGUAGE USED :  Python, HTML and CSS")
            st.write("IDE :  Jupyter Notebook and VS Code")
            st.write("FRAMEWORK :  Streamlit [Python's Web-based application development framework]")
            st.write("##")
        with col2:
            st_lottie(lottie_coding2, height = 300, key =" coding")
        st.write("---")
        st.subheader("TEAM MEMBERS")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with imageclm:
            st.image(kishor, width = 150)
        with textclm:
            st.subheader("KISHOR KUMAR")
            st.write("Reg. No. of 2019-2022: D192000379")
            st.write("##")
        st.write("#")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with imageclm:
            st.image(dhruv, width = 150)
        with textclm:
            st.subheader("DHRUBAJIT GOPE")
            st.write("Reg. No. of 2019-2022: D192000374")
            st.write("##")
        st.write("#")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with textclm:
            st.subheader("RIMI MONDAL")
            st.write("Reg. No. of 2019-2022: D192000389")
            st.write("#")
        with imageclm:
            st.image(rimi, width = 150)
        st.write("#")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with textclm:
            st.subheader("ANANYA MUKHERJEE")
            st.write("Reg. No. of 2019-2022: D192000364")
            st.write("#")
        with imageclm:
            st.image(anna, width = 150)
        st.write("#")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with textclm:
            st.subheader("ANKUSH PAUL")
            st.write("Reg. No. of 2019-2022: D192000368")
            st.write("#")
        with imageclm:
            st.image(ankush, width = 150)
        st.write("#")
        st.write("---")
        imageclm , textclm = st.columns([0.3,0.7])
        with textclm:
            st.subheader("SUBAJIT CHAKRABORTY ")
            st.write("Reg. No. of 2019-2022: D192000403")
            st.write("##")
        with imageclm:
            st.image(subhajit, width = 150)

#---If "Contact us" selected, it will redirect to contact form page.
elif choose == "Contact us":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #009edc;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    
    st.subheader(":mailbox: Get in touch with us!")

    
    
    contact_form = """
    <form action="https://formsubmit.co/kishorkumar83076@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
"""

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")
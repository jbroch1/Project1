import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import main_functions

# nltk.download("punkt")
# nltk.download("stopwords")

# --------------PART A - The Top Stories API

st.title("COP 4813 - Web Application Programming")

st.title("Project 1")

st.header("Part A - NY Times Top Stories")

st.write("This app displays the most common words used in the current top articles from the NY Times based on the topic selected. The data is displayed as a line chart and as a wordcloud.")

st.subheader("I - Topic Selection")

# GET USER INPUT

name = st.text_input(label="Please enter you name", value="", type="default")

topic = st.selectbox("Select your topic of interest",
                       ["", "Arts", "Automobiles", "Books", "Business", "Fashion", "Food", "Health", "Home", "Insider", "Magazine", "Movies", "NYRegion", "Obituaries", "Opinion", "Politics", "RealEstate", "Science", "Sports", "SundayReview", "Technology", "Theater", "T-magazine", "Travel", "Upshot", "US", "World"],
                       )

if name != "" and topic != "":
    st.write("Hello {},".format(name) + " you selected {}.".format(topic))


# FIND URL WITH TOPIC FROM USER AND CREATE ABSTRACT WITH ALL ARTICLES

api_key_dict = main_functions.read_from_file("JSON_files/api_key.json")
api_key = api_key_dict["my_key"]


url = "https://api.nytimes.com/svc/topstories/v2/"+topic+".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response,"JSON_files/response.json")

my_articles = main_functions.read_from_file("JSON_files/response.json")

if topic != "":
    str1 = ""
    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]


# GENERATE FREQUENCY DISTRIBUTION

if topic != "":
    words = word_tokenize(str1)

    words_no_punc = []
    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    stopwords = stopwords.words("english")

    clean_words = []
    for w in words_no_punc:
        if w not in stopwords:
            clean_words.append(w)


    st.subheader("II - Frequency Distribution")
    if st.checkbox("Click here to generate Frequency Distribution"):
        fdist = FreqDist(clean_words)

        fdist_10 = pd.DataFrame(fdist.most_common(10))

        table = pd.DataFrame({"Words": fdist_10[0], "Count": fdist_10[1]})
        final = px.line(table, x="Words", y="Count", title = "")
        st.plotly_chart(final)

# DISPLAY WORDCLOUD


if topic != "":
    wordcloud = WordCloud().generate(str1)

    st.subheader("III - Wordcloud")
    if st.checkbox("Click here to generate wordcloud"):
        fig, ax = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)


# --------------PART B - Most Popular Articles


st.header("Part B - Most Popular Articles")

st.write("Select if you want to see the most shared, emailed, or viewed articles.")

articles = st.selectbox("Select your preferred set of articles",
                       ["", "Shared", "Emailed", "Viewed"],
                       )

time_frame = st.selectbox("Select the period of time (last days)",
                       ["", "1", "7", "30"],
                       )

# FIND URL WITH ARTICLE SET IN TIME FRAME FROM USER AND CREATE ABSTRACT WITH ALL ARTICLES
if articles != "" and time_frame != "":
    api_key2_dict = main_functions.read_from_file("JSON_files/api_key2.json")
    api_key2 = api_key2_dict["my_key2"]

    url2 = "https://api.nytimes.com/svc/mostpopular/v2/shared/"+time_frame+".json?api-key="+api_key2

    response2 = requests.get(url2).json()

    main_functions.save_to_file(response2,"JSON_files/response2.json")

    my_articles2 = main_functions.read_from_file("JSON_files/response2.json")

if articles != "" and time_frame != "":
    str2 = ""
    for j in my_articles2["results"]:
        str2 = str2 + j["abstract"]

# DISPLAY WORDCLOUD2

    wordcloud2 = WordCloud().generate(str2)

    fig2, ax = plt.subplots()
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig2)

import streamlit as st
import matplotlib.pyplot as plt


# Titre principal
st.set_page_config(page_title="Projet NoSQL", layout="wide")
st.title("Projet NoSQL")

st.markdown("""
Bienvenue sur le dashboard du projet NoSQL !

Voici quelques exemples des réponses du projet NoSQL 2025 pour les 4a Outils : 
MongoDB et Neo4j 

github : https://github.com/...
""")

st.header("Question 4 : Nombre de films par année")
st.image("doc/question_4.png", caption="Histogramme des films par année", width=600)


st.header("Question 12 : Corrélation entre la durée des films et leur revenu")
st.image("doc/question_12.png", caption="Corrélation entre durée et revenu de films", width=600)


st.header("Question 25 : Lien entre Tom Hanks et Scarlett Johansson")
st.image("doc/question_25.png", caption="Le chemin le plus court entre 2 acteurs", width=600)


# Nouvelle question - Films et Genres
st.header("Films et leur genre")
st.image("doc/Film et leur genre.png", caption="Films et leur genre", width=600)


# Nouvelle question - Influence entre réalisateurs
st.header("Influence entre réalisateurs")
st.image("doc/influence entre realisateur.png", caption="Influence entre réalisateurs basée sur les genres", width=600)



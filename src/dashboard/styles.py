colors = {
    "app-bg": "#2f5972",
    "secondary-bg": "#052140",
    "text": "white"
}

# ---------------------------------------------------------------------
# ------------------------------- Body --------------------------------
# ---------------------------------------------------------------------

body_style = {
    "background-color": colors['app-bg'],
    "margin-left": -8,
    "margin-top": -8,
    'padding': '0px 0px 0px 0px',
    "display": "flex",
    "flex-direction": "horizontal",
    "font-family": "HelveticaNeue"
}

tab_style = {
    "background-color": colors['secondary-bg'],
    "color": "white",
    "font-size": 20,
    "border": "solid " + colors['app-bg'],
    "border-width": "0px 0px 0px 1px"  # haut | droite | bas | gauche
}

selected_tab_style = {
    "background-color": colors['app-bg'],
    "color": "white",
    "font-size": 20,
    "border": "none",
}

topic_modelling_selected_tab_style = {
    "background-color": "white",
    "color": "black",
    "font-size": 20,
    "border": "none",
}
# --------------------------------------------------------------------------------------
# ----------------------------- Analyse Exploratoire Tab -------------------------------
# --------------------------------------------------------------------------------------

analyse_exploratoire_container_style = {
    "background-color": colors['app-bg'],
    "width": "100vw",
    "min-height": "100vh"
}

map_container_style = {
    "background-color": colors['app-bg'],
    "width": "1300px",
    "margin": "auto",
    "margin-top": "20px",
    "height": "500px"
}

map_dates_dropdown_style = {
    "width": "300px",
    "margin-bottom": "10px",
    "border": "None"
}

chart_container_style = {
    "width": "1300px",
    "margin": "auto",
    "margin-top": "70px",
    "height": "400px",
    "display": "flex",
    "flex-direction": "horizontal"
}

wordcloud_container_style = {
    "background-color": colors['app-bg'],
    "width": "650px",
    "height": "300px"
}

wordcloud_dropdown_style = {
    "width": "100%",
    "margin-bottom": 20,
    "position": "inline-block",
    "z-index": 5
}

pie_container_style = {
    "background-color": colors['app-bg'],
    "width": "650px",
    "height": "300px",
    "margin-top": "0px"
}

# --------------------------

analyze_tweet_container_style = {
    "width": "1300px",
    "height": "200px",
    "margin": "auto"
}

analyze_container_style = {
    "width": "1300px",
    "height": "50px",
    "display": "flex",
    "flex-direction": "horizontal"
}

analyze_tweet_url_style = {
    "width": "990px",
    "margin": 0,
    "padding": 20,
    "max-height": "100%",
    "font-size": 18,
    "color": "black",
    "border-radius": 6,
    "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)",
    "margin-right": 10
}

analyze_button_style = {
    "background-color": "#8064A2",
    "width": "300px",
    "margin": 0,
    "padding": 0,
    "max-height": "100%",
    "font-size": 20,
    "color": "white",
    "border": "None",
    "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)",
    "border-radius": 6
}

results_container_style = {
    "background-color": colors['app-bg'],
    "margin-top": 20,
    "width": "100%",
    "height": "60px",
    "display": "flex",
    "flex-direction": "horizontal"
}

topics_div_style = {
    "width": "260px",
    "background-color": colors['secondary-bg'],
    "margin": 5,
    "color": "white",
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    "font-size": 20,
    "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)"
}

# --------------------------------------------------------------------------------------
# ----------------------------- Nettoyage des données Tab ------------------------------
# --------------------------------------------------------------------------------------

nettoyage_donnees_container_style = {
    "width": "100vw",
    "height": "100vh",
    'display': 'flex',
    'flex-direction': 'row'
}

nettoyage_donnees_sidebar_style = {
    "width": "100px",
    'padding': 10,
    'flex': 0.15
}

nettoyage_donnees_table_style = {
    "width": "1000px",
    "margin-top": 15,
    'padding': 10,
    'flex': 1
}

nettoyage_donnees_title_style = {
    "width": "100%",
    "color": "white",
    "text-align": "center",
    "margin": "auto",
    "margin-top": 15
}

nettoyage_donnees_subtitle_style = {
    "width": "100%",
    "color": "white",
    "text-align": "center",
    "margin": "auto",
    "margin-top": 10
}

nettoyage_donnees_checklist_style = {
    "color": "white",
    "margin": "15px 0px 20px 10px"  # haut | droite | bas | gauche
}

nettoyage_donnees_sentiment_button_style = {
    "width": "90%",
    "background-color": "#8064A2",
    "display": "block",
    "margin": "auto",
    "margin-top": 15,
    "font-size": 15,
    "color": "white",
    "border": "None",
    "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)",
    "border-radius": 6
}

# --------------------------------------------------------------------------------------
# ---------------------------- Analyse des sentiments Tab ------------------------------
# --------------------------------------------------------------------------------------

analyse_sentiments_container_style = {
    "width": "100vw",
    "height": "100vh"
}

# --------------------------------------------------------------------------------------
# -------------------------------- Topic Modelling Tab ---------------------------------
# --------------------------------------------------------------------------------------

topic_modelling_container_style = {
    "width": "100vw",
    "height": "100vh",
    "background-color": "white"
}
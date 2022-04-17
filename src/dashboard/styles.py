colors = {
    "app-bg": "#2f5972",
    "sidebar-bg": "#052140",
    "text": "white"
}

# ---------------------------------------------------------------------
# ------------------------------- Body --------------------------------
# ---------------------------------------------------------------------

body_style = {"min-width": "100%",
              "min-height": "100%",
              "background-color": colors['app-bg'],
              "margin": 0,
              "padding": 0,
              "display": "flex",
              "flex-direction": "horizontal",
              "font-family": "HelveticaNeue"}

# ---------------------------------------------------------------------
# ----------------------------- Sidebar -------------------------------
# ---------------------------------------------------------------------

sidebar_container_style = {"background-color": colors['sidebar-bg'],
                           "width": "25%",
                           "min-height": "100vh",
                           "color": "white",
                           "margin": "0px",
                           "padding": "0px"}

title_style = {"text-align": "center",
               "font-size": "30px"}

# Style des labels
choose_model_style = {"width": "100%",
                      "height": "40px",
                      "font-size": "20px",
                      "display": "inline-block",
                      "transition": "all 0.2s ease",
                      "text-align": "center",
                      "margin-top": "20px"}

# Style des checkbox
choose_model_input_style = {"margin-right": "10px",
                            "width": "16px",
                            "height": "16px"}

# ---------------------------------------------------------------------
# ----------------------------- Content -------------------------------
# ---------------------------------------------------------------------
content_container_style = {"background-color": colors['app-bg'],
                           "width": "100%",
                           "min-height": "100vh"}

map_container_style = {"background-color": colors['app-bg'],
                       "width": "1100px",
                       "margin": "auto",
                       "margin-top": "20px",
                       "height": "400px"}

map_dates_dropdown_style = {"width": "300px",
                            "margin-bottom": "10px",
                            "border": "None"}

chart_container_style = {"width": "1100px",
                         "margin": "auto",
                         "margin-top": "70px",
                         "height": "400px",
                         "display": "flex",
                         "flex-direction": "horizontal"}

wordcloud_container_style = {"background-color": colors['app-bg'],
                             "width": "550px",
                             "height": "300px"}

wordcloud_dropdown_style = {"width": "100%",
                            "margin-bottom": 20,
                            "position": "inline-block",
                            "z-index": 5}

pie_container_style = {"background-color": colors['app-bg'],
                       "width": "550px",
                       "height": "300px",
                       "margin-top": "0px"}

# --------------------------

analyze_tweet_container_style = {"width": "1100px",
                                 "height": "200px",
                                 "margin": "auto"}

analyze_container_style = {"width": "1100px",
                           "height": "50px",
                           "display": "flex",
                           "flex-direction": "horizontal"
                           }

analyze_tweet_url_style = {"width": "840px",
                           "margin": 0,
                           "padding": 20,
                           "max-height": "100%",
                           "font-size": 18,
                           "color": "black",
                           "border-radius": 6,
                           "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)",
                           "margin-right": 10}

analyze_button_style = {"background-color": "#8064A2",
                        "width": "250px",
                        "margin": 0,
                        "padding": 0,
                        "max-height": "100%",
                        "font-size": 20,
                        "color": "white",
                        "border": "None",
                        "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)",
                        "border-radius": 6}

results_container_style = {"background-color": colors['app-bg'],
                           "margin-top": 20,
                           "width": "100%",
                           "height": "60px",
                           "display": "flex",
                           "flex-direction": "horizontal"}

topics_div_style = {"width": "220px",
                    "background-color": colors['sidebar-bg'],
                    "margin": 5,
                    "color": "white",
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "font-size": 20,
                    "box-shadow": "0px 8px 15px rgba(0, 0, 0, 0.1)"}

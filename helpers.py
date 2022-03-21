import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html, dash_table
import dash
import plotly_express as px
import numpy as np
import plotly.graph_objects as go

# Import data
data = pd.read_feather(r"C:\Users\juancarlos.izurieta\Documents\R projects\IntroducedSpeciesDashboard\data\ie_joined.feather")
sk = pd.read_feather(r"C:\Users\juancarlos.izurieta\Documents\R projects\IntroducedSpeciesDashboard\data\sankey.feather")
sk_labels = pd.read_feather(
    r"C:\Users\juancarlos.izurieta\Documents\R projects\IntroducedSpeciesDashboard\data\sankey_labels.feather")

# Colors
color_success = "#62c462"
color_info = "#3498db"
color_primary = "#2c3e50"
color_secondary = "#7a8288"
color_warning = "#f89406"
color_danger = "#ee5f5b"

color_danger_alpha = "#e74c3c17"
color_success_alpha = "#18bc9c1a"
color_warning_alpha = "#f39c1221"

color_gradients = ["rgb(57, 73, 155)", "rgb(87, 72, 157)", "rgb(112, 70, 157)", "rgb(134, 68, 156)",
                   "rgb(155, 65, 151)", "rgb(174, 62, 146)", "rgb(191, 59, 138)", "rgb(206, 59, 129)",
                   "rgb(219, 61, 118)", "rgb(229, 66, 107)", "rgb(237, 74, 95)", "rgb(243, 84, 83)", "rgb(246, 96, 70)",
                   "rgb(246, 109, 56)", "rgb(244, 123, 41)"]

df = data.groupby(["OrganismType", "icon"]).size()
df.sort_values(ascending=False)

# Header
header = html.Div(
    [
        html.H4("Galapagos introduced species status dashboard",
                style={'display': 'inline-block', "color": "white", 'marginLeft': 5, "bottom": 10})
    ], style={"background": "#333f54", 'display': 'inline-block', "width": "100%", "padding": "1rem"}
)


# Functions

def error_chart():
    fig = px.line(x=[0, 0, 0], y=[0, 0, 0], title="Please select input")
    fig.update_layout(
        title_font_color="pink",
        title_font_size=10,
        xaxis_title="x",
        yaxis_title="y",
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(size=10),
        autosize=True,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=1,
            pad=2
        )
    )

    return fig


def cum_records_chart(df_input, x):
    nans = sum(pd.isnull(df_input[x]))
    df = df_input[df_input[x].notnull()]
    df.reset_index(level=0, drop=True, inplace=True)

    y = df.index+1

    fig = px.line(df, x=df[x], y=y,
                  title="Cummulative species records <br>" + "+" + str(nans) + " records with unknown year of record")
    fig.update_traces(line=dict(color=color_gradients[0], width=4))
    fig.add_scatter(x=[fig.data[0].x[-1]],
                    y=[fig.data[0].y[-1]],
                    text=[fig.data[0].y[-1]],
                    mode='markers+text',
                    marker=dict(color=color_gradients[0], size=12),
                    textfont=dict(color=color_gradients[0], size=14),
                    textposition='middle left',
                    showlegend=False)
    fig.update_layout(
        title_font_color=color_gradients[0],
        title_font_size=12,
        xaxis_title="Date",
        yaxis_title="Species records",
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(size=10),
        autosize=True,
        # width=350,
        height=250,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=1,
            pad=2
        )
    )

    return fig


# Helper functions
def radio_buttons_creator(df, column, _id, value):
    unique_values = sorted(df[column].dropna().unique())
    radioButtons = dbc.RadioItems(id=_id,
                                  options=[{"label": i, 'value': i} for i in unique_values],
                                  value=value)
    return radioButtons


def checklist_creator(df, column, _id):
    unique_values = sorted(df[column].dropna().unique())
    checklist = dbc.Checklist(id=_id,
                              options=[{"label": i, 'value': i} for i in unique_values],
                              value=unique_values,
                              switch=True, className="checklist")
    return checklist


def check_all_creator(_id, value):
    check_all = dbc.Checkbox(id=_id,
                             label="Seleccionar todo",
                             value=value)
    return check_all


def pie_chart_creator(df, column):
    df = df.groupby([column]).size()
    df = df.sort_values(ascending=False)
    labels = df.index
    values = df.values

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,
                                 marker_colors=[color_gradients[0],
                                                color_gradients[3],
                                                color_gradients[5],
                                                color_gradients[9],
                                                color_gradients[-1]])])
    fig.update_layout(
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=0,
        #     xanchor="right",
        #     x=1
        # ),
        autosize=True,
        # width=350,
        height=250,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=1,
            pad=2
        )
    )

    return fig


def create_subpathway_bar_chart(df, column):
    df = df.value_counts([column])
    df = df.reset_index(level=0)
    df.columns = ["Subpathway", "Frequency"]
    # print(df)
    df = df.sort_values("Frequency")
    # reversed_color_gradients = list(reversed(color_gradients))

    fig = px.bar(df, x="Frequency", y="Subpathway", color="Frequency", color_continuous_scale=color_gradients)

    return fig


def create_status_value_cards(df, column):
    df = pd.Series(df.value_counts([column]))
    df.sort_values(ascending=False, inplace=True)

    layout = []

    if "Currently established" in df.index:
        established = create_layout_per_status_category(df, "Currently established",
                                                        color_danger, "danger", color_danger_alpha)
    else:
        established = []

    if "Intercepted" in df.index:
        intercepted = create_layout_per_status_category(df, "Intercepted",
                                                        color_warning, "warning", color_warning_alpha)
    else:
        intercepted = []

    if "Eradicated" in df.index:
        eradicated = create_layout_per_status_category(df, "Eradicated",
                                                       color_success, "success", color_success_alpha)
    else:
        eradicated = []

    layout.append(established)
    layout.append(intercepted)
    layout.append(eradicated)

    return layout


### The following function embeds into previous layout function
def create_layout_per_status_category(df, category, color, color_string, color_alpha):
    percentages = round(df[category] / sum(df.values) * 100, 2)
    layout = html.Div(
        [
            html.Div(html.P(category, className="valuecard-header-p"),
                     style={"text-align": "center", "background-color": color,
                            "padding": "0.25rem"}),
            html.Div(
                [
                    html.Div(html.P(str(df[category]) + " species", className="values-next-to-perc")),
                    html.Div(html.P(str(percentages) + "% ", className="percentages")),
                    html.Div(create_meter(percentages, color_string, "#fff", "60%", "colored"),
                             className="meter-container"),
                    html.Br()
                ], style={"background-color": color_alpha, "text-align": "center"}
            )
        ], style={"padding": "0"}
    )

    return layout


def create_images_meter_layout(df, data_column, img_column):
    df = df.groupby([data_column, img_column]).size()
    df = df.sort_values(ascending=False)
    labels = df.index.get_level_values(data_column)
    icons = df.index.get_level_values('icon')
    values = df.values
    percentages = np.round(df.values / sum(df.values) * 100, 2)

    children = []

    for i in range(len(labels)):
        children.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src=icons[i], height="25px", style={"opacity": "0.35"}),
                                    html.P(labels[i], style={"margin-left": "10px"})
                                ], style={"display": "flex", "justify-content": "flex-start", "align-items": "center"}
                            ),
                            html.Div(
                                [
                                    html.P(str(values[i]) + " species ", className="info-values"),
                                    html.P("| " + str(percentages[i]) + "% ", className="percentages")
                                ], style={"display": "flex", "justify-content": "flex-end", "align-items": "center"}
                            )
                        ], style={"display": "flex", "justify-content": "space-between"}
                    ),
                    html.Div(
                        html.Div(create_meter(percentages[i], "info", "#e5e5e5", "100%", "one-color"),
                                 className="meter-container")
                    )
                ]
            )
        )

    layout = html.Div(children)

    return layout


def create_meter_layout(df, data_column):
    df = df.groupby([data_column]).size()
    df = df.sort_values(ascending=False)
    labels = df.index.get_level_values(data_column)
    values = df.values
    percentages = np.round(df.values / sum(df.values) * 100, 2)

    children = []

    for i in range(len(labels)):
        children.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(labels[i], style={"margin-left": "10px"})
                                ], style={"display": "flex", "justify-content": "flex-start", "align-items": "center"}
                            ),
                            html.Div(
                                [
                                    html.P(str(values[i]) + " species ", className="info-values"),
                                    html.P("| " + str(percentages[i]) + "% ", className="percentages")
                                ], style={"display": "flex", "justify-content": "flex-end", "align-items": "center"}
                            )
                        ], style={"display": "flex", "justify-content": "space-between"}
                    ),
                    html.Div(
                        html.Div(create_meter(percentages[i], "info", "#e5e5e5", "100%", "one-color"),
                                 className="meter-container")
                    )
                ]
            )
        )

    layout = html.Div(children)

    return layout


# def create_valuecards_layout(df, column, metric_colors, alpha_colors, heading_colors):
#     df = df.groupby([column]).size()
#     df.sort_values(ascending=False)
#     labels = df.index
#     values = df.values
#     percentages = np.round(df.values / sum(df.values) * 100, 2)
#
#     children = []
#
#     for i in range(len(labels)):
#         children.append(
#             html.Div(
#                 [
#                     html.Div(html.P(labels[i], className="valuecard-header-p"),
#                              style={"text-align": "center", "background-color": heading_colors[i],
#                                     "padding": "0.25rem"}),
#                     html.Div(
#                         [
#                             html.Div(html.P(str(values[i]) + " especies", className="values-next-to-perc")),
#                             html.Div(html.P(str(percentages[i]) + "% ", className="percentages")),
#                             html.Div(create_meter(percentages[i], metric_colors[i], "#fff", "60%"),
#                                      className="meter-container"),
#                             html.Br()
#                         ], style={"background-color": alpha_colors[i], "text-align": "center"}
#                     )
#                 ], style={"padding": "0"}
#             )
#         )
#
#     layout = html.Div(children)
#
#     return layout


# def create_images_meter_layout(df, data_column, img_column):
#     df = df.groupby([data_column, img_column]).size()
#     df = df.sort_values(ascending=False)
#     labels = df.index.get_level_values(data_column)  ########
#     icons = df.index.get_level_values('icon')
#     values = df.values
#     percentages = np.round(df.values / sum(df.values) * 100, 2)
#
#     children = []
#
#     for i in range(len(labels)):
#         children.append(
#             html.Div(
#                 [
#                     html.Div(
#                         [
#                             html.Img(src=icons[i], height="25px"),
#                             html.P(labels[i], style={"margin-right": "10px"})
#                         ], style={"text-align": "right", "margin-right": "10px", "width": "40%"}
#                     ),
#                     html.Div(
#                         [
#                             html.Div(html.Div(create_meter(percentages[i], "info", "lightgray", "100%"))),
#                             html.Div(
#                                 [
#                                     html.Div(html.P(str(values[i]) + " especies ", className="info-values")),
#                                     html.Div(html.P("| " + str(percentages[i]) + "% ", className="percentages")),
#                                 ], style={"display": "flex"}
#                             )
#                         ], style={"width": "60%", "margin-bottom": "0", "align-self": "end", "margin-right": "2rem"}
#                     )
#                 ], style={"display": "flex", "justify-content": "center"}
#             )
#         )
#
#     layout = html.Div(children)
#
#     return layout


def create_meter(value, color, background_color, width, mode):
    # Compensating visually small values
    if value < 1:
        value = 1
    else:
        value = value

    if mode == "one-color":
        meter = html.Meter(
            min=0,
            max=100,
            value=str(value),
            style={"width": "100%"}
        )
    elif mode == "colored":
        meter = dbc.Progress(
            label="",
            value=value,
            max=100,
            min=0,
            color=color,
            style={"height": "7px", "width": width, "border-radius": "1rem", "background-color": background_color})

    return meter

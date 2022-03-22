from helpers import *

# App constructor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Sections
# Controls
controls = html.Div(
    dbc.Accordion(
        dbc.AccordionItem(
            title="Controls",
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Status", className="labels"),
                                check_all_creator("status-all-selected", False),
                                checklist_creator(data, "introducedStatus", "status-selection")
                            ], className="controls-item"
                        ),
                        html.Div(
                            [
                                html.Label("Organism type", className="labels"),
                                check_all_creator("organism-type-all-selected", False),
                                checklist_creator(data, "OrganismType", "organism-type-selection")
                            ], className="controls-item"
                        ),
                        html.Div(
                            [
                                html.Label("Pathway", className="labels"),
                                check_all_creator("pathway-all-selected", False),
                                checklist_creator(data, "Pathway", "pathway-selection")
                            ], className="controls-item"
                        ),
                        html.Div(
                            [
                                html.Label("Mode of introduction", className="labels"),
                                check_all_creator("moi-all-selected", False),
                                checklist_creator(data, "MOI", "moi-selection")
                            ], className="controls-item"
                        ),
                        html.Div(
                            [
                                html.Label("Galapagos Status", className="labels"),
                                check_all_creator("gpsstatus-all-selected", False),
                                checklist_creator(data, "GPSStatus", "gpsstatus-selection")
                            ], className="controls-item"
                        )
                    ], className="controls-container"
                )
            ]
        ), start_collapsed=True
    )
)

# Total
total = dbc.Card([
    html.Div(html.Label("Total introduced species in Galapagos", className="labels"),
             className="label-container"),
    html.Div(id="total-species", style={"text-align": "center"}),
    html.Br(),
    html.Div(dcc.Graph(id="cum-count", config={'displayModeBar': False})),
    html.Div(id="last-record", style={"text-align": "center", "margin-top": "0.25rem"})
], body=True, className="card-box")

status = dbc.Card([
    html.Div(html.Label("Introduced species per status", className="labels"),
             className="label-container"),
    html.Div(id="status", className="indicator"),
    # html.Div(id="status", children=[html.P("123")], className="indicator")
], body=True, className="card-box")

organism_type = dbc.Card([
    html.Div(html.Label("Introduced species per organism type", className="labels"),
             className="label-container"),
    html.Div(id="organism-type"),
], body=True, className="card-box")

pathway = dbc.Card([
    html.Div(html.Label("Pathways to Galapagos", className="labels"), className="label-container"),
    html.Div(dcc.Graph(id="pathway", config={'displayModeBar': False})),
    html.Div(
        dbc.Button("See sub-pathways", id="subpathway-modal-btn", size="sm", outline=True, color="primary", n_clicks=0),
        style={"text-align": "center", "margin-top": "1rem"})
], body=True, className="card-box")

moi = dbc.Card([
    html.Div(html.Label("Mode of introduction", className="labels"), className="label-container"),
    html.Div(dcc.Graph(id="moi", config={'displayModeBar': False}))
], body=True, className="card-box")

gps_status = dbc.Card([
    dbc.CardBody(
        [
            html.Div(html.Label("Status in Galapagos", className="labels"), className="label-container"),
            html.Div(id="gpsstatus")
        ]
    ),
    dbc.CardFooter([dbc.Button("Definitions", size="sm", outline=True, color="secondary"),
                    dbc.Button("Download table", size="sm", outline=True, color="secondary")])
], body=True, className="card-box")

# test = html.Div(dcc.Graph(id="test"))

subpathway_modal = dbc.Modal(id="subpathway-modal",
                             children=[
                                 dbc.ModalHeader(dbc.ModalTitle("Species subpathways")),
                                 dbc.ModalBody(
                                     [
                                         html.Div(html.Label("Subpathways frequencies", className="labels")),
                                         html.Div(dcc.Graph(id="subpathway", config={'displayModeBar': False})),
                                         html.Div(
                                             html.Label("Relation between organism types, pathways and subpathways",
                                                        className="labels")),
                                         html.Div(dcc.Graph(id="sankey"))
                                     ]
                                 )
                             ],
                             size="xl",
                             is_open=False)

app.layout = html.Div([
    header,
    html.Div(controls),
    html.Div([
        total,
        status,
        organism_type,
        moi,
        pathway,
        gps_status,
        subpathway_modal,
    ], className="page-container"),
    html.Div([

    ], className="page-container"),
])


@app.callback(
    Output("status-selection", "value"),
    Input("status-all-selected", "value"),
    prevent_initial_call=True
)
def check_all_status(check):
    values = []
    if check:
        values = data["introducedStatus"].dropna().unique()
    return values


@app.callback(
    Output("organism-type-selection", "value"),
    Input("organism-type-all-selected", "value"),
    prevent_initial_call=True
)
def check_all_status(check):
    values = []
    if check:
        values = data["OrganismType"].dropna().unique()
    return values


@app.callback(
    Output("pathway-selection", "value"),
    Input("pathway-all-selected", "value"),
    prevent_initial_call=True
)
def check_all_status(check):
    values = []
    if check:
        values = data["Pathway"].dropna().unique()
    return values


@app.callback(
    Output("moi-selection", "value"),
    Input("moi-all-selected", "value"),
    prevent_initial_call=True
)
def check_all_status(check):
    values = []
    if check:
        values = data["MOI"].dropna().unique()
    return values


@app.callback(
    Output("gpsstatus-selection", "value"),
    Input("gpsstatus-all-selected", "value"),
    prevent_initial_call=True
)
def check_all_status(check):
    values = []
    if check:
        values = data["GPSStatus"].dropna().unique()
    return values


@app.callback(
    Output("total-species", "children"),
    Output("cum-count", "figure"),
    Output("last-record", "children"),
    Output("status", "children"),
    Output("organism-type", "children"),
    Output("pathway", "figure"),
    Output("moi", "figure"),
    Output("gpsstatus", "children"),
    Output("subpathway", "figure"),
    Output("subpathway-modal", "is_open"),
    Output("subpathway-modal-btn", "n_clicks"),
    Output("sankey", "figure"),
    Input("status-selection", "value"),
    Input("organism-type-selection", "value"),
    Input("pathway-selection", "value"),
    Input("moi-selection", "value"),
    Input("gpsstatus-selection", "value"),
    Input("subpathway-modal-btn", "n_clicks")
)
def update_layout(status_selection, organism_type_selection, pathway_selection, moi_selection, gpsstatus_selection,
                  subpathway_btn):
    selections = [status_selection, organism_type_selection, pathway_selection, moi_selection, gpsstatus_selection]

    df = data[data["introducedStatus"].isin(selections[0]) &
              data["OrganismType"].isin(selections[1]) &
              data["Pathway"].isin(selections[2]) &
              data["MOI"].isin(selections[3]) &
              data["GPSStatus"].isin(selections[4])]

    df.reset_index(drop=True, inplace=True)
    # df.index = range(1, len(df) + 1)
    # print(df)

    error_message = html.P("Please select input", className="error-message")

    # &
    # data_copy["OrganismType"].isin(organism_type_selection) &
    # data_copy["Pathway"].isin(pathway_selection) &
    # data_copy["MOI"].isin(moi_selection) &
    # data_copy["GPSStatus"].isin(gpsstatus_selection)
    # print(selections)

    # Main value card
    if len(df.index) > 0:
        total_species = html.P(str(df.shape[0]) + " species", className="main-value")
    else:
        total_species = error_message

    # Cummulative records plot
    if len(df.index) > 0:
        cum_count = cum_records_chart(df, "FirstRecordDate")
    else:
        cum_count = error_chart()

    if len(df.index) > 0:
        valid_df = df[df["FirstRecordYear"].notnull()]
        last_record_index = len(valid_df["FirstRecordYear"]) - 1
        last_record_spp = valid_df["ScientificName"][last_record_index]
        last_record = html.Div(
            [
                html.P("Last record year: " + str(int(df["FirstRecordYear"][last_record_index]))),
                html.P("Last species recorded: (" + last_record_spp + ")", className="scientific-name")
            ]
        )
    else:
        last_record = error_message

    # Status layout
    if len(df.index) > 0:
        status_layout = create_status_value_cards(df, "introducedStatus")
    else:
        status_layout = error_message

    # Organism type layout
    organism_type_layout = create_images_meter_layout(df, "OrganismType", "icon")

    # Pathway chart
    pathway_chart = pie_chart_creator(df, "Pathway")

    # Moi chart
    moi_chart = pie_chart_creator(df, "MOI")

    # GPS Status chart
    gps_status_chart = create_meter_layout(df, "GPSStatus")

    # Subpathway chart
    subpathway_chart = create_subpathway_bar_chart(df, "Subpathway")
    open_modal = False
    if subpathway_btn > 0:
        open_modal = True
        subpathway_btn = 0

    # Sankey
    sankey_fig = create_sankey(sankey_labels["labels"], sankey["source"], sankey["target"], sankey["value"])

    return total_species, cum_count, last_record, status_layout, organism_type_layout \
        , pathway_chart, moi_chart, gps_status_chart, subpathway_chart, open_modal, subpathway_btn, sankey_fig


if __name__ == '__main__':
    app.run_server(debug=True)

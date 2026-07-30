from dash import html, dcc, dash_table, Input, Output, State, callback
import plotly.express as px
import pandas as pd
from navbar import create_navbar

# COORDO DE GENEVE CENTRE
GENEVA_CENTER = {"lat": 46.2044, "lon": 6.1432}

nav = create_navbar()

# CHARGEMENT DES DONNEES ECRITES DANS UN FICHIER SOURCE
#df_buildings = pd.read_json('Data_SE.json', orient='records')

df_buildings = pd.DataFrame(
{
    "id": [0, 1, 2,3,4,5],
    "nom": [
        "L'Atelier",
        "TPG Bachet",
        "La Praille",
        "JTI","Campus Biotech","Cité Léopold"
    ],
    "egid": ["295165454", "2040608", "295020439","295161133","295020439","295020439"],
    "sre": [33350, 36614, 52909,25263,50000,50000],
    "affectations": ["Industrie 60% ; Administration 30% ; Commerces 10%",
                     "Dépôt TPG", "Centre commercial-Hôtel","Administration","Laboratoires","Logements"],
    "surface_enveloppe": [15587, 21189, 32478,32478,50000,50000],
    "type_construction": ["Mi-lourde", "légère", "légère","Mi-lourde","légère","Mi-lourde"],
    "chaud_producteur": ["CAD Ziplo", "CAD SIG", "CCF gaz-Chaudière gaz-chaudière mazout","CAD SIG","CAD SIG","CAD SIG"],
    "chaud_puissance_installee_kW": [750, 2600, 2915,1500,3500,3500],
    "chaud_ratio_puiss_inst_W_m2": [17, 71, 55, 60, 60, 60],
    "chaud_puissance_max": [700, 2000, 1500, 1000, 1000, 1000],
    "chaud_conso_annuelle": [{"2023": 741000,"2024":720949,"2025":921520},
                             {"2023": 2590000,"2024":2626000,"2025":2805000},
                             {"2023": 2590000,"2024":2626000,"2025":2805000},
                             {"2023": 2590000,"2024":2626000,"2025":2805000},
                             {"2023": 2590000,"2024":2626000,"2025":2805000},
                             {"2023": 2590000,"2024":2626000,"2025":2805000}],
    "chaud_ratio_conso": [27.6, 76.6, 53, 40, 40, 40],
    "chaud_type_emetteurs": ["ventilo-convecteurs", "ventilo-convecteurs-radiateurs-monoblocs",
                             "ventilo-convecteurs-radiateurs-monoblocs","ventilo-convecteurs","ventilo-convecteurs",
                             "planchers chauffants"],
    "froid_producteur": ["FAD Ziplo", "PAC aérotherme", "GF à vis","FAD SIG","FAD SIG"," "],
    "froid_puissance_installee_kW": [850, 315, 3800,2000,2000,0],
    "froid_ratio_surfacique_W_m2": [19.2, 0, 72,50,50,0],
    "froid_puissance_max": [500, 0, 2400,2000,2000,0],
    "froid_conso_annuelle": [{"2023": 584330,"2024":584330,"2025":584330},
                             {"2023": 0,"2024":0,"2025":0},
                             {"2023": 2540000,"2024":2540000,"2025":2540000},
                             {"2023": 1500000,"2024":1500000,"2025":1500000},
                             {"2023": 1500000,"2024":1500000,"2025":1500000},
                             {"2023": 0,"2024":0,"2025":0}],
    "froid_ratio_conso": [17.5, 0, 48,48,48,0],
    "froid_type_emetteurs": ["ventilo-convecteurs", "ventilo-convecteurs-monoblocs",
                             "ventilo-convecteurs-monoblocs","ventilo-convecteurs","ventilo-convecteurs"," "],
    "lat": [46.1658, 46.1750, 46.1803,46.2226,46.2221,46.1839],
    "lon": [6.1090, 6.1320, 6.1286,6.1460,6.1486,6.1445],
})

df_display = df_buildings.copy()
df_display["chaud_conso_annuelle"] = df_display["chaud_conso_annuelle"].apply(
    lambda d: " / ".join(f"{k}: {v}" for k, v in d.items())
)
df_display["froid_conso_annuelle"] = df_display["froid_conso_annuelle"].apply(
    lambda d: " / ".join(f"{k}: {v}" for k, v in d.items())
)
data=df_display.to_dict("records")


CARD_STYLE = {
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
    "padding": "10px",
}

TITLE_STYLE = {
    "fontWeight": "600",
    "fontSize": "16px",
    "marginBottom": "5px"
}

def create_page_home():
    return html.Div(
        [
            nav,

            html.Div(
                style={
                    "height": "calc(100vh - 60px)",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "10px",
                },
                children=[
                    # ================== TABLE AT THE TOP ==================
                    html.Div([
                        html.Div("🏢 Listing des sites", style=TITLE_STYLE),
                        dash_table.DataTable(
                            id="building-table",
                            data=data,
                            row_selectable="single",
                            row_deletable=False,
                            selected_rows=[],
                            active_cell=None,
                            filter_action="native",
                            sort_action="native",
                            page_action="none",
                            merge_duplicate_headers=True,
                            columns=[
                                {"name": ["Général", "Nom"], "id": "nom"},
                                {"name": ["Général", "EGID"], "id": "egid"},
                                {"name": ["Général", "SRE"], "id": "sre"},
                                {"name": ["Général", "Affectations"], "id": "affectations"},
                                {"name": ["Général", "Surface enveloppe"], "id": "surface_enveloppe"},
                                {"name": ["Général", "Type Construction"], "id": "type_construction"},

                                {"name": ["CHAUD", "Producteur"], "id": "chaud_producteur"},
                                {"name": ["CHAUD", "Puissance Installée (kW)"], "id": "chaud_puissance_installee_kW"},
                                {"name": ["CHAUD", "Ratio Surfacique – Puiss Instal"],
                                 "id": "chaud_ratio_puiss_inst_W_m2"},
                                {"name": ["CHAUD", "Puissance Max atteinte"], "id": "chaud_puissance_max"},
                                {"name": ["CHAUD", "Conso Annuelle"], "id": "chaud_conso_annuelle"},
                                {"name": ["CHAUD", "Ratio Surf conso"], "id": "chaud_ratio_conso"},
                                {"name": ["CHAUD", "Type émetteurs"], "id": "chaud_type_emetteurs"},

                                {"name": ["FROID", "Producteur"], "id": "froid_producteur"},
                                {"name": ["FROID", "Puissance Installée (kW)"], "id": "froid_puissance_installee_kW"},
                                {"name": ["FROID", "Ratio Surfacique"], "id": "froid_ratio_surfacique_W_m2"},
                                {"name": ["FROID", "Puissance Max atteinte"], "id": "froid_puissance_max"},
                                {"name": ["FROID", "Conso Annuelle"], "id": "froid_conso_annuelle"},
                                {"name": ["FROID", "Ratio Surf conso"], "id": "froid_ratio_conso"},
                                {"name": ["FROID", "Type émetteurs"], "id": "froid_type_emetteurs"},
                            ],
                            style_table={
                                "height": "40vh",
                                "minHeight": "300px",
                                "maxHeight": "50vh",
                                "overflowY": "auto",
                                "overflowX": "auto",
                            },
                            style_cell={
                                "padding": "6px",
                                "fontSize": "11px",
                                "textAlign": "center",
                                "minWidth": "100px",
                                "maxWidth": "200px",
                                "whiteSpace": "normal",
                                "height": "auto",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                            },
                            style_header={
                                "backgroundColor": "#f4f6f8",
                                "fontWeight": "600",
                                "border": "1px solid #e0e0e0",
                            },
                            style_header_conditional=[
                                {
                                    "if": {"header_index": 0},
                                    "backgroundColor": "rgba(200, 200, 200, 0.9)",
                                    "color": "black",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                    "textAlign": "center",
                                },
                                {
                                    "if": {"column_id": ["chaud_producteur", "chaud_puissance_installee_kW",
                                           "chaud_ratio_puiss_inst_W_m2", "chaud_puissance_max",
                                           "chaud_conso_annuelle", "chaud_ratio_conso", "chaud_type_emetteurs"]},
                                    "backgroundColor": "rgba(204, 0, 0, 0.7)",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                },
                                {
                                    "if": {"column_id": ["froid_producteur", "froid_puissance_installee_kW",
                                                         "froid_ratio_surfacique_W_m2", "froid_puissance_max",
                                                         "froid_conso_annuelle", "froid_ratio_conso", "froid_type_emetteurs"]},
                                    "backgroundColor": "rgba(0, 128, 255, 0.8)",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                },
                                {
                                    "if": {"column_id": ["nom", "egid", "sre", "affectations",
                                                         "surface_enveloppe", "type_construction"]},
                                    "backgroundColor": "rgba(119, 118, 118, 0.8)",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                },
                            ],
                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"},
                                {"if": {"state": "selected"}, "backgroundColor": "#cce5ff"},
                            ],
                        ),
                    ], style={
                        **CARD_STYLE,
                        "flex": "none",
                        "minHeight": "300px",
                    }),
                    
                    # ================== MAP AND SIDE PANEL CONTAINER ==================
                    html.Div(
                        style={
                            "flex": "1",
                            "display": "flex",
                            "position": "relative",
                            "overflow": "hidden",
                            "minHeight": "0",
                        },
                        children=[
                            # MAP - fills the container
                            html.Div(
                                id="map-container",
                                style={
                                    "width": "100%",
                                    "height": "100%",
                                    "transition": "all 0.3s ease",
                                },
                                children=[
                                    dcc.Graph(
                                        id="building-map",
                                        style={"height": "100%"},
                                        config={"displayModeBar": True, "displaylogo": False}
                                    )
                                ],
                            ),
                            
                            # SIDE PANEL - positioned at bottom left
                            html.Div(
                                id="side-panel",
                                style={
                                    "position": "absolute",
                                    "bottom": "0",
                                    "left": "0",
                                    "width": "40%",
                                    "height": "0%",
                                    "transition": "height 0.3s ease",
                                    "overflowY": "auto",
                                    "overflowX": "hidden",
                                    "backgroundColor": "#f9f9f9",
                                    "borderTop": "1px solid #ddd",
                                    "borderRight": "1px solid #ddd",
                                    "borderBottom": "none",
                                    "borderLeft": "none",
                                    "zIndex": "10",
                                    "boxShadow": "0 -2px 5px rgba(0,0,0,0.1)",
                                    "borderTopLeftRadius": "12px",
                                    "borderTopRightRadius": "12px",
                                },
                                children=[]
                            ),
                        ],
                    ),
                ],
            ),
        ],
        style={"margin": "10px"},
    )

# =====================================================
# Callbacks
# =====================================================

from dash import callback, Input, Output, State
import plotly.express as px
import pandas as pd


@callback(
    Output("building-map", "figure"),
    Input("building-table", "selected_rows"),
    Input("building-map", "clickData"),
    State("building-table", "derived_virtual_data"),
    State("building-map", "figure"),
)
def update_map(selected_rows, click_data, filtered_rows, current_map_fig):
    """
    Callback to update the map's center when either a row is selected or a point is clicked.
    """

    dff = pd.DataFrame(filtered_rows) if filtered_rows else df_buildings

    center = GENEVA_CENTER
    selected_id = None

    if selected_rows:
        try:
            selected_row = dff.iloc[selected_rows[0]]
            center = {"lat": selected_row["lat"], "lon": selected_row["lon"]}
            selected_id = selected_row["id"]
        except IndexError:
            pass

    if click_data:
        clicked_id = click_data["points"][0]["customdata"][0]
        clicked_row = dff[dff["id"] == clicked_id].iloc[0]
        center = {"lat": clicked_row["lat"], "lon": clicked_row["lon"]}
        selected_id = clicked_id

    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        size="chaud_puissance_installee_kW",
        hover_name="nom",
        custom_data=[
            "id",
            "sre",
            "chaud_puissance_installee_kW",
            "chaud_ratio_puiss_inst_W_m2"
        ],
        zoom=11,
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center=center,
        mapbox_zoom=11,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        height=600,
    )

    fig.update_traces(
        marker=dict(
            sizemin=10,
            color=[
                "purple" if i == selected_id else "blue"
                for i in dff["id"]
            ]
        ),
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "SRE: %{customdata[1]:,.0f} m²<br>"
            "Puissance chaud installée: %{customdata[2]:,.0f} kW<br>"
            "Ratio chaud installé: %{customdata[3]:,.1f} W/m²<br>"
            "<extra></extra>"
        ),
    )

    return fig


@callback(
    Output("side-panel", "children"),
    Output("side-panel", "style"),
    Input("building-table", "selected_rows"),
    State("building-table", "derived_virtual_data"),
)
def update_side_panel(selected_rows, rows):
    if not selected_rows or rows is None:
        return [], {
            "position": "absolute",
            "bottom": "0",
            "left": "0",
            "width": "40%",
            "height": "0%",
            "transition": "height 0.3s ease",
            "overflowY": "auto",
            "overflowX": "hidden",
            "backgroundColor": "#f9f9f9",
            "borderTop": "1px solid #ddd",
            "borderRight": "1px solid #ddd",
            "borderBottom": "none",
            "borderLeft": "none",
            "zIndex": "10",
            "boxShadow": "0 -2px 5px rgba(0,0,0,0.1)",
            "borderTopLeftRadius": "12px",
            "borderTopRightRadius": "12px",
        }

    dff_table = pd.DataFrame(rows)
    row_table = dff_table.iloc[selected_rows[0]]
    row = df_buildings[df_buildings["id"] == row_table["id"]].iloc[0]

    style_side_panel_text = {
        "fontSize": "13px",
        "lineHeight": "1.2",
        "color": "#1f388b",
    }

    graph_container_style = {
        "width": "95%",
        "margin": "0 auto",
        "maxWidth": "800px",
    }

    conso_dict_CH = row["chaud_conso_annuelle"]
    conso_dict_FR = row["froid_conso_annuelle"]
    df_conso = pd.DataFrame({
        "Année": list(conso_dict_CH.keys()),
        "Consommation_CH": list(conso_dict_CH.values()),
        "Consommation_FR": list(conso_dict_FR.values())
    })

    fig_conso_ch = px.bar(
        df_conso,
        x="Année",
        y="Consommation_CH",
        title="Consommation annuelle - Chauffage (kWh)",
        text="Consommation_CH",
        color_discrete_sequence=["#C00000"]
    )
    fig_conso_ch.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(title=None),
    )
    fig_conso_ch.update_traces(textposition='outside')

    fig_conso_fr = None
    if row["froid_puissance_installee_kW"] > 0:
        fig_conso_fr = px.bar(
            df_conso,
            x="Année",
            y="Consommation_FR",
            title="Consommation annuelle - Froid (kWh)",
            text="Consommation_FR",
            color_discrete_sequence=["#00B0F0"]
        )
        fig_conso_fr.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(title=None),
        )
        fig_conso_fr.update_traces(textposition='outside')

    content = html.Div(
        children=[
            html.H1(row["nom"], style={"fontSize": "24px", "fontWeight": "bold","textAlign": "center"}),
            html.P(
                [html.Strong("EGID: "), row["egid"]],
                style=style_side_panel_text
            ),
            html.P(
                [html.Strong("SRE: "), f"{row['sre']:,} m²".replace(",", " ")],
                style=style_side_panel_text
            ),
            html.P(
                [html.Strong("Affectation: "), row["affectations"]],
                style=style_side_panel_text
            ),

            html.Div([
                html.H4("🔥 Chaud", style={"color": "#C00000", "fontSize": "17px"}),
                html.P(
                    [html.Strong("Producteur: "), row["chaud_producteur"]],
                    style=style_side_panel_text
                ),
                html.P(
                    [html.Strong("Puissance installée: "),
                     f"{row['chaud_puissance_installee_kW']:,} kW".replace(",", " ")],
                    style=style_side_panel_text
                ),
                html.P(
                    [html.Strong("Ratio puissance installée: "), f"{row['chaud_ratio_puiss_inst_W_m2']} W/m²"],
                    style=style_side_panel_text
                ),
                html.Div(
                    dcc.Graph(
                        figure=fig_conso_ch,
                        config={"displayModeBar": False, "responsive": True},
                        style={"width": "100%"}
                    ),
                    style=graph_container_style,
                ),
            ], style={"marginBottom": "15px"}),

            html.Div([
                html.H4("❄️ Froid", style={"color": "#00B0F0", "fontSize": "17px"}),
                html.P(
                    [html.Strong("Producteur: "), row["froid_producteur"]],
                    style=style_side_panel_text
                ),
                html.P(
                    [html.Strong("Puissance installée: "),
                     f"{row['froid_puissance_installee_kW']:,} kW".replace(",", " ")],
                    style=style_side_panel_text
                ),
                html.Div(
                    dcc.Graph(
                        figure=fig_conso_fr,
                        config={"displayModeBar": False, "responsive": True},
                        style={"width": "100%"}
                    ),
                    style=graph_container_style,
                ),
            ], style={"marginBottom": "15px"}) if fig_conso_fr else None,
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "gap": "15px",
            "padding": "15px",
            **CARD_STYLE,
            "minWidth": "350px",
            "maxWidth": "500px",
            "maxHeight": "70vh",
            "overflowY": "auto",
        },
    )

    style = {
        "position": "absolute",
        "bottom": "0",
        "left": "0",
        "width": "40%",
        "height": "70%",
        "transition": "height 0.3s ease",
        "overflowY": "auto",
        "overflowX": "hidden",
        "backgroundColor": "#f9f9f9",
        "borderTop": "1px solid #ddd",
        "borderRight": "1px solid #ddd",
        "borderBottom": "none",
        "borderLeft": "none",
        "zIndex": "10",
        "boxShadow": "0 -2px 5px rgba(0,0,0,0.1)",
        "borderTopLeftRadius": "12px",
        "borderTopRightRadius": "12px",
    }

    return content, style


@callback(
    Output("building-table", "selected_rows"),
    Input("building-map", "clickData"),
    State("building-table", "derived_virtual_data"),
)
def select_row_from_map(clickData, rows):
    if not clickData or rows is None:
        return []

    clicked_id = clickData["points"][0]["customdata"][0]
    df_rows = pd.DataFrame(rows)

    return df_rows.index[df_rows["id"] == clicked_id].tolist()

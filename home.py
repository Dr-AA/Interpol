from dash import html, dcc, dash_table, Input, Output, State, callback
import plotly.express as px
import pandas as pd
from navbar import create_navbar

# =====================================================
# Constants
# =====================================================
GENEVA_CENTER = {"lat": 46.2044, "lon": 6.1432}

nav = create_navbar()

# =====================================================
# Example buildings in Geneva
# =====================================================
df_buildings = pd.DataFrame({
    "id": [0, 1, 2,3,4,5],

    # ---------- Identification ----------
    "nom": [
        "L'Atelier",
        "TPG Bachet",
        "La Praille",
        "JTI","Campus Biotech","Cité Léopard"
    ],
    "egid": ["295165454", "2040608", "295020439","295161133","295020439","295020439"],
    "sre": [33350, 36614, 52909,25263,50000,50000],
    "affectations": ["Industrie 60%-Administration 30%-Commerces 10%",
                     "Dépôt TPG", "Centre commercial-Hôtel","Administration","Laboratoires","Logements"],

    # ---------- Construction ----------
    "surface_enveloppe": [15587, 21189, 32478,32478,50000,50000],
    "type_construction": ["Mi-lourde", "légère", "légère","Mi-lourde","légère","Mi-lourde"],

    # ---------- Chaud ----------
    "chaud_producteur": ["CAD Ziplo", "CAD SIG", "CCF gaz-Chaudière gaz-chaudière mazout","CAD SIG","CAD SIG","CAD SIG"],
    "chaud_puissance_installee_kW": [750, 2600, 2915,1500,3500,3500],
    "chaud_ratio_puiss_inst_W_m2": [17, 71, 55, 60, 60, 60],
    "chaud_puissance_max": [700, 2000, 1500, 1000, 1000, 1000],
    "chaud_conso_annuelle": [921520, 2805000, 2815000, 1500000, 1500000, 1500000],
    "chaud_ratio_conso": [27.6, 76.6, 53, 40, 40, 40],
    "chaud_type_emetteurs": ["ventilo-convecteurs", "ventilo-convecteurs-radiateurs-monoblocs",
                             "ventilo-convecteurs-radiateurs-monoblocs","ventilo-convecteurs","ventilo-convecteurs",
                             "planchers chauffants"],

    # ---------- Froid ----------
    "froid_producteur": ["FAD Ziplo", "PAC aérotherme", "GF à vis","FAD SIG","FAD SIG"," "],
    "froid_puissance_installee_kW": [850, 315, 3800,2000,2000,0],
    "froid_ratio_surfacique_W_m2": [19.2, 0, 72,50,50,0],
    "froid_puissance_max": [500, 0, 2400,2000,2000,0],
    "froid_conso_annuelle": [584330, 0, 2540000,1500000,1500000,0],
    "froid_ratio_conso": [17.5, 0, 48,48,48,0],
    "froid_type_emetteurs": ["ventilo-convecteurs", "ventilo-convecteurs-monoblocs",
                             "ventilo-convecteurs-monoblocs","ventilo-convecteurs","ventilo-convecteurs"," "],

    # ---------- Map (Geneva) ----------
    "lat": [46.1658, 46.1750, 46.1803,46.2226,46.2221,46.1839],
    "lon": [6.1090, 6.1320, 6.1286,6.1460,6.1486,6.1445],
})

# =====================================================
# Page layout
# =====================================================
def create_page_home():
    return html.Div(
        [
            nav,

            html.Div(
                style={
                    "height": "calc(100vh - 60px)",
                    "display": "flex",
                    "flexDirection": "column",
                },
                children=[

                    # ================== TABLE ==================
                    html.Div(
                        style={"height": "40%", "padding": "10px"},
                        children=[
                            dash_table.DataTable(
                                id="building-table",
                                data=df_buildings.to_dict("records"),
                                row_selectable="single",
                                row_deletable=False,
                                selected_rows=[],
                                active_cell=None,
                                filter_action="native",
                                sort_action="native",
                                page_action="none",
                                merge_duplicate_headers=True,

                                columns=[
                                    {"name": ["", "Nom"], "id": "nom"},
                                    {"name": ["", "EGID"], "id": "egid"},
                                    {"name": ["", "SRE"], "id": "sre"},
                                    {"name": ["", "Affectations"], "id": "affectations"},
                                    {"name": ["", "Surface enveloppe"], "id": "surface_enveloppe"},
                                    {"name": ["", "Type Construction"], "id": "type_construction"},

                                    {"name": ["Chaud", "Producteur"], "id": "chaud_producteur"},
                                    {"name": ["Chaud", "Puissance Installée (kW)"], "id": "chaud_puissance_installee_kW"},
                                    {"name": ["Chaud", "Ratio Surfacique – Puiss Instal"], "id": "chaud_ratio_puiss_inst_W_m2"},
                                    {"name": ["Chaud", "Puissance Max atteinte"], "id": "chaud_puissance_max"},
                                    {"name": ["Chaud", "Conso Annuelle"], "id": "chaud_conso_annuelle"},
                                    {"name": ["Chaud", "Ratio Surf conso"], "id": "chaud_ratio_conso"},
                                    {"name": ["Chaud", "Type émetteurs"], "id": "chaud_type_emetteurs"},

                                    {"name": ["Froid", "Producteur"], "id": "froid_producteur"},
                                    {"name": ["Froid", "Puissance Installée (kW)"], "id": "froid_puissance_installee_kW"},
                                    {"name": ["Froid", "Ratio Surfacique"], "id": "froid_ratio_surfacique_W_m2"},
                                    {"name": ["Froid", "Puissance Max atteinte"], "id": "froid_puissance_max"},
                                    {"name": ["Froid", "Conso Annuelle"], "id": "froid_conso_annuelle"},
                                    {"name": ["Froid", "Ratio Surf conso"], "id": "froid_ratio_conso"},
                                    {"name": ["Froid", "Type émetteurs"], "id": "froid_type_emetteurs"},
                                ],

                                style_data_conditional=[
                                   {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "#d6eaff",
                                    },
                                ],

                                style_table={
                                    "height": "100%",
                                    "overflowX": "auto",
                                    "overflowY": "auto",
                                },
                                style_cell={
                                    "padding": "6px",
                                    "textAlign": "center",
                                },
                                style_header={
                                    "fontWeight": "bold",
                                    "textAlign": "center",
                                },
                            )
                        ],
                    ),

                    # ================== MAP ==================
                    html.Div(
                        style={"height": "60%"},
                        children=[
                            dcc.Graph(id="building-map", style={"height": "100%"})
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

@callback(
    Output("building-map", "figure"),
    Input("building-table", "derived_virtual_data"),
    Input("building-table", "selected_rows"),
)
def update_map(filtered_rows, selected_rows):

    dff = df_buildings if filtered_rows is None else pd.DataFrame(filtered_rows)
    center = GENEVA_CENTER

    selected_id = None

    if selected_rows:
        row = dff.iloc[selected_rows[0]]
        selected_id = row["id"]
        center = {"lat": row["lat"], "lon": row["lon"]}

    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        size="chaud_puissance_installee_kW",
        hover_name="nom",
        custom_data=[
            "sre",
            "chaud_puissance_installee_kW",
            "chaud_ratio_puiss_inst_W_m2"
        ]
        ,
        zoom=13,
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center=center,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
        separators=". "
    )

    # Highlight sélection
    fig.update_traces(
        marker=dict(
            sizemin=10,
            color=[
                "purple" if i == selected_id else "blue"
                for i in dff["id"]
            ]
        ),
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "SRE : %{customdata[0]:,.0f} m²<br>" +
        "Puissance chaud installée : %{customdata[1]:,.0f} kW<br>" +
        "Ratio chaud installé : %{customdata[2]:,.1f} W/m²<br>" +
        "<extra></extra>"

    )

    return fig



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

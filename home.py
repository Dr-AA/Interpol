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
        "JTI","Campus Biotech","Cité Léopard"
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
                },
                children=[
                    # ================== TABLE ==================
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
                            merge_duplicate_headers=True,  # Enable merged headers
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
                                "height": "100%",
                                "maxHeight": "100%",
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
                            # Add custom header conditional styling here
                            style_header_conditional=[
                                # Style for top-level merged headers (Général, CHAUD, FROID)
                                {
                                    "if": {"header_index": 0},
                                    "backgroundColor": "rgba(200, 200, 200, 0.9)",
                                    "color": "black",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                    "textAlign": "center",
                                },
                                # Style for CHAUD section columns (bottom level)
                                {
                                    "if": {"column_id": ["chaud_producteur", "chaud_puissance_installee_kW",
                                           "chaud_ratio_puiss_inst_W_m2", "chaud_puissance_max",
                                           "chaud_conso_annuelle", "chaud_ratio_conso", "chaud_type_emetteurs"]},
                                    "backgroundColor": "rgba(204, 0, 0, 0.8)",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                },
                                # Style for FROID section columns (bottom level)
                                {
                                    "if": {"column_id": ["froid_producteur", "froid_puissance_installee_kW",
                                                         "froid_ratio_surfacique_W_m2", "froid_puissance_max",
                                                         "froid_conso_annuelle", "froid_ratio_conso", "froid_type_emetteurs"]},
                                    "backgroundColor": "rgba(0, 128, 255, 0.8)",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "border": "1px solid black",
                                },
                                # Style for Général section columns (bottom level)
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
                        "flex": "1",
                        "minWidth": "500px",
                        "display": "flex",
                        "flexDirection": "column",
                        "overflow": "hidden"
                    }),
                    # ================== PANEL AND MAP ==================
                    html.Div(
                        children=[
                            # SIDE PANEL
                            html.Div(
                                id="side-panel",
                                style={
                                    "width": "0%",  # hidden by default
                                    "transition": "0.3s",
                                    "overflow": "hidden",
                                    "backgroundColor": "#f9f9f9",
                                    "borderRight": "1px solid #ddd",
                                    "padding": "10px"
                                },
                                children=[]
                            ),
                            # MAP
                            html.Div(
                                id="map-container",
                                style={"width": "100%", "height": "100%"},
                                children=[
                                    dcc.Graph(id="building-map", style={"height": "100%"})
                                ],
                            ),
                        ],
                        style={
                            **CARD_STYLE,
                            "flex": "1",
                            "display": "flex",
                            "overflow": "hidden"
                        }
                    )

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
    Input("building-table", "selected_rows"),  # Table selection
    Input("building-map", "clickData"),  # Map click
    State("building-table", "derived_virtual_data"),  # Current filtered rows from table
    State("building-map", "figure"),  # Current map figure state
)
def update_map(selected_rows, click_data, filtered_rows, current_map_fig):
    """
    Callback to update the map's center when either a row is selected or a point is clicked.
    """

    # DataFrame from DataTable or fallback to full dataset if none
    dff = pd.DataFrame(filtered_rows) if filtered_rows else df_buildings

    # Default to Geneva Center if no selection is made
    center = GENEVA_CENTER
    selected_id = None

    # Handle table row selection
    if selected_rows:
        try:
            selected_row = dff.iloc[selected_rows[0]]  # Get first selected row
            center = {"lat": selected_row["lat"], "lon": selected_row["lon"]}
            selected_id = selected_row["id"]
        except IndexError:
            pass  # In case selected_rows is out of sync

    # Handle map click selection
    if click_data:
        clicked_id = click_data["points"][0]["customdata"][0]  # Extract ID from clicked point
        clicked_row = dff[dff["id"] == clicked_id].iloc[0]
        center = {"lat": clicked_row["lat"], "lon": clicked_row["lon"]}
        selected_id = clicked_id

    # Create the map figure
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
        zoom=13,
    )

    # Update map layout with new center and zoom
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center=center,  # Center updated dynamically
        mapbox_zoom=14,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    # Highlight the point corresponding to the selection
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
        # ✅ HIDE SIDE PANEL (par défaut)
        return [], {
            "width": "0%",
            "transition": "0.3s",
            "overflow": "hidden",
        }

    # Récupérer les données de la ligne sélectionnée
    dff_table = pd.DataFrame(rows)
    row_table = dff_table.iloc[selected_rows[0]]
    row = df_buildings[df_buildings["id"] == row_table["id"]].iloc[0]

    # Styles pour le texte dans le panneau
    style_side_panel_text = {
        "fontSize": "13px",  # Taille réduite d'1 point
        "lineHeight": "1.2",  # Espacement entre lignes
        "color": "#1f388b",  # Uniformiser la couleur
    }

    # Style du conteneur pour recentrer et limiter la largeur des graphiques
    graph_container_style = {
        "maxWidth": "90%",  # 🔄 Réduit la largeur des graphiques à 90% de la largeur du panel
        "margin": "0 auto",  # 🔄 Centre horizontalement
    }

    # Préparer le graphique pour les consommations
    conso_dict_CH = row["chaud_conso_annuelle"]
    conso_dict_FR = row["froid_conso_annuelle"]
    df_conso = pd.DataFrame({
        "Année": list(conso_dict_CH.keys()),
        "Consommation_CH": list(conso_dict_CH.values()),
        "Consommation_FR": list(conso_dict_FR.values())
    })

    # Graphe des consommations de chauffage
    fig_conso_ch = px.bar(
        df_conso,
        x="Année",
        y="Consommation_CH",
        title="Consommation annuelle - Chauffage (kWh)",
        text="Consommation_CH",
        color_discrete_sequence=["#C00000"]
    )
    fig_conso_ch.update_layout(
        height=220,  # 🔄 Réduction de la hauteur
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(title=None),  # Supprimer le titre de l'axe Y
    )

    # Graphe des consommations de refroidissement
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
            height=220,  # 🔄 Réduction de la hauteur
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(title=None),  # Supprimer le titre de l'axe Y
        )

    # Création du contenu du panneau latéral
    content = html.Div(
        children=[
            # Titre du site
            html.H1(row["nom"], style={"fontSize": "24px", "fontWeight": "bold","textAlign": "center"}),  # Reduced overall size
            html.P(
                [html.Strong("EGID: "), row["egid"]],  # Bold EGID label
                style=style_side_panel_text
            ),
            html.P(
                [html.Strong("SRE: "), f"{row['sre']:,} m²".replace(",", " ")],  # Bold SRE label
                style=style_side_panel_text
            ),
            html.P(
                [html.Strong("Affectation: "), row["affectations"]],  # Bold Affectation label
                style=style_side_panel_text
            ),

            # Carte sur Chaud
            html.Div([
                html.H4("🔥 Chaud", style={"color": "#C00000", "fontSize": "17px"}),  # Theme-specific heading
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
                    dcc.Graph(figure=fig_conso_ch),
                    style=graph_container_style,  # Centre and limit graphic width
                ),
            ], style={"marginBottom": "15px"}),

            # Carte sur Froid (only shown if data is available)
            html.Div([
                html.H4("❄️ Froid", style={"color": "#00B0F0", "fontSize": "17px"}),  # Theme-specific heading
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
                    dcc.Graph(figure=fig_conso_fr),
                    style=graph_container_style,  # Centre and limit graphic width
                ),
            ], style={"marginBottom": "15px"}) if fig_conso_fr else None,
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "gap": "15px",  # Added spacing between sections
            **CARD_STYLE,
        },
    )

    # Modifier le style de la barre latérale
    style = {
        "width": "40%",
        "transition": "0.3s",
        "overflowY": "auto",
        "padding": "1px",
        "backgroundColor": "#f9f9f9",
        "borderRight": "1px solid #ddd",
    }

    return content, style





@callback(
    Output("map-container", "style"),
    Input("building-table", "selected_rows"),
)
def resize_map(selected_rows):

    if selected_rows:
        return {"width": "60%", "height": "100%"}
    else:
        return {"width": "100%", "height": "100%"}

@callback(
    Output("building-table", "selected_rows"),  # Select the corresponding table row
    Input("building-map", "clickData"),  # When a map point is clicked
    State("building-table", "derived_virtual_data"),  # Current table data
)
def select_row_from_map(clickData, rows):
    """
    Callback to select a corresponding table row when a map point is clicked.
    """
    # No click data or no rows in the table
    if not clickData or rows is None:
        return []

    # Extract the ID of the clicked point
    clicked_id = clickData["points"][0]["customdata"][0]
    df_rows = pd.DataFrame(rows)

    # Find the index of the ID in the table's rows
    return df_rows.index[df_rows["id"] == clicked_id].tolist()
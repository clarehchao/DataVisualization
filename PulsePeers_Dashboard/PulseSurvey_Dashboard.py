from dash import html, Dash, page_container, page_registry
import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import load_figure_template

app = Dash(__name__,
           external_stylesheets=[dbc.themes.LITERA],
           assets_folder='assets',
           use_pages=True)

# load_figure_template('LITERA')

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"])) for page in page_registry.values()
    ],
    brand="Pulse Survey Dashboard",
    brand_href="/",
    color="primary",
    className="mb-4"
    # dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.A("Clare Chao | GitHub", href="https://github.com/clarehchao/DataVisualization"),
                align="left"),
        ],
    ),
    className="footer",
    fluid=True,
)

# content = html.Div(id="page-content", className="container mt-4")

# Overall layout
app.layout = html.Div([
    navbar,  # Include the navigation bar
    dbc.Container(
        page_container,
        className="mb-4"
    ),
    footer,  # Include the footer
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8011)
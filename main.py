import os
import sys

# Mock comm module to prevent Jupyter initialization errors when running as standalone script
class MockComm:
    def create_comm(self, *args, **kwargs):
        return None

sys.modules['comm'] = MockComm()

# Import necessary libraries
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import page1

# Connect the navbar to the index
from components import navbar

# Define default graphs so they appear consistent whether empty of with data plotted
empty_gene_histogram = px.histogram(
    [],
    range_x=[-10, 100],
    nbins=1000,
    title=f'Histogram of ΔΔG values for selected gene',
    template="plotly_white",
)
empty_gene_histogram.update_yaxes(showticklabels=False, title="Frequency")
empty_gene_histogram.update_xaxes(showgrid=False, title="ΔΔG (kcal/mol)")

empty_variant_histogram = px.histogram(
    [],
    range_x=[-10, 100],
    nbins=20,
    title='Histogram of ΔΔG values for selected variant',
    labels={'x': 'ΔΔG (kcal/mol)', 'y': 'Frequency'},
    template="plotly_white",
)
empty_variant_histogram.update_yaxes(showticklabels=False, title="Frequency")
empty_variant_histogram.update_xaxes(showgrid=False, title="ΔΔG (kcal/mol)")


# Define the navbar
nav = navbar.Navbar()

# expose the server for gunicorn
server = app.server

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

@app.callback(
    Output(component_id = "residual_selected", component_property = "options"),
    Input('gene_selected', 'value'),
    prevent_initial_call=True,
)
def update_dropdown_page1_2a(gene_selected):
    dropdownlist = page1.set_dropdown_options_page1_2a(gene_selected)
    return dropdownlist

@app.callback(
    Output(component_id = "mutfrom_selected", component_property = "options"),
    [Input(component_id = "gene_selected", component_property = "value"),
     Input(component_id = "residual_selected", component_property = "value")],
    prevent_initial_call=True,
)
def update_dropdown_page1_2b(gene_selected, residual_selected):
    dropdownlist = page1.set_dropdown_options_page1_2b(gene_selected, residual_selected)
    return dropdownlist


@app.callback(
    Output(component_id = "mutto_selected", component_property = "options"),
    [Input(component_id = "gene_selected", component_property = "value"),
     Input(component_id = "residual_selected", component_property = "value"),
     Input(component_id = "mutfrom_selected", component_property = "value")],
    prevent_initial_call=True,
)
def update_dropdown_page1_2c(gene_selected, residual_selected, mutfrom_selected):
    dropdownlist = page1.set_dropdown_options_page1_2c(gene_selected, residual_selected, mutfrom_selected)
    return dropdownlist


@app.callback(
    [Output(component_id = "gene_ddg", component_property = "figure"),
     Output(component_id = "variant_ddg", component_property = "figure"),
     Output(component_id = "gene_ddg_markdown", component_property = "children")],
    [Input(component_id = "gene_selected", component_property = "value"),
     Input(component_id = "residual_selected", component_property = "value"),
     Input(component_id = "mutfrom_selected", component_property = "value"),
     Input(component_id = "mutto_selected", component_property = "value")],
)
def update_graphs_and_markdown(gene_selected, residual_selected, mutfrom_selected, mutto_selected):
    if None in {mutto_selected, gene_selected, residual_selected, mutfrom_selected}:
        return [
            empty_gene_histogram,
            empty_variant_histogram,
            "",
        ]

    gene_pdbs = page1.gene_pdbs
    pdb_values = page1.get_pdb_values(gene_pdbs, gene_selected)
    median_ddg = page1.calculate_median(pdb_values,residual_selected, mutfrom_selected, mutto_selected)
    percentile = page1.calculate_percentile(pdb_values, residual_selected, mutfrom_selected, mutto_selected)

    gene_figure = page1.ddg_for_gene_plot(gene_selected, pdb_values, median_ddg)
    variant_figure = page1.ddg_for_variant_plot(pdb_values, residual_selected, mutfrom_selected, mutto_selected)
    text = page1.gene_ddg_markdown_text(median_ddg, percentile)

    return [gene_figure, variant_figure, text]


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/page1':
        return page1.layout
    else:  # if redirected to unknown link
        return "404 Page Error! Please choose a link"

# Run the app on localhost:8050 by default
if __name__ == '__main__':
    os.environ["host"]  = os.environ.get("host", default="localhost")
    os.environ["port"] = os.environ.get("port", default="8050")
    os.environ["dash_debug"] = os.environ.get("dash_debug", default="True")
    app.run_server()

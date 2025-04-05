import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
from flask import Flask, render_template

volcano_df = pd.read_excel("assets/gene_data.xlsx", sheet_name="S4B limma results", header=2)
volcano_df["neg_log10_adjP"] = -np.log10(volcano_df["adj.P.Val"] + 1e-10)

volcano_fig = px.scatter(
    volcano_df,
    x="logFC",
    y="neg_log10_adjP",
    hover_data=["EntrezGeneSymbol", "TargetFullName"],
    custom_data=["EntrezGeneSymbol"],
    title="Interactive Volcano Plot of Protein Activity Differences",
    labels={"logFC": "Log Fold Change", "neg_log10_adjP": "-log10(adj.P.Val)"},
)

server = Flask(__name__)

dash_app = dash.Dash(__name__, server=server, url_base_pathname="/dash/")
dash_app.layout = html.Div([dcc.Graph(id="volcano-plot", figure=volcano_fig), dcc.Graph(id="boxplot")])


@server.route("/")
def index():
    return render_template("index.html")


# output - changes figure of boxpot, input - volcano plot click data from a click event
@dash_app.callback(Output("boxplot", "figure"), [Input("volcano-plot", "clickData")])
def update_boxplot(clickData):
    if clickData is None:
        return px.box(title="Click a point on the volcano plot to see details.")

    gene = clickData["points"][0]["customdata"][0]

    df_values = pd.read_excel("assets/gene_data.xlsx", sheet_name="S4A values", header=2)
    gene_data = df_values[df_values["EntrezGeneSymbol"] == gene]
    if gene_data.empty:
        return px.box(title=f"No data for gene {gene}")

    # columns of donors
    donor_columns = [column for column in gene_data.columns if "OD" in column or "YD" in column]

    # need to melt the dataframe to long format for boxplot
    donor_data_long = gene_data[donor_columns].melt(var_name="Sample", value_name="Protein Concentration")

    donor_data_long["Age Group"] = donor_data_long["Sample"].apply(determine_age_group)

    fig_box = px.box(
        donor_data_long,
        x="Age Group",
        y="Protein Concentration",
        points="all",
        title=f"Protein Concentration for {gene}",
    )
    return fig_box


def determine_age_group(sample):
    if "OD" in sample:
        return "Old"
    elif "YD" in sample:
        return "Young"
    else:
        return "Unknown"


if __name__ == "__main__":
    server.run(debug=True)

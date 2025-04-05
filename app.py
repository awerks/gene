import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

volcano_df = pd.read_excel("assets/gene_data.xlsx", sheet_name="S4B limma results", header=2)
volcano_df["neg_log10_adjP"] = -np.log10(volcano_df["adj.P.Val"] + 1e-10)

app = dash.Dash(__name__)

volcano_fig = px.scatter(
    volcano_df,
    x="logFC",
    y="neg_log10_adjP",
    hover_data=["EntrezGeneSymbol", "TargetFullName"],
    custom_data=["EntrezGeneSymbol"],
    title="Interactive Volcano Plot of Protein Activity Differences",
    labels={"logFC": "Log Fold Change", "neg_log10_adjP": "-log10(adj.P.Val)"},
)

app = dash.Dash(__name__)

app.layout = html.Div([dcc.Graph(id="volcano-plot", figure=volcano_fig)])


if __name__ == "__main__":
    app.run(debug=True)

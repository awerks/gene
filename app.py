from flask import Flask, render_template
import pandas as pd
import dash_bio

app = Flask(__name__)


@app.route("/")
def index():
    return volcano_plot().to_html()


def volcano_plot():
    df = pd.read_excel("assets/gene_data.xlsx", sheet_name="S4B limma results", header=2)

    # https://plotly.com/python/volcano-plot/

    return dash_bio.VolcanoPlot(
        dataframe=df,
        snp="id",
        effect_size="logFC",
        p="adj.P.Val",
        gene="EntrezGeneSymbol",
        logp=True,
        title="Volcano Plot",
    )


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import sys

app = Flask(__name__)


def load_data(year=None, month=None):
    # Lê o CSV usando Pandas:
    df = pd.read_csv("https://pycourse.s3.amazonaws.com/bike-sharing.csv")
# Filtra o dataframe por ano:
    if year is not None:
        df = df[df["year"] == year]
# Filtra o dataframe por mês:
    if month is not None:
        df = df[df["month"] == month]
    return df


def get_totals(year=None, month=None):
    df = load_data(year, month)  # dataframe com o histórico de locações
    total = df['total_count'].sum()
    total11 = df[df.year == 0].total_count.sum()
    total12 = df[df.year == 1].total_count.sum()
    return [
        {"title": "Locações", "total": total},
        {"title": "Locações em 2011", "total": total11},
        {"title": "Locações em 2012", "total": total12},
    ]


def get_top3_hours(year=None, month=None):
# Dataframe com o histórico de locações:
    df = load_data(year, month)
# Agrupa média de locações por horário do dia:
    df_agg = df.groupby(["hour"]).agg(media=("total_count", "mean")).reset_index()
# Ordenar horários de locações pela média, maior -> menor:
    df_agg_sort = df_agg.sort_values(by="media", ascending=False)
# Top 3 horários com maiores locações:
    df_agg_top3 = df_agg_sort.head(3)
# Converte o dataframe em um dicionário Python:
    top3 = df_agg_top3.to_dict("records")
    return top3



@app.route("/", methods=['GET'])
@app.route("/")
def home():
    totals = get_totals()
    total_fields = ["title", "Locações", "total"]
    hours = get_top3_hours() 
    month=request.args.get('month',type=int)
    year=request.args.get('year',type=int)
    month=get_top3_hours(month)
    year=get_top3_hours(year)
    return render_template('index.html',
                           totals=totals,
                           total_fields=total_fields,
                           hours=hours,month=month,year=year
                           )



@app.route('/month/', methods=['GET', 'POST'])
def month1():
    mid= request.args.get('month',type=int)
    month=get_top3_hours()
    return mid


@ app.route('/year/', methods=['GET', 'POST'])
def year1():
    yid = request.args.get('year',type=int)
    year=get_top3_hours()
    return yid 

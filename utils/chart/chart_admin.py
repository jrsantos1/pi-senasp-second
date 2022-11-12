from utils.data.admin import *
import plotly
import plotly.express as px
import json

def get_grafico_movimentacoes():
    data, valor = get_movimentacoes()
    
    x = valor
    y = data
    
    fig = px.line(x = x or [0], y = y or [0], title='Volume de transações R$' )
    
    grafico = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return grafico
import requests as reque
import pandas as pd 
import locale

requisicao = reque.get("http://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL")
requisicao_dic = requisicao.json()

valort_inicial = float(requisicao_dic['USDBRL']['varBid']) / 100
formart_local = locale.format_string('%.2f%%', valort_inicial*100, grouping=True)
format = formart_local.replace('.',',')

def format_percent(value):
    valort_inicial = float(value) / 100
    formart_local = locale.format_string('%.2f%%', valort_inicial*100, grouping=True)
    format = formart_local.replace('.',',')
    return format

def get_cotacoes():

    cotacoes = {
        'dolar': {
            'today': float(requisicao_dic['USDBRL']['bid']),
            'var': format_percent(requisicao_dic['USDBRL']['pctChange'])
        },
        'euro': {
            'today': float(requisicao_dic['EURBRL']['bid']),
            'var': format_percent(requisicao_dic['EURBRL']['pctChange'])
        },
        'bitcoin': {
            'today': float(requisicao_dic['BTCBRL']['bid']) * 1000,
            'var': format_percent(requisicao_dic['BTCBRL']['pctChange'])
        }    
    }
    
    return cotacoes; 




import sys
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import logging.handlers
import datetime
import os.path

class Anuncio:
    
    def __init__(self,id,url,titulo=None,preco=None,ano=None,km=None,cor=None,cambio=None,portas=None,acessorio=None,info_veiculo=None):
        self.__id = str(id)
        self.__url = str(url)
        self.__titulo = str(titulo)
        self.__preco = str(preco)
        self.__ano = str(ano)
        self.__km = str(km)
        self.__cor = str(cor)
        self.__cambio = str(cambio)
        self.__portas = str(portas)  
        self.__acessorio = str(acessorio)
        self.__info_veiculo = str(info_veiculo)
        self.__data_inicio =  datetime.datetime.now()
        self.__data_fim = None
    
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = str(value)

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = str(value)

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        self.__titulo = str(value)

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, value):
        self.__preco = str(value)        

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, value):
        self.__ano = str(value)          

    @property
    def km(self):
        return self.__km

    @km.setter
    def km(self, value):
        self.__km = str(value)  

    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self, value):
        self.__cor = str(value)   

    @property
    def cambio(self):
        return self.__cambio

    @cambio.setter
    def cambio(self, value):
        self.__cambio = str(value)

    @property
    def portas(self):
        return self.__portas

    @portas.setter
    def portas(self, value):
        self.__portas = str(value)

    @property
    def acessorio(self):
        return self.__acessorio

    @acessorio.setter
    def acessorio(self, value):
        self.__acessorio = str(value) 

    @property
    def info_veiculo(self):
        return self.__info_veiculo

    @info_veiculo.setter
    def info_veiculo(self, value):
        self.__info_veiculo = str(value)

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        self.__data_inicio = value

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, value):
        self.__data_fim = value

a = Anuncio('dasd','assda')        
a.acessorio='dsfs'


class Classe:
    def __init__(self, nome, idade):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value
    


a = Classe('s', 'd')        
a.nome='sad'
print(a.nome)


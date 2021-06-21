my_dict = {}

class Tick:
    ticks_count = 0 # this is supposed to hold the number of ticks we have instanced an object for

    def __init__(self, identifier, macro):
        self.identifier = identifier # creates an attribute called identifier and assigns to it
                                     # the value of the "identifier" parameter
        self.macro = macro           # creates an attribute called macro and assigns to it the
                                     # value of the "macro" parameter
        self.count = 0

        my_dict[macro] = identifier

    def __str__(self):
        pass

    def increaseCounter(self):
        self.count += 1
    
#TODO: gestire gli input scorretti nel costruttore
#TODO: funzionalità del costruttore che aggiunge il pair macro:istanza al dizionario
#TODO: funzione che prenda in parametro la combinazione, verifichi che sia presente nel dizionario,
#      che quindi chiami indIncreaseCounter con parametro il "value" corrispondente alla "key" (combinazione)
def indIncreaseCounter(tickInstance):
    tickInstance.increaseCounter()
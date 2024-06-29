import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._squadraScelta = None

    def inserisciAnni(self):
        allAnni = self._model.getAllAnni()
        for a in allAnni:
            self._view._ddAnno.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def handleTextArea(self, e):
        anno = self._view._ddAnno.value
        squadreAnno = self._model.getSquadreAnno(anno)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno {anno}: {len(squadreAnno)}"))
        for s in squadreAnno:
            self._view._txtOutSquadre.controls.append(ft.Text(s.teamCode))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=s, text=s.teamCode, on_click= self.readDDSquadra))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text(f"Seleziona un anno dal menù."))
            return
        anno = self._view._ddAnno.value
        self._model.buildGraph(anno)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodes()} vertici e {self._model.getNumEdges()} archi."))
        self._view.update_page()

    def readDDSquadra(self, e):
        if e.control.data is None:
            self._squadraScelta = None
        else:
            self._squadraScelta = e.control.data


    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        tupla = self._model.getVicine(self._squadraScelta)
        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {self._squadraScelta.name}"))
        for t in tupla:
            self._view._txt_result.controls.append(ft.Text(f"{t[1]}-{t[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        if self._squadraScelta == None:
            warnings.warn("Squadra non selezionata")
            self._view._txt_result.controls.append(ft.Text(f"Squadra non selezionata."))

        percorso = self._model.getPathPesoMax(self._squadraScelta)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato."))
        for p in percorso:
            self._view._txt_result.controls.append(ft.Text(f"{p[0]} -- {p[1]}"))

        self._view.update_page()
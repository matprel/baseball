import copy
import itertools

import networkx as nx
from networkx import NetworkXError

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._soluzioneBest = []
        self._pesoBest = 0


    def getPathPesoMax(self, v0):
        self._soluzioneBest = []
        self._pesoBest = 0
        parziale = [v0]
        listaVicini = []
        for v in self._grafo.neighbors(v0):
            edgeV = self._grafo[v0][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1], reverse=True)

        parziale.append(listaVicini[0][0])
        self.ricorsioneV2(parziale)
        parziale.pop()

        #return self._soluzioneBest

        self.ricorsioneV2(parziale)
        return self.getWeightsOfPath(self._soluzioneBest)


    def ricorsione(self, parziale):
        if self.getScore(parziale)> self._pesoBest:
            self._soluzioneBest = copy.deepcopy(parziale)
            self._pesoBest = self.getScore(parziale)
        else:
            for n in self._grafo.neighbors(parziale[-1]):
                edgeW = self._grafo[parziale[-1]][n]["weight"]
                if n not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > edgeW:
                    parziale.append(n)
                    self.ricorsione(parziale)
                    parziale.pop()

    def ricorsioneV2(self, parziale):
        if self.getScore(parziale)> self._pesoBest:
            self._soluzioneBest = copy.deepcopy(parziale)
            self._pesoBest = self.getScore(parziale)
        else:
            listaVicini = []
            for n in self._grafo.neighbors(parziale[-1]):
                edgeV = self._grafo[parziale[-1]][n]["weight"]
                listaVicini.append((n,edgeV))
            listaVicini.sort(key = lambda x:x[1], reverse=True)
            for v1 in listaVicini:
                if v1[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v1[1]:
                    parziale.append(v1[0])
                    self.ricorsione(parziale)
                    parziale.pop()
                    return

    def getScore(self, listOfNodes):

        if len(listOfNodes) == 1:
            return 0

        score = 0
        for i in range(0, len(listOfNodes) - 1):
            score += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return score

    def getWeightsOfPath(self, path):
        listTuples = [(path[0], 0)]
        for i in range(0, len(path) - 1):
            listTuples.append((path[i + 1], self._grafo[path[i]][path[i + 1]]["weight"]))

        return listTuples

    def getAllAnni(self):
        squadre = DAO.getAllSquadre()
        anni = []
        for s in squadre:
            if s.year not in anni:
                anni.append(s.year)
        return anni

    def getSquadreAnno(self, anno):
        squadre = DAO.getAllSquadre()
        squadreAnno = []
        for s in squadre:
            if s.year == int(anno):
                squadreAnno.append(s)
        return squadreAnno

    def buildGraph(self, anno):
        self._grafo.clear()
        self._nodes = self.getSquadreAnno(anno)
        self._idMap = {}
        for node in self._nodes:
            self._idMap[node.ID] = node
        self._grafo.add_nodes_from(self._nodes)

        #modo brutto per aggiungere un arco tra ogni nodo
        for n1 in self._nodes:
            for n2 in self._nodes:
                if n1 != n2:
                    self._grafo.add_edge(n1,n2)

        #altro modo: prendo tutte le combinazioni tra i nodi
        #myedges = list(itertools.combinations(self._nodes, 2)) #lista di tuple
        #self._grafo.add_edges_from(myedges)

        salari = DAO.getSalari(anno, self._idMap)
        for e in self._grafo.edges: #tupla di due nodi
            self._grafo[e[0]][e[1]]["weight"] = salari[e[0]] + salari[e[1]]


    def getVicine(self, squadra):
        vicini = self._grafo.neighbors(squadra)
        tupla = []
        for v in vicini:
            tupla.append((v, self._grafo[squadra][v]["weight"]))
        tupla_ordinata = sorted(tupla, key = lambda x: x[1], reverse = True)
        return tupla_ordinata

    def getNodi(self):
        return self._nodes

    def getNumNodes(self):
        return len(self._nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
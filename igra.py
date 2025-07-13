import copy
import math
import time

from stanje import Stanje


class Game(object):
    # inicijalizacija igre
    def __init__(self):
        self._trenutno_stanje = None
        self._na_redu = 'B'
        self._prestao = False
        self.pocni_igru()

    @property
    def trenutno_stanje(self):
        return self._trenutno_stanje
    @trenutno_stanje.setter
    def trenutno_stanje(self, value):
        self._trenutno_stanje = value
    @property
    def na_redu(self):
        return self._na_redu

    @na_redu.setter
    def na_redu(self, value):
        self._na_redu = value
    @property
    def prestao(self):
        return self._prestao

    @prestao.setter
    def prestao(self, value):
        self._prestao = value

    # formira stanje table i dodeljuje prvi potez crnom igraču
    def pocni_igru(self):
        self._trenutno_stanje = Stanje()
        self._na_redu = 'B'

    def igraj_bot(self, trajanje, pocetna_dubina, stanje):
        trenutna_dubina = pocetna_dubina
        pocetno_vreme = time.time()
        stanja = {}
        sve_mogucnosti = stanje.mogucnosti("W")
        potez = sve_mogucnosti[0]
        for i in range(20):
            rez = self.minimax(stanje, trenutna_dubina, -math.inf, math.inf, True, stanja, pocetno_vreme, trajanje)
            if trenutna_dubina > pocetna_dubina and self._prestao:
                self._prestao = False
                if potez is None:
                    return sve_mogucnosti[0]
                return potez
            else:
                print("Presao dubinu : ", trenutna_dubina)
                potez = rez[1]
                trenutna_dubina += 1
        if potez is None:
            return sve_mogucnosti[0]
        return potez

    def minimax(self, stanje, dubina, alfa, beta, maximize, stanja, pocetno_vreme, trajanje):
        if maximize:
            igrac = "W"
            protivnik = "B"
        else:
            igrac = "B"
            protivnik = "W"
        mogucnosti = stanje.mogucnosti(igrac)
        if (time.time() - pocetno_vreme) > trajanje:
            self._prestao = True
            return self.heuristic(stanje, "W", "B"), None, igrac
        if dubina == 0:
            "ako je doslo do listova vrati heuristicku vrednost stanja"
            if stanje.to_string() in stanja:
                if igrac == stanja[stanje.to_string()][2]:
                    return stanja[stanje.to_string()]
            if stanje.game_over("W"):
                return -200000, None, igrac
            elif stanje.game_over("B"):
                return 200000, None, igrac
            elif stanje.ukupni_poeni() == 64:
                return 0, None, igrac

            stanja[stanje.to_string()] = (self.heuristic(stanje, "W", "B"), None, igrac)
            return stanja[stanje.to_string()]
        if maximize:
            "vrednost cvora"
            vrednost = -math.inf
            najbolja_mogucnost = mogucnosti[0]
            for mogucnost in mogucnosti:
                novo_stanje = copy.deepcopy(stanje)
                novo_stanje.okreni(igrac, mogucnost[0], mogucnost[1])
                poeni = self.minimax(novo_stanje, dubina - 1, alfa, beta, not maximize, stanja, pocetno_vreme, trajanje)
                poeni = poeni[0]
                "trazim najvecu vrendost sve dece tog cvora"
                if poeni > vrednost:
                    vrednost = poeni
                    najbolja_mogucnost = mogucnost
                if vrednost > beta:
                    break
                alfa = max(alfa, vrednost)
            return vrednost, najbolja_mogucnost, igrac
        else:
            vrednost = math.inf
            najbolja_mogucnost = mogucnosti[0]
            for mogucnost in mogucnosti:
                novo_stanje = copy.deepcopy(stanje)
                novo_stanje.okreni(igrac, mogucnost[0], mogucnost[1])
                poeni = self.minimax(novo_stanje, dubina - 1, alfa, beta, not maximize, stanja, pocetno_vreme, trajanje)
                poeni = poeni[0]
                if poeni < vrednost:
                    vrednost = poeni
                    najbolja_mogucnost = mogucnost
                if vrednost < alfa:
                    break
                beta = min(beta, vrednost)
            return vrednost, najbolja_mogucnost, igrac

    def heuristic(self, stanje, igrac, protivnik):
        poeni = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
        score = 0
        "pozicije vec stavljenih diskova"
        for i in range(8):
            for j in range(8):
                # ukoliko naiđe na polje na kome se nalazi disk igrača koji je na potezu onda proverava stanje oko tog polja
                if stanje.board[i][j] == igrac:
                    score += poeni[i][j]
                elif stanje.board[i][j] == protivnik:
                    score -= poeni[i][j]
        ig = 0
        pr = 0
        if stanje.board[0][0] == igrac:
            ig += 1
        elif stanje.board[0][0] == protivnik:
            pr += 1
        if stanje.board[7][7] == igrac:
            ig += 1
        elif stanje.board[7][7] == protivnik:
            pr += 1
        if stanje.board[0][7] == igrac:
            ig += 1
        elif stanje.board[0][7] == protivnik:
            pr += 1
        if stanje.board[7][0] == igrac:
            ig += 1
        elif stanje.board[7][0] == protivnik:
            pr += 1
        "coskovi i mogucnosti"
        if (ig + pr) != 0:
            score += 100 * (ig - pr)
        if (len(stanje.mogucnosti(igrac)) + len(stanje.mogucnosti(protivnik))) != 0:
            score += ((len(stanje.mogucnosti(igrac)) - len(stanje.mogucnosti(protivnik))) / (
                        len(stanje.mogucnosti(igrac)) + len(stanje.mogucnosti(protivnik))))
        "broj diskova za svakog igraca"
        diskovi = stanje.poeni()
        score += 10 * (diskovi[1] - diskovi[0]) / (diskovi[0] + diskovi[1])
        return score

    # omogućuje da se svaki potez odigra i dedeljuje poteze igračima (smenjuje belog i crnog igrača)
    def promeni(self, red, kolona, prozor):
        start_time = time.time()
        if self._na_redu == 'B':
            self._trenutno_stanje.igraj(red, kolona, self._na_redu)
            self._na_redu = 'W'
        elif self._na_redu == 'W':
            potez = self.igraj_bot(3, 4, self._trenutno_stanje)
            self._trenutno_stanje.igraj(potez[0], potez[1], self._na_redu)
            self._na_redu = 'B'
            print("--- %s sekundi ---" % (time.time() - start_time))
            # utvrđuje da li je kraj igre
        if self._trenutno_stanje.game_over(self._na_redu):
            self._trenutno_stanje.pobednik()

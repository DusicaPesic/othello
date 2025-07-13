# kreiranje matrice (table) sa dva crna i dva bela diska u centru
class Stanje(object):
    def __init__(self):
        self._board = []
        for i in range(0, 8):
            self._board.append(8 * ['-'])

        self._board[3][3] = 'W'
        self._board[4][4] = 'W'
        self._board[3][4] = 'B'
        self._board[4][3] = 'B'

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    # određuje protivnika
    def protivnik(self, n):
        if n == "B":
            return "W"
        elif n == "W":
            return "B"
        else:
            return "-"

    # određuje da li je neko polje na tabli
    def natabli(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        else:
            return False

    # funkcija mogucnosti prolazi kroz tablu i redom za svako polje na kome se nalazi disk igrača koji je trenutno
    # na potezu određuje da li se pored njega nalazi disk ili niz diskova protivnikove boje i ukoliko se nalazi
    # funkcija dodaje koordinate polja na kraju tog niza protivnikovih diskova u listu mogućih opcija
    def mogucnosti(self, boja):
        lista = []
        for i in range(8):
            for j in range(8):
                # ukoliko naiđe na polje na kome se nalazi disk igrača koji je na potezu onda proverava stanje oko tog polja
                if self._board[i][j] == boja:
                    # xsmer i ysmer omogućavaju kretanje u svim smerovima(horizontalno,vertikalno i dijagonalno)
                    for xsmer, ysmer in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                                         [-1, 1]]:
                        x = i + xsmer
                        y = j + ysmer
                        if self.natabli(x, y) and self._board[x][y] == self.protivnik(boja):
                            while self.natabli(x, y):
                                if self._board[x][y] == self.protivnik(boja) or self._board[x][y] == "-":
                                    # ako naiđe na prazno polje posle niza diskova protivnikove boje, dodaje
                                    # njegove koordinate u listu mogućih poteza
                                    if self._board[x][y] == "-":
                                        lista.append([x, y])
                                        break
                                    # ako se na polju nalazi protivnikov disk nastavlja dalje
                                    else:
                                        x += xsmer
                                        y += ysmer
                                else:
                                    break
                else:
                    continue
        return lista

    # funkcija okreni prolazi kroz tablu i svaki put kada naiđe na polje na kome je disk igrača koji je trenutno na potezu
    # proverava da li u nekom smeru postoji protivnikov disk ili niz diskova na čijem krajus e nalazi disk igrača koji je na potezu.
    # Ukoliko je to slučaj funkcija okreni okrće redom disk ili niz diskova protivnikove boje u boju igrača koji je na potezu.
    def okreni(self, boja, i, j):
        self._board[i][j] = boja
        # xsmer i ysmer omogucavaju kretanje u svim smerovima(horizontalno,vertikalno i dijagonalno)
        for xsmer, ysmer in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                             [-1, 1]]:
            x = i + xsmer
            y = j + ysmer
            ima = False
            # proverava da li postoji disk ili niz protivnikovih diskova na čijem kraju je disk igrača koji je na potezu
            while self.natabli(x, y) and (self._board[x][y] == self.protivnik(boja) or self._board[x][y] == boja):
                if self._board[x][y] == boja:
                    ima = True
                    break
                x += xsmer
                y += ysmer
            # ako postoji menja sve diskove tog niza u boju igrača koji je trneutno na potezu
            if ima:
                x = i + xsmer
                y = j + ysmer
                while self.natabli(x, y) and self._board[x][y] == self.protivnik(boja):
                    self._board[x][y] = boja
                    x += xsmer
                    y += ysmer

    # funkcija igraj proverava da li je moguće odigrati izabrani potez
    def igraj(self, x, y, boja):
        # ako je izabran mogući potez
        if [x, y] in self.mogucnosti(boja):
            # okreće diskove
            self.okreni(boja, x, y)
        # ako je izabran nemogući potez
        else:
            print("Ovaj potez nije moguce odigrati!")

    # funkcija Game Over proglašava kraj igre ukoliko je tabla popunjena ili nema više mogućih poteza
    def game_over(self, na_redu):
        if (not self.mogucnosti(na_redu)) or (self.ukupni_poeni() == 64):
            return True
        else:
            return False

    def ukupni_poeni(self):
        return self.poeni()[0] + self.poeni()[1]

    # funkcija poeni prolazi kroz tablu i broji koliko ima crnih a koliko belih diskova
    def poeni(self):
        b = 0
        w = 0
        for i in range(8):
            for j in range(8):
                # ako naiđe na crni disk doda 1 poen crnom igraču
                if self._board[i][j] == "B":
                    b += 1
                # ako naiđe na beli disk doda 1 poen belom igraču
                elif self._board[i][j] == "W":
                    w += 1
        return b, w

    def to_string(self):
        s = ''
        for r in self._board:
            for c in r:
                s += str(c) + ','
        return s[:-1]

    # funkcija pobednik utvrđuje koji igrač je pobedio ili
    # ukoliko je nerešeno
    def pobednik(self):
        if len(self.mogucnosti("B")) == 0:
            return "POBEDIO JE BELI :) np"
        elif len(self.mogucnosti("W")) == 0:
            return "POBEDIO JE CRNI :) np"
        elif self.poeni()[0] > self.poeni()[1]:
            return "POBEDIO JE CRNI :)"
        elif self.poeni()[0] < self.poeni()[1]:
            return "POBEDIO JE BELI :)"
        else:
            return "NEREŠENO JE!"

#importovanje potrebnih fajlova i pygame-a
from igra import Game
import pygame

pygame.init()
#podešavanje boja i fiksnih veličina
sirina = 640
visina = 760
dimenzija = 8
polje = sirina // dimenzija
zelena = (0, 100, 0)
crna = (0, 0, 0)
bela = (255, 255, 255)
fps = 60
#podešavanje header-a
pygame.display.set_caption('Reversi')
slika = pygame.image.load('1.png')
pygame.display.set_icon(slika)

def main():
    #formiranje prozora
    prozor = pygame.display.set_mode((sirina, visina))
    sat = pygame.time.Clock()
    g = Game()
    run = True
    print_text(prozor, "Crni ", (490, 650), 30)
    #dok je otvoren prozor
    while run:
        #tabla se prikazuje
        nacrtajTrenutnoStanje(prozor, g)
        sat.tick(fps)
        pygame.display.flip()
        
        for e in pygame.event.get():
            #klikom na x se izlazi iz prozora
            if e.type == pygame.QUIT:
                run = False
            #ako se klikne mišom na prozoru
            if e.type == pygame.MOUSEBUTTONDOWN and g.na_redu == 'B':
                mx = e.pos[0]
                my = e.pos[1]
                #određuje na koje polje je kliknuto u zavisnosti od koordinata klika
                red = int(my // polje)
                kolona = int(mx // polje)
                #ispitujemo da li je izabrano validno polje (mogući potez)
                if [red, kolona] in g.trenutno_stanje.mogucnosti(g.na_redu):
                    #ako je izabran mogući potez onda se okreću odgovarajući diskovi
                    g.promeni(red, kolona, prozor)
                    #crta crni pravougaonik na dnu prozora preko starog teksta
                    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(20, 700, 550, 30))
                    #ako je kraj igre ispisuje pobednika
                    if g.trenutno_stanje.game_over(g.na_redu):
                        pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(0, 640, 640, 120))
                        print_text(prozor,  str(g.trenutno_stanje.pobednik()), (50, 700), 35)
                        break
                #ako je izabran nemoguć potez
                else:
                    #crta crni pravougaonik na dnu prozora preko starog teksta
                    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(20, 700, 550, 30))
                    #ispisuje novi tekst "Ovaj potez nije moguce odigrati, pokusajte ponovo! "
                    print_text(prozor, "Ovaj potez nije moguce odigrati, pokusajte ponovo! ", (20, 700), 25)
                #pokrtiva crnim kvadratima prethodni rezlutat
                cover(prozor, g)
            elif g.na_redu == 'W':
                # ako je izabran mogući potez onda se okreću odgovarajući diskovi
                g.promeni(0, 0, prozor)
                # crta crni pravougaonik na dnu prozora preko starog teksta
                pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(20, 700, 550, 30))
                # ako je kraj igre ispisuje pobednika
                if g.trenutno_stanje.game_over(g.na_redu):
                    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(0, 640, 640, 120))
                    print_text(prozor, str(g.trenutno_stanje.pobednik()), (50, 700), 35)
                    break
                cover(prozor, g)
        pygame.display.update()
    pygame.quit()
    
#funkcija nacrtajTrenutnoStanje poziva sve funkcije koje su potrebne za prikaz table i stanja na njoj
def nacrtajTrenutnoStanje(prozor, g):
    nacrtajTablu(prozor)
    nacrtajKrugove(prozor, g.trenutno_stanje)
    nacrtajMogucnosti(prozor, g)
    print_text(prozor, "Crni: ", (20, 650), 30)
    print_text(prozor, str(g.trenutno_stanje.poeni()[0]), (80, 650), 30)
    print_text(prozor, "Beli: ", (200, 650), 30)
    print_text(prozor, str(g.trenutno_stanje.poeni()[1]), (260, 650), 30)
    print_text(prozor, "Igra: ", (435, 650), 30)

def cover(prozor, g):
    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(255, 650, 40, 30))
    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(75, 650, 40, 30))
    pygame.draw.rect(prozor, (0, 0, 0), pygame.Rect(490, 650, 120, 30))
    # ispisuje novi rezultat
    print_text(prozor, "Crni: ", (20, 650), 30)
    print_text(prozor, str(g.trenutno_stanje.poeni()[0]), (80, 650), 30)
    print_text(prozor, "Beli: ", (200, 650), 30)
    print_text(prozor, str(g.trenutno_stanje.poeni()[1]), (260, 650), 30)
    print_text(prozor, "Igra: ", (435, 650), 30)
    # ispisuje igrača koji je na redu
    if g.na_redu == 'B':
        print_text(prozor, "Crni ", (490, 650), 30)
    else:
        print_text(prozor, "Beli ", (490, 650), 30)
#funkcija nacrtajTablu redom crta zelene kvadrate (tablu) na prozoru igrice
def nacrtajTablu(prozor):
    for i in range(dimenzija):
        for j in range(dimenzija):
            pygame.draw.rect(prozor,zelena,pygame.Rect(j*polje, i*polje, polje-2, polje-2))

#funkcija nacrtajKrugove crta crne i bele krugove na određena (zauzeta) polja table
def nacrtajKrugove(prozor,stanjeIgre):
    for i in range(dimenzija):
        for j in range(dimenzija):
            #ako je polje zauzeo beli igrač crta beli krug
            if stanjeIgre.board[i][j] == 'W':
                #crtanje crnog kruga (okvira) sa malo većim prečnikom
                pygame.draw.circle(prozor, crna, (polje * j + polje // 2, polje * i + polje // 2), polje // 2 - 8)
                #crtanje belog kruga preko crnog, sa malo manjim prečnikom
                pygame.draw.circle(prozor, bela, (polje*j + polje//2,polje*i + polje//2), polje//2 - 10)
            #ako je polje zauzeo crni igrač crta crni krug
            if stanjeIgre.board[i][j] == 'B':
                #crtanje crnog kruga
                pygame.draw.circle(prozor, crna, (polje * j + polje // 2, polje * i + polje // 2), polje // 2 - 8)

#funkcija nacrtajMogucnosti crta kružnice na poljima na kojima je moguće odigrati potez
def nacrtajMogucnosti(prozor, g):
    #za svako polje na kome je moguće staviti disk
    for i in g.trenutno_stanje.mogucnosti(g.na_redu):
        x, y = i
        #crtanje crnog kruga sa malo većim prečnikom
        pygame.draw.circle(prozor, crna, (polje * y + polje // 2, polje * x + polje // 2), polje // 2 - 8)
        #crtanje zelenog kruga preko crnog, sa malo manjim prečnikom (da bi dobili kružnicu)
        pygame.draw.circle(prozor, zelena, (polje * y + polje // 2, polje * x + polje // 2), polje // 2 - 10)

#funkcija print_text pravi površinu na kojoj ispisuje text a zatim
#tu površinu prikazuje na prozoru igrice
def print_text(prozor, text, pos, velicina):
    myfont = pygame.font.SysFont('calibri', velicina)
    surface = myfont.render(text, False, (250, 250, 250))
    prozor.blit(surface, pos)
    pygame.display.flip()



if __name__ == '__main__':
    main()




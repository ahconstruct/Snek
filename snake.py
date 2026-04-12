import pygame
import random
import sys

# --- Innstillinger ---
CELLE = 20          # Størrelse på hver rute i piksler
KOLONNER = 30       # Antall kolonner
RADER = 25          # Antall rader
BREDDE = CELLE * KOLONNER
HØYDE = CELLE * RADER
FPS = 10            # Hastighet (ruter per sekund)

# Farger
SORT      = (  0,   0,   0)
HVIT      = (255, 255, 255)
GRØNN     = ( 50, 205,  50)
MØRK_GRØNN= ( 34, 139,  34)
RØD       = (220,  20,  60)
GRÅ       = ( 40,  40,  40)
ORANSJE   = (255, 165,   0)

# Retninger
OPP   = ( 0, -1)
NED   = ( 0,  1)
VENSTRE = (-1,  0)
HØYRE   = ( 1,  0)


def tegn_rute(overflate, farge, x, y, ramme=False):
    rect = pygame.Rect(x * CELLE, y * CELLE, CELLE, CELLE)
    pygame.draw.rect(overflate, farge, rect)
    if ramme:
        pygame.draw.rect(overflate, SORT, rect, 1)


def tilfeldig_mat(slange):
    while True:
        pos = (random.randint(0, KOLONNER - 1), random.randint(0, RADER - 1))
        if pos not in slange:
            return pos


def vis_tekst(overflate, tekst, størrelse, x, y, farge=HVIT, sentrert=False):
    font = pygame.font.SysFont("segoeui", størrelse, bold=True)
    flate = font.render(tekst, True, farge)
    if sentrert:
        rect = flate.get_rect(center=(x, y))
    else:
        rect = flate.get_rect(topleft=(x, y))
    overflate.blit(flate, rect)


def spill_løkke():
    pygame.init()
    skjerm = pygame.display.set_mode((BREDDE, HØYDE))
    pygame.display.set_caption("Snake")
    klokke = pygame.time.Clock()

    # Spilltilstand
    slange = [(KOLONNER // 2, RADER // 2)]
    retning = HØYRE
    neste_retning = HØYRE
    mat = tilfeldig_mat(slange)
    poeng = 0
    spiller = True  # False = game over

    while True:
        # --- Hendelser ---
        for hendelse in pygame.event.get():
            if hendelse.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if hendelse.type == pygame.KEYDOWN:
                if not spiller:
                    # Trykk på en tast for å starte på nytt
                    return spill_løkke()
                if hendelse.key in (pygame.K_UP, pygame.K_w) and retning != NED:
                    neste_retning = OPP
                elif hendelse.key in (pygame.K_DOWN, pygame.K_s) and retning != OPP:
                    neste_retning = NED
                elif hendelse.key in (pygame.K_LEFT, pygame.K_a) and retning != HØYRE:
                    neste_retning = VENSTRE
                elif hendelse.key in (pygame.K_RIGHT, pygame.K_d) and retning != VENSTRE:
                    neste_retning = HØYRE

        if spiller:
            retning = neste_retning

            # Flytt hodet
            hode_x, hode_y = slange[0]
            ny_x = hode_x + retning[0]
            ny_y = hode_y + retning[1]
            ny_hode = (ny_x, ny_y)

            # Sjekk kollisjon med vegg
            if not (0 <= ny_x < KOLONNER and 0 <= ny_y < RADER):
                spiller = False
            # Sjekk kollisjon med seg selv
            elif ny_hode in slange:
                spiller = False
            else:
                slange.insert(0, ny_hode)
                if ny_hode == mat:
                    poeng += 1
                    mat = tilfeldig_mat(slange)
                else:
                    slange.pop()

        # --- Tegning ---
        skjerm.fill(GRÅ)

        # Tegn rutenett (subtilt)
        for kol in range(KOLONNER):
            for rad in range(RADER):
                rect = pygame.Rect(kol * CELLE, rad * CELLE, CELLE, CELLE)
                pygame.draw.rect(skjerm, (50, 50, 50), rect, 1)

        # Tegn mat
        tegn_rute(skjerm, RØD, mat[0], mat[1])

        # Tegn slange
        for i, (x, y) in enumerate(slange):
            farge = GRØNN if i > 0 else MØRK_GRØNN
            tegn_rute(skjerm, farge, x, y, ramme=True)

        # Tegn poeng
        vis_tekst(skjerm, f"Poeng: {poeng}", 22, 8, 6, ORANSJE)

        # Game over-melding
        if not spiller:
            overlay = pygame.Surface((BREDDE, HØYDE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            skjerm.blit(overlay, (0, 0))
            vis_tekst(skjerm, "GAME OVER", 54, BREDDE // 2, HØYDE // 2 - 40, RØD, sentrert=True)
            vis_tekst(skjerm, f"Poeng: {poeng}", 34, BREDDE // 2, HØYDE // 2 + 20, HVIT, sentrert=True)
            vis_tekst(skjerm, "Trykk en tast for å spille igjen", 20, BREDDE // 2, HØYDE // 2 + 70, (180, 180, 180), sentrert=True)

        pygame.display.flip()
        klokke.tick(FPS)


if __name__ == "__main__":
    spill_løkke()

from otree.api import *
import smtplib
import smtpd

import random
import psycopg2
import postgres
import psycopg2_pool
from otree.models import player


# Diese Python Seite ist da um alle Variabeln, welche später für die Datenverarbeitung wichtig sind zu definieren und auf der Seite abfragen zu lassen


class C(BaseConstants):
    NAME_IN_URL = 'MockUp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Ich habe in der C Klasse die Daten definiert, welche am Anfang fest stehen sollen und erstmal Konstant sind.
    # Dabei habe ich mehrere Informationen per Zufallsprinzip entscheiden lassen.

    # Page 2
    # ------------
    # Diese Variabel bestimmt, ob die Staatsbürgerschaft zutrifft oder nicht.
    # Wenn die Random Zahl 0 ist dann gehört die teilnehmende Person zu Novaland und wenn diese 1 ist, dann hat sie eine dauerhaft Aufenthaltserlaubnis
    Staatsbuergerschaft = random.randint(0, 1)
    # Das gleiche Prinzip wird hier auch gemacht. Mit einer if Funktion, welche weiter unten für die Page 2 definier worden ist wird die Zahl einer bestimmten Eigenschaft zugeordnet.
    # Die if Funktionen finden Sie aber auf der Page 1, da die Variabeln am Anfang an schon feststehen müssen, damit die Seite 2 diese greifen kann und damit arbeiten kann.
    Mitglieder_Arbeitslos = random.randint(0, 3)
    Ethnische_Gruppe = random.randint(0, 3)
    Effizienz = random.randint(0, 2)

    # Page 3
    # -----------
    # Einkommensstart
    # Eine Randrange macht das gleiche Prinzip eine randint nur, dass der Anfang, das Ende und die Reihe bestimmt wird, welche abgefragt werden sollen.
    # Also nach dem Prinzip random.randrange(start, stop, step) also geht diese Reihe von 1000 bis 3000 und fragt nur alle in 1000er Schritte ab.
    Random_Einkommen = random.randrange(1000, 3000, 1000)
    # Einkommenssteuer
    Random_Steuer = random.randrange(20, 40, 10)

    # Live Trustgame Page 9
    # Ich hab hier einen Gegenspieler mit dem Zufallsprinzip generiert, was wir noch mit einem echten Menschen austauschen könnten.
    gegenspieler = random.randint(1, 2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # in der Player Klasse habe ich alle Variabeln definiert, welche von den Eingaben von den Teilnehmenden verändert werden können.
    # Dafür habe ich euch mit den Unterpunkten "Pages" ausgelistet, welche Variabeln für welche Seite wichtig sind.
    # Meistens sind die Namen eindeutig genug.


    page = models.FloatField()
    # Page 2 Staatsbuergerschaft
    # -----------------
    # Hier werden die Variabeln definiert, welche kontrollieren, welche Gruppe die Teilnehmenden angehören.
    # Dabei habe ich alle
    Staatsbuergerschaft = models.StringField()          # Teilt die Staatsbürgerschaft zu. Diese ist ein Stringfield, da diese unten bei page 1 abhängig ist von Staatsbürgerschaftszahl, welche in der C Klasse definiert worden ist.
                                                        # Das Stringfield ist hauptsächlich für die Anzeige und für die Datenverarbeitung
    Mitglieder_Arbeitslos = models.StringField()        #  Sagt zu welcher Wahrscheinlichkeit die Arbeiter arbeitslos sind
    Ethnische_Gruppe = models.StringField()             # Teilt die Ethnische Gruppe zu.
    Effizienz = models.StringField()                    # Teilt die Effizient der Mitarbeiter zu.

    # page 3
    # ----------------
    Geld_besitz = models.IntegerField()                 # Sagt dem Spieler und uns, wie viel Geld die Teilnehmenden zur Verfügung stehen haben.
    Einkommenssteuer = models.FloatField()              # Beschreibt den Prozentsatz der Einkommenssteuer.
    Geld_uebrig = models.FloatField()                   # Gibt den Wert an welcher übrig bleibt, wenn die Einkommenssteuer von dem Anfangskapital abgezogen worden ist.

    # page 4
    # ----------------
    Geld_Nach_Auswahl = models.FloatField()             # Hier wird der Wert des Geldes gespeichert, welcher durch die Entscheidungen der teilnehmenden auf der Seite bestimmt wird.

    Wohnung = models.FloatField()                       # Speicherung der Daten für welche Wohnung sich die Person entschieden hat. Aber leider nur in Zahlen, dass bedeutet wenn da 200 steht, dann hat sie sich für das Appartment entschieden.
    Verpflegung = models.FloatField()                   # Speicherung der Daten aus der Entscheidung der Verpflegung.
    Freizeit = models.FloatField()                      # Speicherung der Daten aus der Entscheidung der Freizeitaktivitäten, also in welche Art Urlaub sie fahren/fliegen.

    # page 5
    # ----------------
    # Speicherung der Entscheidungsmöglichkeiten der Teilnehmenden auf die Frage 1, welche im Mockup definiert worden ist.
    F1 = models.StringField(
        choices=[["1", "Stimme stark zu"], ["2", ""], ["3", ""], ["4", ""], ["5", "Lehne stark ab"]],
        label="",
        widget=widgets.RadioSelect,
    )

    # page 6
    # ----------------
    # Speicherung der Entscheidungsmöglichkeiten der Teilnehmenden auf die Frage 2, welche im Mockup definiert worden ist.
    F2 = models.StringField(
        choices=[["1", "Auf jeden Fall verantwortlich sein"], ["2", ""], ["3", ""], ["4", ""],
                 ["5", "Auf keinen Fall verantwortlich sein"]],
        label="",
        widget=widgets.RadioSelect,
    )

    # page 7
    # ---------------
    # Speicherung der Entscheidungsmöglichkeiten der Teilnehmenden auf die Frage 3, welche im Mockup definiert worden ist.
    F3 = models.StringField(
        choices=[["1", "Der Staat sollte mehr Verantwortung dafür übernehmen, dass jeder Bürger abgesichert ist"],
                 ["2", ""], ["3", ""], ["4", ""],
                 ["5", "Der einzelne Bürger sollte mehr Verantwortung für sich selbst übernehmen"]],
        label="",
        widget=widgets.RadioSelect,
    )

    # page 9 Vertrauensgame
    # ----------------
    # hier wird das Vertrauensspiel mit Hilfe von Booleans definiert. Wenn die Person vertraut hat, ist diese Variable true
    Vertrauensspiel = models.BooleanField()
    # Dieser Variabel leitet sich oben aus der Klasse C ab.
    Gegner = models.IntegerField()

    # page 10 Userdaten
    # --------------
    # Diese Daten wurden bis jetzt angefertigt aber noch nicht integriert, da die SQL Datei also PostgresSQL noch integriert werden muss
    UserName = models.StringField()
    EMail = models.LongStringField()
    Alter = models.StringField()
    Gender = models.StringField(
        choices=[["1", "Männlich"], ["2", "Weiblich"], ["3", "Divers"], ["4", "Keine Angabe"]],
        label="Geschlecht",
        widget=widgets.RadioSelect,
    )
    # --------------
    # --------------
    # in dem Bereich ordne ich die Variabeln, den einzelnen Seiten zu.

class page_1_Startseite(Page):
    # mit vars_for_template erstelle ich Variabeln, welche von der HTML Seite erkannt werden und integriert werden können
    def vars_for_template(player: Player):
        player.page = 1
        # Ich benutze hier eine If Funktion, da ich die Konstanten die als Grundlage für diese Variabeln dienen,
        # oben randomisiert habe. Es ist auch möglich mit anderen Datatypes randomisierung zu machen, aber mit den
        # Zahlen Werten fällt es am Ende leichter, diese in Postgres abzurufen. An sich teile ich hier nur die models
        # zu, welche ich oben beim player definiert habe.
        if C.Staatsbuergerschaft == 1:
            player.Staatsbuergerschaft = "Ja"
        else:
            player.Staatsbuergerschaft = "Nein"

        if C.Mitglieder_Arbeitslos == 1:
            player.Mitglieder_Arbeitslos = "höher"
        elif C.Mitglieder_Arbeitslos == 2:
            player.Mitglieder_Arbeitslos = "gleich"
        else:
            player.Mitglieder_Arbeitslos = "niedriger"

        if C.Ethnische_Gruppe == 1:
            player.Ethnische_Gruppe = "Alfianer"
        elif C.Ethnische_Gruppe == 2:
            player.Ethnische_Gruppe = "Bolirianer"
        else:
            player.Ethnische_Gruppe = "Kolfianer"

        if C.Effizienz == 1:
            player.Effizienz = "sehr effizient"
        else:
            player.Effizienz = "sehr ineffizient"

        player.Geld_besitz = C.Random_Einkommen
        player.Einkommenssteuer = C.Random_Steuer
        player.Geld_uebrig = int(player.Geld_besitz - ((player.Geld_besitz / 100) * player.Einkommenssteuer))


class page_2_Staatsbuergerschaft(Page):
    # hier wird die Frage abverlangt, ob die Person ein Staatsbürger von Novaland ist oder nicht
    form_model = 'player'

    def vars_for_template(player: Player):
        player.page = 2
        Staatsbuergerschaft = C.Staatsbuergerschaft
        return {
            "Staatsbuergerschaft": Staatsbuergerschaft
        }


class page_3_Einkommen(Page):
    def vars_for_template(player: Player):
        player.page = 3


class page_4_Beduerfnisse_abdecken(Page):
    form_model = 'player'
    form_fields = ['Wohnung', 'Verpflegung', 'Freizeit']

    # mit der if FUnktion, sage ich dem Programm einfach nur, wie viel Geld abgezogen werden, durch die Auswahl der Teilnehmenden
    def vars_for_template(player: Player):
        player.page = 4
        Wohnung = 0
        Verpflegung = 0
        Freizeit = 0
        Geld = player.Geld_uebrig
        Gesamt = 0
        return {
            "Wohnung": Wohnung,
            "Verpflegung": Verpflegung,
            "Freizeit": Freizeit,
            "Geld": Geld,
            "Gesamt": Gesamt,
        }


class page_5_Fragentext_1(Page):
    form_model = 'player'
    form_fields = ['F1']

    def vars_for_template(player: Player):
        player.page = 5
        player.Geld_Nach_Auswahl = player.Geld_uebrig - player.Wohnung - player.Verpflegung - player.Freizeit


class page_6_Fragentext_2(Page):
    form_model = 'player'
    form_fields = ['F2']

    def vars_for_template(player: Player):
        player.page = 6


class page_7_Fragentext(Page):
    player.page = 7
    form_model = 'player'
    form_fields = ['F3']

    def vars_for_template(player: Player):
        player.page = 7


class page_8_Results(Page):
    def vars_for_template(player: Player):
        player.page = 8


# Das Trustgame ist noch nicht integriert
class page_9_Trustgame(Page):
    form_model = 'player'
    form_fields = ['Vertrauensspiel']
    live_method = "live_vertrauen"

    @staticmethod
    def vars_for_template(player: Player):
        player.Gegner = C.gegenspieler
        Geld = player.Geld_Nach_Auswahl
        Gegenspieler = C.gegenspieler
        return {
            "Geld": Geld,
            "Gegenspieler": Gegenspieler,
        }
        player.page = 9


class page_10_Userinfos_Speichern(Page):
    form_model = 'player'
    form_fields = ['UserName', 'EMail', 'Alter', 'Gender']


class Email(Page):
    pass


# class page_10_UserInfos_Speichern(Page):
# pass

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


# Hier stellt man die Reihenfolge der Pages ein
page_sequence = [page_1_Startseite, page_2_Staatsbuergerschaft, page_3_Einkommen,
                 page_4_Beduerfnisse_abdecken,
                 page_5_Fragentext_1, page_6_Fragentext_2, page_7_Fragentext, page_9_Trustgame, page_8_Results]

# Zusätzlich
# Die Button.css File soll später ein Stylesheet werden für die ganze Website. Da muss aber noch einiges probiert werden

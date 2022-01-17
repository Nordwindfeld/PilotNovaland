from otree.api import *
import random
import psycopg2
import postgres
import psycopg2_pool
from otree.models import player


class C(BaseConstants):
    NAME_IN_URL = 'MockUp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    #Ich habe in der C Klasse die Daten definiert, welche am Anfang fest stehen sollen und erstmal Konstant sind
    # Page 2
    Staatsbuergerschaft = random.randint(0, 2)
    Mitglieder_Arbeitslos = random.randint(0, 3)
    Ethnische_Gruppe = random.randint(0, 3)
    Effizienz = random.randint(0, 2)
    # Page 3
    # Einkommensstart
    Random_Einkommen = random.randrange(1000, 3000, 1000)
    # Einkommenssteuer
    Random_Steuer = random.randrange(20, 40, 10)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # in der Player Klasse habe ich alle Variabeln definiert, welche von den Eingaben von den Teilnehmenden verändert werden können.
    # Dafür habe ich euch mit den Unterpunkten "Pages" ausgelistet, welche Variabeln für welche Seite wichtig sind

    # Page 2 Staatsbuergerschaft
    #-----------------
    # Hier werden die Variabeln definiert, welche kontrollieren, welche Gruppe die Teilnehmenden angehören.
    # Dabei habe ich alle
    Staatsbuergerschaft = models.StringField()
    Mitglieder_Arbeitslos = models.StringField()
    Ethnische_Gruppe = models.StringField()
    Effizienz = models.StringField()
    Frage_Staatsbuergerschaft = models.StringField(
        choices=[['Ja', 'Ja'], ['Nein', 'Nein']],
        label='Bist du Staatsbürger von Novaland?',
        widget=widgets.RadioSelect,
    )

    # page 2_5
    #----------------
    Staatsbuergerschaft_Kontrolle = models.BooleanField()

    # page 3
    #----------------
    Geld_besitz = models.IntegerField()
    Einkommenssteuer = models.FloatField()
    Geld_uebrig = models.FloatField()

    # page 4
    #----------------
    Geld_Nach_Auswahl = models.FloatField()

    Wohnung = models.StringField(
        choices=[["1", "Ein großes Haus. (700 Novas)"], ["2", "Eine geräumige Wohnung. (450 Novas)"],
                 ["3", "Ein kleines Ein-Zimmer-Apartment. (200 Novas)"]],
        label="Ihnen stehen verschiedene Unterkünfte zur Auswahl:",
        widget=widgets.RadioSelect,
    )
    Verpflegung = models.StringField(
        choices=[["1", "Sie gehen regelmäßig Essen (700 Novas)"],
                 ["2", "Sie bestellen sich häufig was zu essen nach Hause.(450 Novas)"],
                 ["3", "Sie kaufen günstig ein und kochen zuhause. (200 Novas)"]],
        label="Ihnen stehen verschiedene Möglichkeiten der Verpflegung zur Auswahl:",
        widget=widgets.RadioSelect,
    )

    Freizeit = models.StringField(
        choices=[["1", "Sie fliegen im Urlaub in ein fernes Land. (700 Novas)"],
                 ["2", "Sie fahren in ein Hotel in einer Urlaubsregion in Novaland. (450 Novas"],
                 ["3", "Sie machen einen Campingurlaub in einer Urlaubsregion in Novaland. (200 Novas)"]],
        label="Ihnen stehen verschiedene Möglichkeiten der Freizeitgestaltung zur Auswahl:",
        widget=widgets.RadioSelect,
    )

    # page 5
    F1 = models.StringField(
        choices=[["1", "Stimme stark zu"], ["2", ""], ["3", ""], ["4", ""], ["5", "Lehne stark ab"]],
        label="",
        widget=widgets.RadioSelect,
    )

    F2 = models.StringField(
        choices=[["1", "Auf jeden Fall verantwortlich sein"], ["2", ""], ["3", ""], ["4", ""],
                 ["5", "Auf keinen Fall verantwortlich sein"]],
        label="",
        widget=widgets.RadioSelect,
    )

    F3 = models.StringField(
        choices=[["1", "Der Staat sollte mehr Verantwortung dafür übernehmen, dass jeder Bürger abgesichert ist"],
                 ["2", ""], ["3", ""], ["4", ""],
                 ["5", "Der einzelne Bürger sollte mehr Verantwortung für sich selbst übernehmen"]],
        label="",
        widget=widgets.RadioSelect,
    )

    # page 9 Vertrauensgame
    #----------------
    # Hier muss ich erst noch die Live pages integrieren, bevor ich das fertig machen kann
    vertrauen = models.BooleanField(
        label="Bitte wähle, ob du der anderen Person vertraust oder nicht:",
        choices=[
            [True, "Vertrauen"],
            [False, "Nicht vertrauen"]
        ]
    )

# in dem Bereich ordne ich die Variabeln, den einzelnen Seiten zu.
class page_1_Startseite(Page):
    # mit vars_for_template erstelle ich Variabeln, welche von der HTML Seite erkannt werden und integriert werden können
    def vars_for_template(player: Player):
    # Ich benutze hier eine If Funktion, da ich die Konstanten die als Grundlage für diese Variabeln dienen, oben randomisiert habe.
    # Es ist auch möglich mit anderen Datatypes randomisierung zu machen, aber mit den Zahlen Werten fällt es am Ende leichter, diese in Postgres abzurufen.
    # An sich teile ich hier nur die models zu, welche ich oben beim player definiert habe.
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
    form_fields = ['Frage_Staatsbuergerschaft']


class page_2_5_Test_Staatsbuergerschaft(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.Staatsbuergerschaft == player.Frage_Staatsbuergerschaft:
            player.Staatsbuergerschaft_Kontrolle = True
        else:
            player.Staatsbuergerschaft_Kontrolle = False
    # mit der def is_displayed Funktion kann man Seiten überspringen lassen, was ich in dem Fall gemacht habe, da diese Seite nur gezeigt wird, wenn die Teilnehmenden die Frage falsch beantwortet haben.
    def is_displayed(player: Player):
        return player.Staatsbuergerschaft != player.Frage_Staatsbuergerschaft


class page_3_Einkommen(Page):
    pass


class page_4_Beduerfnisse_abdecken(Page):
    form_model = 'player'
    form_fields = ['Wohnung', 'Verpflegung', 'Freizeit']




class page_5_Fragentext_1(Page):
    form_model = 'player'
    form_fields = ['F1']
    
    # mit der if FUnktion, sage ich dem Programm einfach nur, wie viel Geld abgezogen werden, durch die Auswahl der Teilnehmenden 

    def vars_for_template(player: Player):
        player.Geld_Nach_Auswahl = player.Geld_uebrig
        if player.Wohnung == "1":
            player.Geld_Nach_Auswahl -= 700
        elif player.Wohnung == "2":
            player.Geld_Nach_Auswahl -= 450
        elif player.Wohnung == "3":
            player.Geld_Nach_Auswahl -= 200

        if player.Verpflegung == "1":
            player.Geld_Nach_Auswahl -= 700
        elif player.Verpflegung == "2":
            player.Geld_Nach_Auswahl -= 450
        elif player.Verpflegung == "3":
            player.Geld_Nach_Auswahl -= 200

        if player.Freizeit == "1":
            player.Geld_Nach_Auswahl -= 700
        elif player.Freizeit == "2":
            player.Geld_Nach_Auswahl -= 450
        elif player.Freizeit == "3":
            player.Geld_Nach_Auswahl -= 200


class page_6_Fragentext_2(Page):
    form_model = 'player'
    form_fields = ['F2']


class page_7_Fragentext(Page):
    form_model = 'player'
    form_fields = ['F3']


class page_8_Results(Page):
    pass

# Das Trustgame ist noch nicht integriert
class page_9_Trustgame(Page):
    form_model = 'player'
    form_fields = ['vertrauen']

    def vars_for_template(player: Player):
        C.Beide_Vertrauen = 400
        C.Nur_Du_Vertraust = -200
        C.Du_misstraust = 200
        C.beide_misstrauen = 0


# class page_10_UserInfos_Speichern(Page):
# pass

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


#Hier stellt man die Reihenfolge der Pages ein
page_sequence = [page_1_Startseite, page_2_Staatsbuergerschaft, page_2_5_Test_Staatsbuergerschaft, page_3_Einkommen,
                 page_4_Beduerfnisse_abdecken,
                 page_5_Fragentext_1, page_6_Fragentext_2, page_7_Fragentext, page_8_Results]

#Zusätzlich
# Die Button.css File soll später ein Stylesheet werden für die ganze Website. Da muss aber noch einiges probiert werden

import time

from Functions import AddCardsToOpenBinder, startmtgoapp, is_MainNavigation_running, maximize_MTGO, checkifimagepresent, TradeWithGoatbotsSell

#main software

if is_MainNavigation_running() == 0:
    startmtgoapp()
CardName = "Lava Dart"
AddCardsToOpenBinder("Lava dart")



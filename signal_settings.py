from templates import Templates
from main import Event_Green


class Settings:
    # Wählen ob Schaltplan nach Vorlage (True = Vorlage, False = Eigener Schaltplan)
    use_templates = True
    template_number = 1

    # Eigener Schaltplan: Füge für jede Ampel, die auf grün wechseln soll, einen Event_Green zur Liste hinzu
    own_events = [
        Event_Green(1, 2, 10),
        Event_Green(1, 3, 50),
        Event_Green(2, 4, 80),
        Event_Green(2, 1, 80),
        Event_Green(3, 2, 60),
        Event_Green(3, 4, 120)
    ]

    # Definiere, wie lange der ganze Schaltplan (in Frames) dauern soll, bis er sich wiederholt
    own_duration = 200

    # NICHT VERÄNDERN!
    if use_templates:
        events = Templates.get_events(template_number)[0]
        duration = Templates.get_events(template_number)[1]
    else:
        events = own_events
        duration = own_duration

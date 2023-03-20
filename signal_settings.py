from templates import Templates
from main import Event_Green


class Settings:
    # Wählen ob Schaltplan nach Vorlage (True = Vorlage, False = Eigener Schaltplan)
    use_templates = False
    template_number = 1

    # Eigener Schaltplan: Füge für jede Ampel, die auf grün wechseln soll, einen Event_Green zur Liste hinzu
    own_events = [
        Event_Green(1, 1, 1),
        Event_Green(1, 2, 50),
        Event_Green(1, 3, 100),
        Event_Green(1, 4, 150),
        Event_Green(2, 1, 1),
        Event_Green(2, 2, 50),
        Event_Green(2, 3, 100),
        Event_Green(2, 4, 150),
        Event_Green(3, 1, 1),
        Event_Green(3, 2, 50),
        Event_Green(3, 3, 100),
        Event_Green(3, 4, 150),

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

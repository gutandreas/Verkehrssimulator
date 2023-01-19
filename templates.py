import random
from main import Event_Green


class Templates:
    event_collection = []
    duration_collection = []

    events1 = [
        Event_Green(1, 1, 100),
        Event_Green(2, 1, 100),
        Event_Green(3, 1, 100),

        Event_Green(1, 2, 200),
        Event_Green(2, 2, 200),
        Event_Green(3, 2, 200),

        Event_Green(1, 3, 300),
        Event_Green(2, 3, 300),
        Event_Green(3, 3, 300),

        Event_Green(1, 4, 400),
        Event_Green(2, 4, 400),
        Event_Green(3, 4, 400),
    ]

    random_numbers_1 = [1, 2, 3, 4]
    random_numbers_2 = [1, 2, 3, 4]
    random_numbers_3 = [1, 2, 3, 4]

    events2 = [
        Event_Green(1, random_numbers_1.pop(random.randrange(4)), 50),
        Event_Green(2, random_numbers_2.pop(random.randrange(4)), 50),
        Event_Green(3, random_numbers_3.pop(random.randrange(4)), 50),

        Event_Green(1, random_numbers_1.pop(random.randrange(3)), 100),
        Event_Green(2, random_numbers_2.pop(random.randrange(3)), 100),
        Event_Green(3, random_numbers_3.pop(random.randrange(3)), 100),

        Event_Green(1, random_numbers_1.pop(random.randrange(2)), 150),
        Event_Green(2, random_numbers_2.pop(random.randrange(2)), 150),
        Event_Green(3, random_numbers_3.pop(random.randrange(2)), 150),

        Event_Green(1, random_numbers_1.pop(0), 200),
        Event_Green(2, random_numbers_2.pop(0), 200),
        Event_Green(3, random_numbers_3.pop(0), 200),

    ]

    duration1 = 501
    duration2 = 201

    event_collection.append(events1)
    event_collection.append(events2)
    duration_collection.append(duration1)
    duration_collection.append(duration2)

    def get_events(number):
        return Templates.event_collection[number - 1], Templates.duration_collection[number - 1]

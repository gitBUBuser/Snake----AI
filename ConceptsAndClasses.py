import snake_rules
import GameObject
import snake_object

class movement_event():
     def __init__(self, object = None, new_move = None):
        if isinstance(object, GameObject.Game_Object) and type(new_move) == tuple:
            self.object = object
            self.new_move = new_move
        else:
            "Error! Couldn't add movement event"
    
     def execute(self):
         self.object.step(self.new_move)

     def get_object(self):
         return self.object

     def change_move(self, new_move):
         if type(new_move) == tuple:
             self.new_move == new_move

class movement_event_handler():
    def __init__(self):
        self.events = []

    def add_event(self, an_object, a_move):
        for event in self.events:
            if event.get_object() == an_object:
                event.change_move(a_move)
                return "updated event"
        self.events.append(movement_event(an_object, a_move))
        return "added event"
    
    def remove_event(self, an_object):
        object_to_remove = movement_event()
        for event in self.events:
            if event.get_object() == an_object:
                object_to_remove = event
        self.events.remove(object_to_remove)

    def clear(self):
        self.events.clear()

    def execute_events(self):
        print(len(self.events))
        for event in self.events:
            event.execute()
        self.clear()




        
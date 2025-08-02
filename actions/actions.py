from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):
    def name(self):
        return "action_hello_world"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Hello from the action server!")
        return []

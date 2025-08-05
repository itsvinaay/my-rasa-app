from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import psycopg2
from datetime import datetime
import os
import openai

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appointment_date = tracker.get_slot("appointment_date")
        appointment_time = tracker.get_slot("appointment_time")
        user_name = tracker.get_slot("user_name")
        
        # Connect to database
        try:
            conn = psycopg2.connect(os.getenv("DB_URL"))
            cur = conn.cursor()
            
            # Create appointments table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(100),
                    appointment_date VARCHAR(50),
                    appointment_time VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert appointment
            cur.execute("""
                INSERT INTO appointments (user_name, appointment_date, appointment_time)
                VALUES (%s, %s, %s)
            """, (user_name or "Unknown", appointment_date or "Not specified", appointment_time or "Not specified"))
            
            conn.commit()
            cur.close()
            conn.close()
            
            dispatcher.utter_message(text=f"Great! I've booked your appointment for {appointment_date or 'the requested date'} at {appointment_time or 'the requested time'}. You'll receive a confirmation shortly.")
            
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, there was an issue booking your appointment. Please try again later.")
            print(f"Database error: {e}")
        
        return []

class ActionCancelAppointment(Action):
    def name(self) -> Text:
        return "action_cancel_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="I've cancelled your appointment. If you need to reschedule, just let me know!")
        return []

class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simulate balance check
        balance = 2500.75  # This would normally come from a banking API
        
        dispatcher.utter_message(text=f"Your current account balance is ${balance:.2f}")
        return []

class ActionTransferMoney(Action):
    def name(self) -> Text:
        return "action_transfer_money"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        amount = tracker.get_slot("transfer_amount")
        
        if amount:
            dispatcher.utter_message(text=f"I've initiated a transfer of ${amount}. You'll receive a confirmation once it's processed.")
        else:
            dispatcher.utter_message(text="I'd be happy to help you transfer money. How much would you like to transfer?")
        
        return []

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # This would normally integrate with a weather API
        dispatcher.utter_message(text="I don't have access to real-time weather data, but I recommend checking your local weather app for the most accurate forecast!")
        return []

class ActionGetTime(Action):
    def name(self) -> Text:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        dispatcher.utter_message(text=f"The current time is {current_time} on {current_date}")
        return []

class ActionAIResponse(Action):
    def name(self) -> Text:
        return "action_ai_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text')
        
        try:
            # Use OpenAI to generate a response for complex queries
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Keep responses concise and friendly."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            
            ai_response = response.choices[0].message.content.strip()
            dispatcher.utter_message(text=ai_response)
            
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, I'm having trouble processing that request right now. Could you try rephrasing?")
            print(f"OpenAI API error: {e}")
        
        return []
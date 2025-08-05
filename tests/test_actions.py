import pytest
from unittest.mock import Mock, patch
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.actions import ActionBookAppointment, ActionCheckBalance, ActionTransferMoney

class TestActions:
    
    def test_book_appointment_action(self):
        """Test appointment booking action"""
        action = ActionBookAppointment()
        dispatcher = Mock(spec=CollectingDispatcher)
        tracker = Mock(spec=Tracker)
        
        # Mock slot values
        tracker.get_slot.side_effect = lambda slot_name: {
            "appointment_date": "2024-01-15",
            "appointment_time": "10:00 AM",
            "user_name": "John Doe"
        }.get(slot_name)
        
        domain = {}
        
        with patch('psycopg2.connect') as mock_connect:
            mock_conn = Mock()
            mock_cur = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cur
            
            result = action.run(dispatcher, tracker, domain)
            
            # Verify database operations
            mock_cur.execute.assert_called()
            mock_conn.commit.assert_called_once()
            
            # Verify response
            dispatcher.utter_message.assert_called_once()
            assert "booked your appointment" in dispatcher.utter_message.call_args[1]['text']
    
    def test_check_balance_action(self):
        """Test balance check action"""
        action = ActionCheckBalance()
        dispatcher = Mock(spec=CollectingDispatcher)
        tracker = Mock(spec=Tracker)
        domain = {}
        
        result = action.run(dispatcher, tracker, domain)
        
        # Verify response contains balance
        dispatcher.utter_message.assert_called_once()
        assert "$2500.75" in dispatcher.utter_message.call_args[1]['text']
    
    def test_transfer_money_action_with_amount(self):
        """Test money transfer with amount"""
        action = ActionTransferMoney()
        dispatcher = Mock(spec=CollectingDispatcher)
        tracker = Mock(spec=Tracker)
        tracker.get_slot.return_value = 100.0
        domain = {}
        
        result = action.run(dispatcher, tracker, domain)
        
        # Verify response contains transfer amount
        dispatcher.utter_message.assert_called_once()
        assert "$100" in dispatcher.utter_message.call_args[1]['text']
    
    def test_transfer_money_action_without_amount(self):
        """Test money transfer without amount"""
        action = ActionTransferMoney()
        dispatcher = Mock(spec=CollectingDispatcher)
        tracker = Mock(spec=Tracker)
        tracker.get_slot.return_value = None
        domain = {}
        
        result = action.run(dispatcher, tracker, domain)
        
        # Verify response asks for amount
        dispatcher.utter_message.assert_called_once()
        assert "How much would you like to transfer" in dispatcher.utter_message.call_args[1]['text']

if __name__ == "__main__":
    pytest.main([__file__])
import pytest
from datetime import datetime
from app.schemas import MessageBase, MessageCreate, MessageRead, ConversationRead
from app.models import Message

class TestSchemas:
    """Test Pydantic schemas."""
    
    def test_message_base(self):
        """Test MessageBase schema."""
        message_data = {
            "role": "user",
            "content": "Test message"
        }
        
        message = MessageBase(**message_data)
        assert message.role == "user"
        assert message.content == "Test message"
    
    def test_message_create(self):
        """Test MessageCreate schema."""
        message_data = {
            "role": "ai",
            "content": "AI response"
        }
        
        message = MessageCreate(**message_data)
        assert message.role == "ai"
        assert message.content == "AI response"
    
    def test_message_read(self):
        """Test MessageRead schema."""
        message_data = {
            "id": 1,
            "role": "user",
            "content": "Test message",
            "created_at": datetime.now()
        }
        
        message = MessageRead(**message_data)
        assert message.id == 1
        assert message.role == "user"
        assert message.content == "Test message"
        assert isinstance(message.created_at, datetime)
    
    def test_conversation_read(self):
        """Test ConversationRead schema."""
        messages = [
            MessageRead(
                id=1,
                role="user",
                content="Hello",
                created_at=datetime.now()
            ),
            MessageRead(
                id=2,
                role="ai",
                content="Hi there!",
                created_at=datetime.now()
            )
        ]
        
        conversation = ConversationRead(messages=messages)
        assert len(conversation.messages) == 2
        assert conversation.messages[0].role == "user"
        assert conversation.messages[1].role == "ai"
    
    def test_schema_validation(self):
        """Test schema validation."""
        # Test invalid role
        with pytest.raises(ValueError):
            MessageBase(role="invalid", content="test")
        
        # Test missing required fields
        with pytest.raises(ValueError):
            MessageBase(role="user")  # missing content
        
        with pytest.raises(ValueError):
            MessageBase(content="test")  # missing role 
import pytest
from datetime import datetime
from app.models import Message, Base
from app.schemas import MessageRead, ConversationRead

class TestModels:
    """Test database models."""
    
    @pytest.mark.asyncio
    async def test_message_creation(self, test_session):
        """Test creating a message."""
        message = Message(
            role="user",
            content="Test message content"
        )
        
        test_session.add(message)
        await test_session.commit()
        await test_session.refresh(message)
        
        assert message.id is not None
        assert message.role == "user"
        assert message.content == "Test message content"
        assert isinstance(message.created_at, datetime)
    
    @pytest.mark.asyncio
    async def test_message_ai_role(self, test_session):
        """Test creating an AI message."""
        message = Message(
            role="ai",
            content="AI response content"
        )
        
        test_session.add(message)
        await test_session.commit()
        await test_session.refresh(message)
        
        assert message.role == "ai"
        assert message.content == "AI response content"
    
    @pytest.mark.asyncio
    async def test_message_validation(self, test_session):
        """Test message validation."""
        # Test with empty content
        message = Message(role="user", content="")
        test_session.add(message)
        await test_session.commit()
        await test_session.refresh(message)
        
        assert message.content == ""
    
    @pytest.mark.asyncio
    async def test_message_retrieval(self, test_session):
        """Test retrieving messages from database."""
        # Create multiple messages
        messages = [
            Message(role="user", content="Message 1"),
            Message(role="ai", content="Response 1"),
            Message(role="user", content="Message 2"),
        ]
        
        for msg in messages:
            test_session.add(msg)
        await test_session.commit()
        
        # Retrieve all messages
        result = await test_session.execute(
            Message.__table__.select().order_by(Message.created_at.asc())
        )
        retrieved_messages = result.fetchall()
        
        assert len(retrieved_messages) == 3
        assert retrieved_messages[0].role == "user"
        assert retrieved_messages[1].role == "ai"
        assert retrieved_messages[2].role == "user" 
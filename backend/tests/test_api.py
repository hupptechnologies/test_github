import pytest
from httpx import AsyncClient
from app.models import Message
from app.schemas import MessageCreate

class TestAPI:
    """Test API endpoints."""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test the root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "AI Chat Backend is running"
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, client: AsyncClient):
        """Test the health check endpoint."""
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data
    
    @pytest.mark.asyncio
    async def test_history_endpoint_empty(self, client: AsyncClient):
        """Test the history endpoint with no messages."""
        response = await client.get("/api/history")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert isinstance(data["messages"], list)
        assert len(data["messages"]) == 0
    
    @pytest.mark.asyncio
    async def test_history_endpoint_with_messages(self, client: AsyncClient, test_session):
        """Test the history endpoint with messages."""
        # Create test messages
        user_message = Message(role="user", content="Hello")
        ai_message = Message(role="ai", content="Hi there!")
        
        test_session.add(user_message)
        test_session.add(ai_message)
        await test_session.commit()
        
        response = await client.get("/api/history")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert len(data["messages"]) == 2
        
        # Check message structure
        for message in data["messages"]:
            assert "id" in message
            assert "role" in message
            assert "content" in message
            assert "created_at" in message
            assert message["role"] in ["user", "ai"]
    
    @pytest.mark.asyncio
    async def test_invalid_endpoint(self, client: AsyncClient):
        """Test invalid endpoint returns 404."""
        response = await client.get("/api/nonexistent")
        assert response.status_code == 404 
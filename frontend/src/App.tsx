import React, { useEffect, useRef, useState } from 'react';
import { fetchConversation } from './api';
import type { Message, WSMessage } from './types';
import { Conversation } from './components/Conversation';
import { MessageInput } from './components/MessageInput';
import { config } from './config';
import './App.css';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streamingAI, setStreamingAI] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    fetchConversation()
      .then((data) => setMessages(data.messages))
      .catch(() => setError('Failed to load conversation history.'));
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket(config.WS_URL);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
      try {
        const data: WSMessage = JSON.parse(event.data);
        handleWSMessage(data);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
        setError('Invalid message from server');
      }
    };

    ws.onerror = () => {
      setError('WebSocket error');
    };

    return ws;
  };

  const handleWSMessage = (msg: WSMessage) => {
    if (msg.error) {
      setError(msg.error);
      setLoading(false);
      setStreamingAI('');
      wsRef.current?.close();
      wsRef.current = null;
      return;
    }

    if (msg.loading) {
      setLoading(true);
      if (msg.role === 'ai') {
        setStreamingAI(msg.content || '');
      }
    } else {
      setLoading(false);
      if (msg.role === 'ai' && msg.content !== undefined) {
        setMessages((prev) => [
          ...prev,
          { 
            id: Date.now(), 
            role: 'ai', 
            content: msg.content ?? '', 
            created_at: new Date().toISOString() 
          },
        ]);
        setStreamingAI('');
        wsRef.current?.close();
        wsRef.current = null;
      }
    }

    if (msg.role === 'user' && msg.content !== undefined) {
      setMessages((prev) => [
        ...prev,
        { 
          id: Date.now(), 
          role: 'user', 
          content: msg.content ?? '', 
          created_at: new Date().toISOString() 
        },
      ]);
    }
  };

  const handleSend = (content: string) => {
    setError(null);
    setLoading(true);
    setStreamingAI('');
    
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      wsRef.current = connectWebSocket();
      
      // Wait for connection to be established
      wsRef.current.onopen = () => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({ content }));
        }
      };
    } else {
      wsRef.current.send(JSON.stringify({ content }));
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <h1 className="app-title">{config.APP_TITLE}</h1>
        <Conversation messages={messages} streamingAI={streamingAI} />
        {error && <div className="error-message">{error}</div>}
        <MessageInput onSend={handleSend} disabled={loading} />
        {loading && <div className="loading-indicator">AI is typing...</div>}
      </div>
      </div>
  );
};

export default App; 
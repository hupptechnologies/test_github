import React, { useEffect, useRef } from 'react';
import type { Message } from '../types';

type Props = {
  messages?: Message[];
  streamingAI?: string;
};

const formatMessage = (content: string) => {
  // Simple formatting for common markdown-like patterns
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br />');
};

export const Conversation: React.FC<Props> = ({ messages = [], streamingAI }) => {
  const conversationRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages or streaming content changes
  useEffect(() => {
    if (conversationRef.current) {
      conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
    }
  }, [messages, streamingAI]);

  return (
    <div className="conversation-container" ref={conversationRef}>
      {messages.map((msg) => (
        <div key={msg.id} className={`message ${msg.role === 'user' ? 'user-message' : 'ai-message'}`}>
          <div 
            className="message-content"
            dangerouslySetInnerHTML={msg.role === 'ai' ? { __html: formatMessage(msg.content) } : undefined}
          >
            {msg.role === 'user' ? msg.content : undefined}
          </div>
        </div>
      ))}
      {streamingAI && (
        <div className="message ai-message">
          <div 
            className="message-content"
            dangerouslySetInnerHTML={{ __html: formatMessage(streamingAI) }}
          />
        </div>
      )}
    </div>
  );
}; 
import React, { useState } from 'react';

type Props = {
  onSend: (content: string) => void;
  disabled?: boolean;
};

export const MessageInput: React.FC<Props> = ({ onSend, disabled }) => {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim()) {
      onSend(value);
      setValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <input
        type="text"
        value={value}
        onChange={e => setValue(e.target.value)}
        disabled={disabled}
        placeholder="Type your message..."
        className="message-input"
      />
      <button 
        type="submit" 
        disabled={disabled || !value.trim()} 
        className="send-button"
      >
        Send
      </button>
    </form>
  );
}; 
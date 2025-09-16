import React from 'react';
import { Bot } from 'lucide-react';
import './TypingIndicator.css';

const TypingIndicator = () => {
  return (
    <div className="message-bubble bot-message typing-indicator">
      <div className="message-avatar">
        <Bot size={20} className="bot-icon" />
      </div>
      <div className="message-content typing-content">
        <div className="typing-animation">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
        <div className="typing-text">JalBuddy is thinking...</div>
      </div>
    </div>
  );
};

export default TypingIndicator;
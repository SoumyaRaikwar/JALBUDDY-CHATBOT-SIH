import React from 'react';
import { Bot, User } from 'lucide-react';
import DataCard from './DataCard';
import './MessageBubble.css';

const MessageBubble = ({ message }) => {
  const { text, sender, timestamp, dataCard } = message;
  const isBot = sender === 'bot';

  const formatTime = (date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    }).format(date);
  };

  return (
    <div className={`message-bubble ${isBot ? 'bot-message' : 'user-message'}`}>
      <div className="message-avatar">
        {isBot ? (
          <Bot size={20} className="bot-icon" />
        ) : (
          <User size={20} className="user-icon" />
        )}
      </div>
      <div className="message-content">
        <div className="message-text">
          {text}
        </div>
        {dataCard && (
          <DataCard
            title={dataCard.title}
            summary={dataCard.summary}
            details={dataCard.details}
            suggestion={dataCard.suggestion}
            color={dataCard.color}
          />
        )}
        <div className="message-timestamp">
          {formatTime(timestamp)}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
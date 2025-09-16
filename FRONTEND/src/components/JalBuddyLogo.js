import React from 'react';
import './JalBuddyLogo.css';

const JalBuddyLogo = ({ size = 32, animated = true }) => {
  return (
    <div className={`jalbuddy-logo ${animated ? 'animated' : ''}`} style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 120"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Water drop body */}
        <path
          d="M50 10C30 30 15 45 15 65C15 82.5 30.5 95 50 95C69.5 95 85 82.5 85 65C85 45 70 30 50 10Z"
          fill="url(#waterGradient)"
          stroke="rgba(255,255,255,0.3)"
          strokeWidth="2"
        />
        
        {/* Shine effect */}
        <ellipse
          cx="40"
          cy="35"
          rx="8"
          ry="12"
          fill="rgba(255,255,255,0.4)"
          transform="rotate(-15 40 35)"
        />
        
        {/* Eyes */}
        <circle cx="40" cy="50" r="4" fill="#1e3a8a" />
        <circle cx="60" cy="50" r="4" fill="#1e3a8a" />
        
        {/* Eye highlights */}
        <circle cx="41" cy="48" r="1.5" fill="white" />
        <circle cx="61" cy="48" r="1.5" fill="white" />
        
        {/* Smile */}
        <path
          d="M38 65 Q50 75 62 65"
          stroke="#1e3a8a"
          strokeWidth="3"
          strokeLinecap="round"
          fill="none"
        />
        
        {/* Cheek blush */}
        <ellipse cx="30" cy="58" rx="4" ry="2" fill="rgba(59, 130, 246, 0.2)" />
        <ellipse cx="70" cy="58" rx="4" ry="2" fill="rgba(59, 130, 246, 0.2)" />
        
        {/* Water ripples at bottom */}
        <path
          d="M25 85 Q35 80 45 85 Q55 90 65 85 Q75 80 85 85"
          stroke="rgba(59, 130, 246, 0.3)"
          strokeWidth="2"
          fill="none"
        />
        
        <defs>
          <linearGradient id="waterGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#60a5fa" />
            <stop offset="50%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#1e40af" />
          </linearGradient>
        </defs>
      </svg>
      
      {/* Floating particles around the logo */}
      <div className="particle particle-1"></div>
      <div className="particle particle-2"></div>
      <div className="particle particle-3"></div>
    </div>
  );
};

export default JalBuddyLogo;

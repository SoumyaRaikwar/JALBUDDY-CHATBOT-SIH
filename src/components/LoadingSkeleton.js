import React from 'react';
import './LoadingSkeleton.css';

const LoadingSkeleton = () => {
  return (
    <div className="loading-skeleton">
      <div className="skeleton-header">
        <div className="skeleton-title"></div>
        <div className="skeleton-status"></div>
      </div>
      
      <div className="skeleton-summary"></div>
      
      <div className="skeleton-details">
        <div className="skeleton-detail-row">
          <div className="skeleton-label"></div>
          <div className="skeleton-value"></div>
        </div>
        <div className="skeleton-detail-row">
          <div className="skeleton-label"></div>
          <div className="skeleton-value"></div>
        </div>
        <div className="skeleton-detail-row">
          <div className="skeleton-label"></div>
          <div className="skeleton-value"></div>
        </div>
      </div>
      
      <div className="skeleton-suggestion"></div>
      
      <div className="skeleton-footer">
        <div className="skeleton-source"></div>
        <div className="skeleton-powered"></div>
      </div>
    </div>
  );
};

export default LoadingSkeleton;

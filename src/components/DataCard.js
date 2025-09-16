import React from 'react';
import { ExternalLink, CheckCircle } from 'lucide-react';
import './DataCard.css';

const DataCard = ({ title, summary, details, suggestion, color = '#3498db' }) => {
  return (
    <div className="data-card" style={{ '--card-color': color }}>
      <div className="card-header">
        <div className="card-title">{title}</div>
        <div className="card-status">
          <CheckCircle size={16} />
          <span>Live Data</span>
        </div>
      </div>
      
      <div className="card-summary">
        {summary}
      </div>
      
      <div className="card-details">
        {details.map((detail, index) => (
          <div key={index} className="detail-row">
            <span className="detail-label">{detail.label}:</span>
            <span className="detail-value">{detail.value}</span>
          </div>
        ))}
      </div>
      
      {suggestion && (
        <div className="card-suggestion">
          <ExternalLink size={14} />
          <span>{suggestion}</span>
        </div>
      )}
      
      <div className="card-footer">
        <div className="data-source">Source: INGRES API • CGWB Database</div>
        <div className="powered-by">Powered by JalBuddy AI</div>
      </div>
    </div>
  );
};

export default DataCard;
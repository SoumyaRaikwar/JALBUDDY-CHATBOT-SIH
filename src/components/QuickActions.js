import React from 'react';
import { Droplets, CloudRain, MapPin, TestTube, FileText, Activity, Sprout } from 'lucide-react';
import './QuickActions.css';

const QuickActions = ({ language, onActionClick, isVisible }) => {
  const actions = [
    {
      key: 'groundwater',
      icon: <Droplets size={18} />,
      labelEn: 'Water Level',
      labelHi: 'जल स्तर',
      color: '#3498db'
    },
    {
      key: 'rainfall',
      icon: <CloudRain size={18} />,
      labelEn: 'Monsoon Impact',
      labelHi: 'मानसून प्रभाव',
      color: '#2ecc71'
    },
    {
      key: 'boring',
      icon: <MapPin size={18} />,
      labelEn: 'Boring Location',
      labelHi: 'बोरिंग स्थान',
      color: '#e67e22'
    },
    {
      key: 'irrigation',
      icon: <Sprout size={18} />,
      labelEn: 'Irrigation Advisory',
      labelHi: 'सिंचाई सलाह',
      color: '#f39c12'
    },
    {
      key: 'quality',
      icon: <TestTube size={18} />,
      labelEn: 'Water Quality',
      labelHi: 'जल गुणवत्ता',
      color: '#9b59b6'
    },
    {
      key: 'gec',
      icon: <FileText size={18} />,
      labelEn: 'GEC-2015',
      labelHi: 'GEC-2015',
      color: '#e74c3c'
    },
    {
      key: 'dwlr',
      icon: <Activity size={18} />,
      labelEn: 'Live DWLR',
      labelHi: 'लाइव DWLR',
      color: '#1abc9c'
    }
  ];

  if (!isVisible) return null;

  return (
    <div className="quick-actions">
      <div className="quick-actions-header">
        <span className="quick-actions-title">
          {language === 'hi' ? '🚀 त्वरित कार्य' : '🚀 Quick Actions'}
        </span>
        <span className="quick-actions-subtitle">
          {language === 'hi' ? 'डेमो सुविधाएं देखें' : 'Try demo features'}
        </span>
      </div>
      <div className="quick-actions-grid">
        {actions.map((action) => (
          <button
            key={action.key}
            className="quick-action-chip"
            onClick={() => onActionClick(action.key)}
            style={{ '--chip-color': action.color }}
          >
            <div className="chip-icon">
              {action.icon}
            </div>
            <span className="chip-label">
              {language === 'hi' ? action.labelHi : action.labelEn}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;
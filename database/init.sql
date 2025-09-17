-- jalBuddy Database Initialization Script
-- Smart India Hackathon 2025

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table for authentication and profiles
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(15) UNIQUE,
    whatsapp_id VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    language_preference VARCHAR(10) DEFAULT 'hi',
    location_district VARCHAR(100),
    location_state VARCHAR(100),
    user_type VARCHAR(20) DEFAULT 'farmer', -- farmer, official, expert
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat sessions for conversation tracking
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    platform VARCHAR(20) DEFAULT 'web', -- web, whatsapp, app
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat messages for conversation history
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message_type VARCHAR(20) NOT NULL, -- user_text, user_voice, bot_response
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'hi',
    confidence_score DECIMAL(3,2),
    processing_time_ms INTEGER,
    voice_duration_ms INTEGER,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- INGRES data cache for performance
CREATE TABLE ingres_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    block VARCHAR(100),
    data_type VARCHAR(50) NOT NULL, -- groundwater_level, quality, rainfall
    data_payload JSONB NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '1 hour',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DWLR monitoring stations
CREATE TABLE dwlr_stations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    station_id VARCHAR(20) UNIQUE NOT NULL,
    station_name VARCHAR(200),
    district VARCHAR(100),
    state VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    elevation DECIMAL(8, 2),
    installation_date DATE,
    is_active BOOLEAN DEFAULT true,
    last_reading_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DWLR readings for real-time monitoring
CREATE TABLE dwlr_readings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    station_id UUID REFERENCES dwlr_stations(id) ON DELETE CASCADE,
    water_level_m DECIMAL(8, 3) NOT NULL,
    battery_voltage DECIMAL(4, 2),
    signal_strength INTEGER,
    temperature_c DECIMAL(5, 2),
    reading_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    is_anomaly BOOLEAN DEFAULT false,
    quality_flag VARCHAR(10) DEFAULT 'GOOD', -- GOOD, SUSPECT, BAD
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alerts and notifications
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- water_level_low, quality_degraded, system_down
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    location_district VARCHAR(100),
    location_state VARCHAR(100),
    is_sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP WITH TIME ZONE,
    delivery_channels VARCHAR(100)[], -- web, whatsapp, sms
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Knowledge base for GEC-2015 and documentation
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_type VARCHAR(50) NOT NULL, -- gec2015, manual, faq, guideline
    title VARCHAR(300) NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    section_number VARCHAR(20),
    keywords TEXT[],
    embeddings VECTOR(768), -- For RAG similarity search (requires pgvector extension)
    source_file VARCHAR(200),
    page_number INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User preferences and settings
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    voice_alerts_enabled BOOLEAN DEFAULT true,
    whatsapp_alerts_enabled BOOLEAN DEFAULT true,
    sms_alerts_enabled BOOLEAN DEFAULT false,
    alert_frequency VARCHAR(20) DEFAULT 'weekly', -- daily, weekly, monthly
    preferred_units VARCHAR(10) DEFAULT 'metric',
    location_sharing_enabled BOOLEAN DEFAULT true,
    data_sync_wifi_only BOOLEAN DEFAULT false,
    offline_cache_enabled BOOLEAN DEFAULT true,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics and usage tracking
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_category VARCHAR(50),
    event_properties JSONB,
    user_agent TEXT,
    ip_address INET,
    platform VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_whatsapp ON users(whatsapp_id);
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_active ON chat_sessions(is_active);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created ON chat_messages(created_at DESC);
CREATE INDEX idx_ingres_cache_location ON ingres_cache(district, state, data_type);
CREATE INDEX idx_ingres_cache_expires ON ingres_cache(expires_at);
CREATE INDEX idx_dwlr_stations_active ON dwlr_stations(is_active);
CREATE INDEX idx_dwlr_readings_station_time ON dwlr_readings(station_id, reading_timestamp DESC);
CREATE INDEX idx_alerts_user_created ON alerts(user_id, created_at DESC);
CREATE INDEX idx_knowledge_base_type_lang ON knowledge_base(document_type, language);
CREATE INDEX idx_analytics_user_time ON analytics_events(user_id, created_at DESC);

-- Insert sample data for development
INSERT INTO users (phone_number, whatsapp_id, name, language_preference, location_district, location_state, user_type) VALUES
('9876543210', 'wa_user_001', 'Ramesh Kumar', 'hi', 'Nalanda', 'Bihar', 'farmer'),
('9876543211', 'wa_user_002', 'Priya Singh', 'hi', 'Jalgaon', 'Maharashtra', 'farmer'),
('9876543212', 'wa_user_003', 'Dr. A.K. Sharma', 'en', 'Anantapur', 'Andhra Pradesh', 'official');

-- Insert sample DWLR stations
INSERT INTO dwlr_stations (station_id, station_name, district, state, latitude, longitude, is_active) VALUES
('DWLR001', 'Nalanda Central Monitoring', 'Nalanda', 'Bihar', 25.1372, 85.4426, true),
('DWLR002', 'Jalgaon Agricultural Zone', 'Jalgaon', 'Maharashtra', 21.0077, 75.5626, true),
('DWLR003', 'Anantapur Hard Rock Region', 'Anantapur', 'Andhra Pradesh', 14.6819, 77.6006, true);

-- Insert sample knowledge base entries
INSERT INTO knowledge_base (document_type, title, content, language, section_number, keywords) VALUES
('gec2015', 'Groundwater Assessment Categories', 'As per GEC-2015 guidelines, groundwater assessment units are classified into four categories: Safe, Semi-Critical, Critical, and Over-Exploited based on stage of development and long-term water level trend.', 'en', '3.1', ARRAY['assessment', 'categories', 'safe', 'critical']),
('gec2015', 'भूजल मूल्यांकन श्रेणियां', 'GEC-2015 दिशानिर्देशों के अनुसार, भूजल मूल्यांकन इकाइयों को विकास के चरण और दीर्घकालिक जल स्तर की प्रवृत्ति के आधार पर चार श्रेणियों में वर्गीकृत किया गया है: सुरक्षित, अर्ध-महत्वपूर्ण, महत्वपूर्ण, और अति-दोहित।', 'hi', '3.1', ARRAY['मूल्यांकन', 'श्रेणी', 'सुरक्षित', 'महत्वपूर्ण']);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jalbuddy_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jalbuddy_user;
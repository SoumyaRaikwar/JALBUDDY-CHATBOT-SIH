#!/usr/bin/env python3
"""
WhatsApp Mock Service for JalBuddy
"""

from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """WhatsApp webhook endpoint"""
    if request.method == 'GET':
        # Verification
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == 'jalbuddy_verify_token':
            return challenge
        return 'Invalid verify token', 403
    
    elif request.method == 'POST':
        # Handle incoming messages
        data = request.get_json()
        logger.info(f"Received WhatsApp message: {data}")
        
        # Mock response
        return jsonify({
            "status": "success",
            "message": "Message received and processed"
        })

@app.route('/send', methods=['POST'])
def send_message():
    """Send WhatsApp message endpoint"""
    data = request.get_json()
    logger.info(f"Sending WhatsApp message: {data}")
    
    return jsonify({
        "status": "sent",
        "message_id": "mock_msg_123",
        "recipient": data.get('to', 'unknown')
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Mock Service"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

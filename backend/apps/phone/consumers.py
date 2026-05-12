import json
import asyncio
import threading
import telnetlib
import time
import logging
import socket
import ssl
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class AsteriskEventsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer that monitors Asterisk events and notifies clients
    about incoming calls to extension 809.
    """
    
    # Class variable to track active AMI connection
    ami_thread = None
    ami_running = False
    connected_clients = set()
    event_loop = None

    async def connect(self):
        await self.accept()
        AsteriskEventsConsumer.connected_clients.add(self)
        logger.info(f"✅ WebSocket client connected. Total clients: {len(AsteriskEventsConsumer.connected_clients)}")
        
        # Start AMI monitoring thread if not already running
        if not AsteriskEventsConsumer.ami_running:
            AsteriskEventsConsumer.ami_running = True
            AsteriskEventsConsumer.event_loop = asyncio.get_event_loop()
            AsteriskEventsConsumer.ami_thread = threading.Thread(
                target=AsteriskEventsConsumer.monitor_asterisk_events_static,
                daemon=True
            )
            AsteriskEventsConsumer.ami_thread.start()
            logger.info("🔄 Started AMI monitoring thread")

    async def disconnect(self, close_code):
        AsteriskEventsConsumer.connected_clients.discard(self)
        logger.info(f"⚠️ WebSocket client disconnected. Total clients: {len(AsteriskEventsConsumer.connected_clients)}")
        
        # Stop AMI thread if no more clients
        if len(AsteriskEventsConsumer.connected_clients) == 0:
            AsteriskEventsConsumer.ami_running = False
            logger.info("Stopped AMI monitoring (no clients)")

    async def receive(self, text_data):
        """Handle incoming messages from client"""
        try:
            data = json.loads(text_data)
            logger.debug(f"Message from client: {data}")
        except Exception as e:
            logger.error(f"Error parsing message: {e}")

    @staticmethod
    def monitor_asterisk_events_static():
        """
        Connect to Asterisk AMI and listen for events (static method for threading).
        When an INVITE comes for 809, notify all connected clients.
        """
        ami_user = "NAV_OKKTA"
        ami_pass = "Nav@2026AM!**"
        pbx_ip = "192.168.1.5"
        ami_port = 5039  # TLS port
        
        while AsteriskEventsConsumer.ami_running:
            try:
                logger.info("🔄 Connecting to Asterisk AMI (TLS)...")
                
                # Create SSL context for TLS connection
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE  # For self-signed certificates
                
                # Connect using TLS
                sock = socket.create_connection((pbx_ip, ami_port), timeout=10)
                tn = context.wrap_socket(sock, server_hostname=pbx_ip)
                
                # Read initial response
                response = tn.recv(1024).decode(errors='ignore')
                if "Asterisk Call Manager" not in response:
                    logger.error(f"❌ Invalid AMI response: {response}")
                    tn.close()
                    time.sleep(5)
                    continue
                
                # LOGIN with events enabled
                login_cmd = f"""Action: Login
Username: {ami_user}
Secret: {ami_pass}
Events: on

""".encode()
                tn.send(login_cmd)
                
                time.sleep(0.5)
                response = tn.recv(1024).decode(errors='ignore')
                logger.info(f"✅ Connected to Asterisk AMI (TLS)")
                
                # Listen for events
                while AsteriskEventsConsumer.ami_running:
                    try:
                        # Set socket timeout
                        tn.settimeout(0.5)
                        data = tn.recv(4096).decode(errors='ignore')
                        
                        if data:
                            event_str = data
                            
                            # Check if this is an incoming call to 809
                            if 'Exten: 809' in event_str or 'CallerIDNum' in event_str:
                                logger.info(f"📞 Asterisk event for 809:\n{event_str[:300]}")
                                
                                # Extract caller info
                                lines = event_str.split('\n')
                                caller_id = "Unknown"
                                channel = "Unknown"
                                
                                for line in lines:
                                    if 'CallerIDNum:' in line:
                                        caller_id = line.split(':', 1)[1].strip()
                                    if 'Channel:' in line and channel == "Unknown":
                                        channel = line.split(':', 1)[1].strip()
                                
                                # Notify all connected clients (thread-safe)
                                if AsteriskEventsConsumer.event_loop:
                                    asyncio.run_coroutine_threadsafe(
                                        AsteriskEventsConsumer.notify_all_clients({
                                            'type': 'incoming_call',
                                            'caller_id': caller_id,
                                            'channel': channel,
                                            'timestamp': str(now())
                                        }),
                                        AsteriskEventsConsumer.event_loop
                                    )
                        
                        time.sleep(0.1)
                    except socket.timeout:
                        continue
                    except Exception as e:
                        logger.warning(f"Error reading AMI: {e}")
                        break
                
                tn.close()
                
            except Exception as e:
                logger.error(f"❌ AMI connection error: {e}")
                if AsteriskEventsConsumer.ami_running:
                    time.sleep(5)  # Wait before retrying

    @staticmethod
    async def notify_all_clients(message):
        """Send message to all connected clients (thread-safe)"""
        disconnected = set()
        for client in list(AsteriskEventsConsumer.connected_clients):
            try:
                await client.send(text_data=json.dumps(message))
                logger.debug(f"📨 Sent to client: {message['type']}")
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(client)
        
        # Remove disconnected clients
        AsteriskEventsConsumer.connected_clients -= disconnected

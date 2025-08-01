"""
Data storage module for InquiryCircle.
Handles JSON file persistence for circles and keys.
"""
import json
import os
from pathlib import Path
from django.conf import settings
from decouple import config
import logging

logger = logging.getLogger(__name__)

class DataStorage:
    """Handles persistent storage of circles and keys in JSON files."""
    
    def __init__(self):
        self.data_dir = Path(settings.BASE_DIR) / config('DATA_DIR', default='data')
        self.circles_file = self.data_dir / config('CIRCLES_FILE', default='circles.json')
        self.keys_file = self.data_dir / config('KEYS_FILE', default='keys.json')
        
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize with default data if files don't exist
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize with default circles and keys if files don't exist."""
        if not self.circles_file.exists():
            default_circles = {
                'demo-circle': {
                    'id': 'demo-circle',
                    'name': 'Demo Circle',
                    'jitsi_room': f"{settings.JITSI_ROOM_PREFIX}demo-circle",
                    'created_by': 'admin-master-key',
                    'active': True
                }
            }
            self.save_circles(default_circles)
            logger.info("Initialized default circles data")
        
        if not self.keys_file.exists():
            default_keys = {
                'admin-master-key': {'type': 'admin', 'name': 'Admin'},
                'facilitator-demo': {'type': 'facilitator', 'circle_id': 'demo-circle', 'name': 'Demo Facilitator'},
                'participant-demo': {'type': 'participant', 'circle_id': 'demo-circle', 'name': 'Demo Participant'},
            }
            self.save_keys(default_keys)
            logger.info("Initialized default keys data")
    
    def load_circles(self):
        """Load circles from JSON file."""
        try:
            if self.circles_file.exists():
                with open(self.circles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading circles: {e}")
            return {}
    
    def save_circles(self, circles):
        """Save circles to JSON file."""
        try:
            with open(self.circles_file, 'w', encoding='utf-8') as f:
                json.dump(circles, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved {len(circles)} circles to {self.circles_file}")
        except IOError as e:
            logger.error(f"Error saving circles: {e}")
    
    def load_keys(self):
        """Load keys from JSON file."""
        try:
            if self.keys_file.exists():
                with open(self.keys_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading keys: {e}")
            return {}
    
    def save_keys(self, keys):
        """Save keys to JSON file."""
        try:
            with open(self.keys_file, 'w', encoding='utf-8') as f:
                json.dump(keys, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved {len(keys)} keys to {self.keys_file}")
        except IOError as e:
            logger.error(f"Error saving keys: {e}")
    
    def backup_data(self):
        """Create backup copies of data files."""
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            if self.circles_file.exists():
                backup_circles = self.data_dir / f"circles_backup_{timestamp}.json"
                backup_circles.write_text(self.circles_file.read_text())
                logger.info(f"Created circles backup: {backup_circles}")
            
            if self.keys_file.exists():
                backup_keys = self.data_dir / f"keys_backup_{timestamp}.json"
                backup_keys.write_text(self.keys_file.read_text())
                logger.info(f"Created keys backup: {backup_keys}")
                
        except IOError as e:
            logger.error(f"Error creating backup: {e}")

# Global storage instance
storage = DataStorage()

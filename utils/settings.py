"""
Centralized settings/configuration management for the test framework.
Loads environment variables from .env file and provides easy access via class properties.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """
    Centralized configuration class that loads and manages all environment variables.
    
    Usage:
        from utils.settings import Settings
        
        # Access settings
        city = Settings.delivery_city
        url = Settings.base_url
    """
    
    # Load .env file when class is imported
    _env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=_env_path)
    
    # ========== Test Environment ==========
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> str:
        """Helper method to get environment variable with optional default."""
        return os.getenv(key, default)
    
    # Test Environment
    TEST_ENV: str = get_env.__func__('TEST_ENV', 'dev')
    BASE_URL: str = get_env.__func__('BASE_URL', 'https://www.shufersal.co.il/online/he')
    
    # ========== Browser Settings ==========
    HEADLESS: bool = get_env.__func__('HEADLESS', 'false').lower() == 'true'
    SLOW_MO: int = int(get_env.__func__('SLOW_MO', '500'))
    BROWSER_TIMEOUT: int = int(get_env.__func__('BROWSER_TIMEOUT', '30000'))
    
    # ========== Reporting ==========
    SCREENSHOT_ON_FAILURE: bool = get_env.__func__('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    VIDEO_ON_FAILURE: bool = get_env.__func__('VIDEO_ON_FAILURE', 'false').lower() == 'true'
    
    # ========== Delivery Address ==========
    DELIVERY_CITY: str = get_env.__func__('DELIVERY_CITY', 'תל אביב')
    DELIVERY_STREET: str = get_env.__func__('DELIVERY_STREET', 'דיזנגוף')
    DELIVERY_STREET_NUMBER: str = get_env.__func__('DELIVERY_STREET_NUMBER', '1')
    DELIVERY_APARTMENT: str = get_env.__func__('DELIVERY_APARTMENT', '1')
    
    # ========== Delivery Time Slot ==========
    DELIVERY_DATE: str = get_env.__func__('DELIVERY_DATE', '20251104')
    DELIVERY_TIME: str = get_env.__func__('DELIVERY_TIME', '14:00')
    
    @classmethod
    def reload(cls):
        """Reload environment variables from .env file. Useful for testing."""
        load_dotenv(dotenv_path=cls._env_path, override=True)
        # Re-initialize all settings
        cls.TEST_ENV = cls.get_env('TEST_ENV', 'dev')
        cls.BASE_URL = cls.get_env('BASE_URL', 'https://www.shufersal.co.il/online/he')
        cls.HEADLESS = cls.get_env('HEADLESS', 'false').lower() == 'true'
        cls.SLOW_MO = int(cls.get_env('SLOW_MO', '500'))
        cls.BROWSER_TIMEOUT = int(cls.get_env('BROWSER_TIMEOUT', '30000'))
        cls.SCREENSHOT_ON_FAILURE = cls.get_env('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
        cls.VIDEO_ON_FAILURE = cls.get_env('VIDEO_ON_FAILURE', 'false').lower() == 'true'
        cls.DELIVERY_CITY = cls.get_env('DELIVERY_CITY', 'תל אביב')
        cls.DELIVERY_STREET = cls.get_env('DELIVERY_STREET', 'דיזנגוף')
        cls.DELIVERY_STREET_NUMBER = cls.get_env('DELIVERY_STREET_NUMBER', '1')
        cls.DELIVERY_APARTMENT = cls.get_env('DELIVERY_APARTMENT', '1')
        cls.DELIVERY_DATE = cls.get_env('DELIVERY_DATE', '20251104')
        cls.DELIVERY_TIME = cls.get_env('DELIVERY_TIME', '14:00')
    
    @classmethod
    def get_full_address(cls) -> str:
        """Get formatted full delivery address."""
        return f"{cls.DELIVERY_STREET} {cls.DELIVERY_STREET_NUMBER}, Apt {cls.DELIVERY_APARTMENT}, {cls.DELIVERY_CITY}"
    
    @classmethod
    def get_delivery_datetime(cls) -> str:
        """Get formatted delivery date and time."""
        # Format: YYYYMMDD -> DD/MM/YYYY
        date = cls.DELIVERY_DATE
        formatted_date = f"{date[6:8]}/{date[4:6]}/{date[0:4]}"
        return f"{formatted_date} at {cls.DELIVERY_TIME}"
    
    @classmethod
    def print_config(cls):
        """Print all current configuration values. Useful for debugging."""
        print("\n" + "="*50)
        print("CURRENT CONFIGURATION")
        print("="*50)
        print(f"Test Environment: {cls.TEST_ENV}")
        print(f"Base URL: {cls.BASE_URL}")
        print(f"Headless Mode: {cls.HEADLESS}")
        print(f"Slow Motion: {cls.SLOW_MO}ms")
        print(f"Browser Timeout: {cls.BROWSER_TIMEOUT}ms")
        print(f"Screenshot on Failure: {cls.SCREENSHOT_ON_FAILURE}")
        print(f"Video on Failure: {cls.VIDEO_ON_FAILURE}")
        print(f"\nDelivery Address:")
        print(f"  {cls.get_full_address()}")
        print(f"\nDelivery Time:")
        print(f"  {cls.get_delivery_datetime()}")
        print("="*50 + "\n")

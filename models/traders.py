import datetime
from datetime import timezone


# Class of traders
class TradersDB:
    __table_name__ = 'test_trader'
    id = 'id'
    user_id = 'user_id'
    is_verified = 'is_verified'
    is_active = 'is_active'
    bio = 'bio'
    created_at = 'created_at'
    updated_at = 'updated_at'
    secret_key = 'secret_key'
    api_key = 'api_key'
    exchange = 'exchange'

    def __init__(self):
        self.created_at = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.updated_at = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")

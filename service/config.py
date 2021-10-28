import os
# Vkontakte

access_token = os.environ['ACCESS_TOKEN']
user_id = os.environ['USER_ID']
key = os.environ['SAFE_KEY']

chunk_size = int(os.environ.get('CHUNK_SIZE', '100'))

backend_url = os.environ['BACKEND_URL']

time_delay = os.environ['TIME_DELAY']

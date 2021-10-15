import os
# Vkontakte

access_token = os.environ['ACCESS_TOKEN']
user_id = os.environ['USER_ID']
key = os.environ['SAFE_KEY']

# Some examples of groups in VK (we need their ID)
owner_id = os.environ['OWNER_ID']
pr_owner_id = os.environ['PR_OWNER_ID']
py_owner_id = os.environ['PY_OWNER_ID']
ro_owner_id = os.environ['RO_OWNER_ID']

groups = os.environ['GROUPS'].split(',')

backend_url = os.environ['BACKEND_URL']

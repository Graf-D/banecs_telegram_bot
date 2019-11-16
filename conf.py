try:
    with open('tg_access_token.txt', 'r') as f:
        TG_ACCESS_TOKEN = f.read().strip()
except OSError:
    TG_ACCESS_TOKEN = None

try:
    with open('vk_access_token.txt', 'r') as f:
        VK_ACCESS_TOKEN = f.read().strip()
except OSError:
    VK_ACCESS_TOKEN = None

OWNER_ID = '-45491419'
VERSION = '5.95'

PROXY = None  # fill in with proxy url if needed

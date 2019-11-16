with open('tg_access_token.txt', 'r') as f:
    TG_ACCESS_TOKEN = f.read().strip()

with open('vk_access_token.txt', 'r') as f:
    VK_ACCESS_TOKEN = f.read().strip()

OWNER_ID = '-45491419'
VERSION = '5.95'

PROXY = 'socks5h://geek:socks@t.geekclass.ru:7777'
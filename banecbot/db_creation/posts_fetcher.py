import vk
import time
import conf
import itertools
from banecbot.db_creation.post import Post


def fetch_posts():
    session = vk.Session(access_token=conf.VK_ACCESS_TOKEN)
    vk_api = vk.API(session)

    posts = []

    for i in itertools.count():
        curr_response = vk_api.wall.get(
            owner_id=conf.OWNER_ID,
            v=conf.VERSION,
            count=100,
            offset=100 * i
        )
        
        if not curr_response['items']:
            break

        for raw_post in curr_response['items']:
            if 'attachments' not in raw_post:
                yield Post(
                    raw_post['id'],
                    raw_post['date'],
                    raw_post['text'],
                    raw_post['likes']['count']
                )
        
        time.sleep(0.3)

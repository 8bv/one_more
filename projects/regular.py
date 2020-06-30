# import module
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# enter your access token
access_token = '1e8a5f4a1ef6e969ceebe2ff585bc6e2abee5b7ccd9da5e821ebba6a5edc1a1f3c944fed88d1b03e6d439'

# define API version
api_version = 5.103

# link to the API method that is used to download wall posts
# full description of API methods is available at https://vk.com/dev.php?method=methods
wall_get = 'https://api.vk.com/method/wall.get'


texts = []
likes = []
post_id = []
date = []
views = []
comments = []
is_pinned = []

# define parameters
for i in range(0, 401, 100):
    p = {
        'domain': 'hse_ir', # link to the VK community
        'filter': 'all',    # filter to apply on posts
        'count': 100,       # number of posts to download (maximum 100)
        'offset': i,        # define subset of posts
        'access_token': access_token,
        'v': api_version
        }

    # request data
    res_wall = requests.get(url = wall_get, params = p)

    for post in res_wall.json()['response']['items']: #каждый итерируемый объект
        texts.append(post['text'])
        likes.append(post['likes']['count'])
        post_id.append(post['id'])
        date.append(post['date'])
        if 'views' in post.keys():
            views.append(post['views']['count'])
        else:
            views.append(0)
        comments.append(post['comments']['count'])

        if 'is_pinned' in post.keys():
            is_pinned.append(post['is_pinned'])
        else:
            is_pinned.append(0)



# just basic functions
# rint(max(x), min(x), len(x), np.mean(x))

# print(plt.plot(likes))
# print(plt.show())

data = pd.DataFrame({
'post_id': post_id, 'text': texts, 'date': date,
'likes': likes, 'views': views, 'comments': comments, 'is_pinned': is_pinned
}) # создаем дата фрейм (таблицу)
# создаем новую колонку
data['new_date'] = pd.to_datetime(data['date'], unit = 's')
# сортировка по new_date
data = data.sort_values(by = 'new_date', ascending = True)

# plot likes against posts
# plt.plot(list(range(1, 445)), data['likes'])
# plt.show()
# plot number of likes against time
# data.plot(x = 'new_date', y = 'likes')
# plt.show()

# plt.plot(list(range(1, 445)), data['views'])
# plt.show()

data['likes_to_views'] = data['likes'] / data['views']
# plt.plot(list(range(1, 445)), data['likes_to_views'])

# likes against views: scatter plot - график разброса
# plt.scatter(x = data.views, y = data.likes)
# plt.xlim(-50, 3000)
# plt.ylim(-10, 75)
# plt.show()

data.to_excel('some_stat.xlsx', engine = 'xlsxwriter')

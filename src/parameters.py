langs = 'ar', 'es', 'fr', 'hi', 'ja', 'pt', 'zh-CN'


num_links = 4

platforms = {"youtube": lambda s: f"https://www.youtube.com/results?search_query={s}&sp=EgYIBBABGAE%3D"}
#             "dailymotion": lambda s: f"https://www.dailymotion.com/search/{s}/videos?duration=mins_1_5&dateRange=past_month"}

# youtube_regex = re.compile(r'watch\?v=(.+?)"')
# dailymotion_regex = re.compile(r'href="/video/(.+?)"')

import os
os.environ['MOZ_HEADLESS'] = '1'


filter_colour = [150, 0, 255]


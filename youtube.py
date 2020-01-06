#Loading Required Libraries
import numpy as np
import pandas as pd
from pandas import DataFrame
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

#reading CSV file
videos= pd.read_csv("USvideos.csv")
#reading JSON categories file
vid_categories= pd.read_json("US_category_id.json")
#exploring the data
print(videos.head(1))
print(videos.info())
print(vid_categories.info())
print(vid_categories.head(1))

#using python's dictionary comprehension  to map categories with their respective ID's
categories = {category['id']: category['snippet']['title'] for category in vid_categories['items']}
#inserting a column for category
videos.insert(4, 'category', videos['category_id'].astype(str).map(categories))
print(videos.head(1))
print(videos.info())
#Creating columnns for like,dislike and comment  percentages
videos['like_pct'] = videos['likes'] / (videos['dislikes'] + videos['likes']) * 100
videos['dislike_pct'] = videos['dislikes'] / (videos['dislikes'] + videos['likes']) * 100
videos['comment_pct'] = videos['comment_count'] / videos['views'] * 100
videos.sort_values('views', ascending=False, inplace=True)
#dropping duplicates as 1 video can be a trending many times
videos.drop_duplicates(subset='video_id',keep='first', inplace=True)
pd.options.display.float_format = "{:,.0f}".format
print(videos.describe().iloc[:,1:5])
pd.options.display.float_format = "{:,.2f}".format
#Top 10 videos with highest views
top10_videos_views = videos.nlargest(10, 'views')
print(top10_videos_views['title'])
# top 10 videos with highest likes
top10_videos_likes =videos.nlargest(10, 'likes')
print(top10_videos_likes['title'])


#wordcloud for Titles
text = " ".join(title for title in videos.title)
plt.figure(figsize = (10, 12))
title_cloud = WordCloud(background_color = "white").generate(text)
plt.imshow(title_cloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

#wordcloud for tags
text = " ".join(tags for tags in videos.tags)
plt.figure(figsize = (10, 12))
tag_cloud = WordCloud(background_color = "white").generate(text)
plt.imshow(tag_cloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

#Converting the trending date and Publish Time to appropriate format.
videos['trending_date'] = pd.to_datetime(videos['trending_date'], format='%y.%d.%m').dt.date
publish_time = pd.to_datetime(videos['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
videos['publish_date'] = publish_time.dt.date
videos['publish_time'] = publish_time.dt.time
videos['publish_hour'] = publish_time.dt.hour

#create a plot to analyse best publish time for a video to become trending
publish_h = [0] * 24

for index, row in videos.iterrows():
    publish_h[row["publish_hour"]] += 1
    
values = publish_h
ind = np.arange(len(values))
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
ax.yaxis.grid()
ax.xaxis.grid()
bars = ax.bar(ind, values)

plt.ylabel('Number of videos that got trending', fontsize=20)
plt.xlabel('Time of publishing', fontsize=20)
plt.title('Best time to publish video (USA)', fontsize=35, fontweight='bold')
plt.xticks(np.arange(0, len(ind), len(ind)/6), [0, 4, 8, 12, 16, 20])

plt.show()



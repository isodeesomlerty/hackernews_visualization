from operator import itemgetter

import requests
import plotly.express as px

# Make an API call and check the response.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:5]:
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
        }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                          reverse=True)

articles, comments, hover_texts = [], [], []

for submission_dict in submission_dicts:
    # Turn article title into active links.
    url = submission_dict['hn_link']
    article_title = str(submission_dict['title'])
    article = f"<a href='{url}'>{article_title}</a>"
    articles.append(article)

    comment = submission_dict['comments']
    comments.append(comment)

    # Build hover texts.
    hover_text = f"{article_title}<br />Comments: {comment}"
    hover_texts.append(hover_text)

# Make visualization.
chart_title = "Most Active Hacker News Discussions"
labels = {'x': 'Article Title', 'y': 'Number of Comments'}
fig = px.bar(x=articles, y=comments, title=chart_title, labels=labels)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
                    yaxis_title_font_size=20)

fig.update_traces(marker_color='Olive', marker_opacity=0.6)

fig.show()
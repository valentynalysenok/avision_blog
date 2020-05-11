# Avision Blog

## Overview
#### Django3, PostgreSQL
Basic models:<br />
- `CustomUser` (sign in / signup)<br />
    - Used **hunter.io** for verifying email existence on signup
    - Used **clearbit.com** for getting additional data for the user on signup (user's first and last name)
- `Post` (made by a registered user)<br />
    - Post CRUD operations by using **Class-based views Django**
    - Share post by using **email / custom logic** (Gmail-serever)
    - Share post by using **django-social-share** (Facebook, LinkedIn, Twitter, Telegram, WhatsApp)
- `Comment` (made by a registered user)<br />
    - Send email to an author when the comment was added
- `Category` (post categorization)
- `Tags` by using **django_taggit**
- `Contact` (for sent message using contact form)
- **Recommendation** system of posts (list of similar posts)
- **Like vs Dislike** for registered user

Other functionality:<br />
- Created custom **Template Tags** 
    - {% load blog_tags %} {% total_posts %}
    - {% show_latest_posts %}
    - {% get_most_commented_posts %}
- Created custom **Filters**
    - **Markdown** view
- Added Site Map **PostSitemap**
- **RSS feed** for posts
- Search posts using **SearchVector**, **SearchQuery**, **SearchRank** from PostgreSQL

## Deploy project on your local machine

1 - To deploy project on your local machine create new virtual environment and execute this command:

`pip install -r requirements.txt`

2 - Insert your own db configuration settings (see example.env):
and change file name to .env:

`SECRET_KEY`,

`DB_PASSWORD`,
`DB_NAME`,
`DB_USER`

`EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD`

3 - Migrate db models to PostgreSQL:

`python3 manage.py migrate`

4 - Load data from JSON files:

`python3 manage.py loaddata posts.json`
`python3 manage.py loaddata users.json`

5 - Run app:

`python3 manage.py runserver`

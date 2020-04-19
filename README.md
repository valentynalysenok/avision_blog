# Avision Blog

## Overview
Basic models:<br />
- User (sign in / signup)<br />
    - Used **hunter.io** for verifying email existence on signup
    - Used **clearbit.com** for getting additional data for the user on signup (user's first and last name)
- Post (made by a registered user)<br />
    - Post CRUD operations by using **Class-based views Django**
    - Share post by using **email / custom logic** (Gmail-serever)
    - Share post by using **django-social-share** (Facebook, LinkedIn, Twitter, Telegram, WhatsApp)
- Comment (made by a registered user)<br />
    - Send email to an author when the comment was added
- Tags by using **django_taggit**
- **Recommendation** system of posts (list of similar posts)

Other functionality:<br />
- Created custom **Template Tags** 
    - {% load blog_tags %} {% total_posts %}
    - {% show_latest_posts %}
    - {% get_most_commented_posts %}
- Created custom **Filters**
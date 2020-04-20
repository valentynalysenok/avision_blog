from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Avision Blog'
    link = '/posts/'
    description = 'See new posts.'

    def items(self):
        return Post.objects.filter(status='published')[:6]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

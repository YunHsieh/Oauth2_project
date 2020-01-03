
from elasticsearch_dsl import Document, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from django_elasticsearch_dsl.registries import registry
from . import models

@registry.register_document
class BlogPostIndex(Document):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Django:
        model = blog
        fields = [
            'author',
            'posted_date',
            'text',
            'title',
        ]

    class Index:
        name = 'blog'
        index = 'blogpost-index'
        settings = {
          "number_of_shards": 2,
        }

def bulk_indexing():
    connections.create_connection(hosts=['localhost'])

    connections.get_connection().cluster.health()

    BlogPostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))
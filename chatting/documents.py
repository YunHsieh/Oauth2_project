from elasticsearch_dsl import analyzer

from django_elasticsearch_dsl import Document , Index, fields

from chatting import models as articles_models
from django_elasticsearch_dsl.registries import registry
from .models import *

article_index = Index('chatting')
article_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)  

@registry.register_document
class BlogPostIndex(Document):
    manufacturer = fields.ObjectField(properties={
        'name': fields.TextField(),
        'date': fields.DateField(),
        'country': fields.TextField(),
        'logo': fields.FileField(),
    })

    class Django:
        model = blog
        # index = 'test_ads'
        fields = [
            'author',
            'posted_date',
            'text',
            'title',
        ]

    class Index:
        name = 'blog'
# @registry.register_document
# class ArticleDocument(Document):
#     """Article elasticsearch document"""

#     id = fields.IntegerField(attr='id')
#     title = fields.TextField(
#         analyzer=html_strip,
#         fields={
#             'raw': fields.TextField(analyzer='keyword'),
#         }
#     )
#     body = fields.TextField(
#         analyzer=html_strip,
#         fields={
#             'raw': fields.TextField(analyzer='keyword'),
#         }
#     )
#     author = fields.IntegerField(attr='author_id')
#     created = fields.DateField()
#     modified = fields.DateField()
#     pub_date = fields.DateField()
#     class Django:
#         model = Car
#         fields = [
#             'name',
#             'color',
#         ]
#     class Meta:
#         model = articles_models.Article 


# class CarDocument(Document):
#     # add a string field to the Elasticsearch mapping called type, the
#     # value of which is derived from the model's type_to_string attribute
#     type = fields.TextField(attr="type_to_string")

#     class Django:
#         model = Car
#         # we removed the type field from here
#         fields = [
#             'name',
#             'color',
#             'description',
#         ]
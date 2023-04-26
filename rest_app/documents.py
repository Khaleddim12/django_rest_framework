from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    class Django:
        model = Product
        fields = [
            'name',
            'price',
        ]
        
# Ignore auto updating of Elasticsearch when a model is saved
# or deleted:
# ignore_signals = True

# Don't perform an index refresh after every update (overrides global setting):
# auto_refresh = False

# Paginate the django queryset used to populate the index with the specified size
# (by default it uses the database driver's default setting)
# queryset_pagination = 5000
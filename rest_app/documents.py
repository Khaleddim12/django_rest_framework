from django_elasticsearch_dsl import Document, fields, Index
from .models import Product
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class ProductDocument(Document):
    title = fields.TextField(
        attr="title",
        fields={
            "raw": fields.TextField(),
            "suggest": fields.CompletionField(),
        },
    )
    price = fields.IntegerField(
        attr="price",
        fields={
            "raw": fields.IntegerField(),
        },
    )

    class Index:
        name = "product"

    class Django:
        model = Product
        

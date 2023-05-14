from django_elasticsearch_dsl.registries import registry
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .documents import ProductDocument


@receiver(post_save, sender=Product)
def update_document(sender, instance, **kwargs):
    registry.update(instance)


@receiver(post_delete, sender=Product)
def delete_document(sender, instance, **kwargs):
    registry.delete(instance, raise_on_error=False)

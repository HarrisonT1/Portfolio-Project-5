# Standard libary imports
# Third-party imports
# Django imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Local imports
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    """
    Updates the parent order total when a line item is saved
    """
    if instance.order:
        instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Updates the parent order total when a line item is removed
    """
    if instance.order:
        instance.order.update_total()

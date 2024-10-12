from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Borrower, Lender


@receiver(post_save, sender=User)
def create_borrower_lender(sender, instance, created, **kwargs):
    if instance.is_borrower and not (Borrower.objects.filter(user=instance).exists()
                                     or Borrower.objects.all_with_deleted().filter(user=instance)):
        Borrower.objects.create(user=instance,
                                name=instance.name,
                                contact_info=instance.contact_info,
                                create_at=instance.create_at,
                                is_valid=instance.is_valid,
                                avatar=instance.avatar)

    if instance.is_lender and not (Lender.objects.filter(user=instance).exists()
                                   or Lender.objects.all_with_deleted().filter(user=instance)):
        Lender.objects.create(user=instance,
                              name=instance.name,
                              contact_info=instance.contact_info,
                              create_at=instance.create_at,
                              is_valid=instance.is_valid,
                              avatar=instance.avatar)


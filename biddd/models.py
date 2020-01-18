from django.db import models

#Added for the Paytm payment
from django.conf import settings
from django.utils import timezone

#Added for the automatic delete the files on deleting an object from model
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.
# class TableName(models.Model):
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, )
#     u_id = models.IntegerField(primary_key=True, blank=False, null=False)
#     available_bid = models.IntegerField( default=0, blank=True, null=True)

#     class Meta:
#         db_table = 'table_name'

class PaytmHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_paytm', on_delete=models.CASCADE, null=True, default=None)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=64)
    BANKTXNID = models.IntegerField('BANK TXN ID', null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        app_label = 'biddd'
        unique_together = (("ORDERID", "TXNID"),)

    def __unicode__(self):
        return self.STATUS


class Available_bids(models.Model):
#   user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='available_bid', on_delete=models.CASCADE, null=True, default=None)
    available_bid = models.PositiveIntegerField(default=0,)

    class Meta:
        db_table = 'Available_bids_table'


class LiveSession(models.Model):
    end_time = models.DateTimeField(default=timezone.now)
    product_name = models.CharField(max_length=200, editable=True, )
    product_price = models.CharField(max_length=10, editable=True, )
    product_dcrp = models.TextField(max_length=200, editable=True, blank='True' )
    product_image = models.ImageField(upload_to='liveSession/', blank='True', editable=True, )

    class Meta:
        db_table = 'Live_session_table'

@receiver(post_delete, sender=LiveSession)
def submission_delete(sender, instance, **kwargs):
    instance.product_image.delete(False) 

class Placed_bids(models.Model):
    # user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='placed_bid', on_delete=models.CASCADE, null=True, default=None)
    bid_value = models.CharField(max_length=10, blank=False, null=False, unique=False,)
    product = models.ForeignKey(LiveSession, on_delete=models.CASCADE, blank='False', default=1,)

    class Meta:
        db_table = 'Placed_bids_table'


class Winners(models.Model):
    user_name = models.CharField(max_length=200, editable=True, )
    winning_bid_value = models.CharField(max_length=10, blank=True, null=True, unique=False, editable=True, )
    winning_product_name = models.CharField(max_length=20, editable=True,)
    winning_product_price = models.CharField(max_length=10, editable=True,)
    winning_product_image = models.ImageField(upload_to='winners/', blank='True', editable=True, )
    
    class Meta:
        db_table = 'Winners_table'

    def __str__(self):
        return '%s | %s | %s' % (self.user_name, self.winning_product_name, self.winning_product_price)
    
# @receiver(post_delete, sender=Winners)
# def submission_delete(sender, instance, **kwargs):
# instance.winning_product_image.delete(False) 

# @receiver(post_delete, sender=ClosedSession)
# def submission_delete(sender, instance, **kwargs):
#     instance.product_image.delete(False) 
# PaytmHistory

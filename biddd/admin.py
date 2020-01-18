from django.contrib import admin
from .models import Available_bids, Placed_bids, Winners, LiveSession, PaytmHistory
from django.contrib.auth.models import Group
import sys
from import_export.admin import ImportExportModelAdmin
#Changing the look of your admin panel
admin.site.site_header = "Bid 2 Win Administration"
admin.site.index_title = "Database Management"
admin.site.site_title = "Control Panel"

# Register your models here.
admin.site.unregister(Group)
class PaytmHistoryAdmin(ImportExportModelAdmin):
    list_display = ('user', 'MID', 'TXNAMOUNT', 'STATUS')

admin.site.register(PaytmHistory, PaytmHistoryAdmin)

class Available_bidsAdmin(ImportExportModelAdmin):
    list_display = ('user', 'available_bid')

admin.site.register(Available_bids, Available_bidsAdmin) 

class Placed_bidsAdmin(ImportExportModelAdmin):
    list_display = ('user', 'bid_value', 'product')
    search_fields = ('bid_value',)
    list_filter = ('bid_value', 'product')
    list_per_page = sys.maxsize
    # date_hierarchy = 'added_on'

admin.site.register(Placed_bids, Placed_bidsAdmin)

class WinnersAdmin(ImportExportModelAdmin):
    list_display = ('user_name', 'winning_bid_value', 'winning_product_name', 'winning_product_price')

admin.site.register(Winners, WinnersAdmin)

class LiveSessionAdmin(ImportExportModelAdmin):
    list_display = ('product_name', 'product_price', 'end_time')

admin.site.register(LiveSession, LiveSessionAdmin)

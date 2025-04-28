
from django.contrib import admin
from .models import QueryLog

@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'timestamp', 'tone', 'intent')
    search_fields = ('query', 'tone', 'intent')
    list_filter = ('tone', 'intent', 'timestamp')
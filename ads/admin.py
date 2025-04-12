from django.contrib import admin
from .models import Category, Condition, Ad, ExchangeProposal


class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "condition", "created_at")
    list_filter = ("category", "condition", "created_at")
    search_fields = ("title", "description")


class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ("ad_sender", "ad_receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("comment",)


admin.site.register(Category)
admin.site.register(Condition)
admin.site.register(Ad, AdAdmin)
admin.site.register(ExchangeProposal, ExchangeProposalAdmin)

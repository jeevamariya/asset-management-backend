from django.contrib import admin
from .models import Asset,InventoryItem,Assignment,RepairTicket, AIConversation, AIMessage

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name","type","serial_number","status","purchase_date")
    list_filter = ("status","type","purchase_date")
    search_fields = ("name","serial_number")
    ordering = ("-purchase_date",)

@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("item_type","quantity","threshold")
    list_filter = ("item_type",)
    search_fields = ("item_type",)
    ordering = ("item_type",)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("asset","employee","date_assigned","date_returned")
    list_filter = ("date_assigned","date_returned")
    search_fields = ("asset__name","asset__serial_number","employee__username")
    ordering = ("-date_assigned",)

@admin.register(RepairTicket)
class RepairTicketAdmin(admin.ModelAdmin):
    list_display = ("asset","issue","status","assigned_technician")
    list_filter = ("status",)
    search_fields = ("asset__name","asset__serial_number","issue","assigned_technician__username")
    ordering = ("status",)


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__username",
        "title",
    )
    ordering = ("-updated_at",)


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "role",
        "created_at",
    )
    list_filter = ("role",)
    search_fields = ("content",)
    ordering = ("-created_at",)
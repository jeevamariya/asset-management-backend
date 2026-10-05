from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet,InventoryItemViewSet,AssignmentViewSet,RepairTicketViewSet,dashboard_analytics,current_user,users_list, ai_chat, ai_conversations

router = DefaultRouter()
router.register("assets", AssetViewSet)
router.register("inventory", InventoryItemViewSet)
router.register("assignments", AssignmentViewSet)
router.register("tickets", RepairTicketViewSet)

urlpatterns = [
    path("dashboard/",dashboard_analytics,name="dashboard-analytics"),
    path('me/', current_user,name='current-user'),
    path('users/', users_list, name='users-list'),
    path('ai/chat/', ai_chat, name='ai-chat'),
    path('ai/conversations/', ai_conversations, name='ai-conversations'),
]

urlpatterns += router.urls
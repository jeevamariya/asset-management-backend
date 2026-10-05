from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Asset, InventoryItem, Assignment, RepairTicket, AIConversation, AIMessage
from .serializers import AssetSerializer,InventoryItemSerializer,AssignmentSerializer,RepairTicketSerializer, AIConversationSerializer
from .permissions import IsAdminOrReadOnly
from django.contrib.auth.models import User
from .gemini_service import generate_ai_response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        "username": request.user.username,
        "is_staff": request.user.is_staff,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_list(request):
    users = User.objects.filter(is_active=True)

    return Response([
        {
            "id": user.id,
            "username": user.username,
        }
        for user in users
    ])

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ["type", "status"]
    search_fields = ["name", "serial_number"]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdminOrReadOnly]

class RepairTicketViewSet(viewsets.ModelViewSet):
    queryset = RepairTicket.objects.all()
    serializer_class = RepairTicketSerializer
    permission_classes = [IsAdminOrReadOnly]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_analytics(request):
    total_assets = Asset.objects.count()
    assigned_assets = Asset.objects.filter(status="Assigned").count()
    available_assets = Asset.objects.filter(status="Available").count()
    repair_assets = Asset.objects.filter(status="Repair").count()

    return Response({
        "totalAssets":total_assets,
        "assignedAssets":assigned_assets,
        "availableAssets":available_assets,
        "repairAssets":repair_assets,
        "assetStatus":[
            {
                "name":"Assigned",
                "value":assigned_assets,
            },
            {
                "name":"Available",
                "value":available_assets,
            },
            {
                "name":"Repair",
                "value":repair_assets
            },
        ],
    })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    prompt = request.data.get("prompt")
    conversation_id = request.data.get("conversation_id")

    if not prompt:
        return Response(
            {"detail": "Prompt is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if conversation_id:
        try:
            conversation = AIConversation.objects.get(
                id=conversation_id,
                user=request.user,
            )
        except AIConversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        conversation = AIConversation.objects.create(
            user=request.user,
            title=prompt[:200],
        )

    AIMessage.objects.create(
        conversation=conversation,
        role="user",
        content=prompt,
    )

    try:
        ai_response = generate_ai_response(prompt)

    except Exception:
        return Response(
            {"detail": "Unable to generate AI response."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    AIMessage.objects.create(
        conversation=conversation,
        role="assistant",
        content=ai_response,
    )

    return Response({
        "conversation_id": conversation.id,
        "response": ai_response,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ai_conversations(request):
    conversations = AIConversation.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    serializer = AIConversationSerializer(
        conversations,
        many=True
    )

    return Response(serializer.data)
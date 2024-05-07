from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from subscriptions.models import Package, Subscription
from subscriptions.serializer import PackageSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class PackageView(APIView):
    def get(self, request: Request):
        packages = Package.objects.filter(is_enable=True)
        serializer_class = PackageSerializer(packages, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        subscriptions = Subscription.objects.filter(user=request.user, expire_time=timezone.now())
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


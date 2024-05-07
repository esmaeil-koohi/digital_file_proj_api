import uuid
from datetime import timedelta
import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from subscriptions.models import Package, Subscription
from rest_framework.views import APIView
from .models import Gateway, Payment
from .serializer import GatewaySerializer


class GatewayView(APIView):

    def get(self):
        gateway = Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(gateway, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        gateway_id = request.query_params.get('gateway')
        package_id = request.query_params.get('package')

        try:
            package = Package.objects.get(pk=package_id, is_enable=True)
            gateway = Gateway.objects.get(pk=gateway_id, is_enable=True)
        except (Package.DoesNotExist, Gateway.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            user=request.user,
            package=package,
            gateway=gateway,
            price=package.price,
            phone_number=request.user.phone_number,
            total=str(uuid.uuid4())
        )
        return Response({'token': payment.token}, 'bank-token')

    def post(self, request: Request):
        token = request.data.get('token')
        sts = request.data.get('status')

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if sts != 10:
            payment.status = Payment.STATUS_CANCELED
            payment.save()
            return Response({'detail': 'Payment canceled by user.'}, status=status.HTTP_400_BAD_REQUEST)

        res = requests.post('bank_verify_url', data={})
        if res.status_code // 100 != 2:
            payment.status = Payment.STATUS_ERROR
            payment.save()
            return Response({'detail': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = Payment.STATUS_PAID
        payment.save()

        Subscription.objects.create(
            user=payment.user,
            package=payment.package,
            expire_time=timezone.now() + timedelta(days=payment.package.duration.days)
        )
        return Response({'detail': 'Payment is Successful'}, status=status.HTTP_200_OK)

import yfinance as yf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Asset
from ..serializers import AssetSerializer
import logging

logger = logging.getLogger(__name__)

class AssetPriceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

class AssetPriceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        assets = Asset.objects.all()
        updated_assets = []
        errors = []

        for asset in assets:
            try:
                ticker = yf.Ticker(asset.ticker)
                price_data = ticker.history(period='1d')
                if not price_data.empty:
                    current_price = price_data['Close'].iloc[-1]
                    asset.current_price = round(current_price, 2)
                    asset.save()
                    updated_assets.append(asset)
                else:
                    errors.append(f"No price data for {asset.ticker}")
                    logger.error(f"No price data for {asset.ticker}")
            except Exception as e:
                errors.append(f"Error updating {asset.ticker}: {str(e)}")
                logger.error(f"Error updating {asset.ticker}: {str(e)}")

        serializer = AssetSerializer(updated_assets, many=True)
        response_data = {
            'updated': serializer.data,
            'errors': errors
        }
        status_code = status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS
        return Response(response_data, status=status_code)
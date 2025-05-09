import yfinance as yf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Asset
from ..serializers import AssetSerializer
from bs4 import BeautifulSoup
import requests, time, os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
BRAPI_BASE_URL = "https://brapi.dev/api"
SLEEP_TIME = 1.0
MAX_RETRIES = 3
RETRY_WAIT = 10.0

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

        if not assets:
            return Response(
                {'updated': [], 'errors': ['Nenhum ativo encontrado']},
                status=status.HTTP_400_BAD_REQUEST
            )

        for asset in assets:
            ticker = asset.ticker
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    url = f"{BRAPI_BASE_URL}/quote/{ticker}?token={BRAPI_TOKEN}"
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()

                    result = data.get('results', [data])[0] if data.get('results') else data

                    current_price = result.get('regularMarketPrice')
                    price_earnings = result.get('priceEarnings')
                    price_to_book = result.get('priceToBook')
                    dividend_yield = result.get('dividendsYield')

                    if current_price is None:
                        errors.append(f"Preço não disponível para {ticker}")
                        logger.error(f"Preço não disponível para {ticker}")
                        break

                    try:
                        asset.current_price = round(float(current_price), 2)
                        if price_earnings is not None:
                            asset.price_earnings = round(float(price_earnings), 2)
                        if price_to_book is not None:
                            asset.price_to_book = round(float(price_to_book), 2)
                        if dividend_yield is not None:
                            asset.dividend_yield = round(float(dividend_yield), 2)
                        asset.save()
                        updated_assets.append(asset)
                    except ValueError as e:
                        errors.append(f"Erro ao converter dados para {ticker}: {str(e)}")
                        logger.error(f"Erro ao converter dados para {ticker}: {str(e)}")
                    except Exception as e:
                        errors.append(f"Erro ao atualizar {ticker}: {str(e)}")
                        logger.error(f"Erro ao atualizar {ticker}: {str(e)}")

                    time.sleep(SLEEP_TIME)
                    break  

                except requests.exceptions.HTTPError as e:
                    if response.status_code == 429:  
                        retry_count += 1
                        if retry_count == MAX_RETRIES:
                            errors.append(f"Limite de requisições atingido para {ticker}")
                            logger.error(f"Limite de requisições atingido para {ticker}")
                            break
                        wait_time = RETRY_WAIT * (2 ** (retry_count - 1))
                        logger.warning(f"Too Many Requests para {ticker}. Tentativa {retry_count}/{MAX_RETRIES}. Esperando {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        errors.append(f"Erro ao obter dados para {ticker}: {str(e)}")
                        logger.error(f"Erro ao obter dados para {ticker}: {str(e)}")
                        break
                except Exception as e:
                    errors.append(f"Erro ao processar {ticker}: {str(e)}")
                    logger.error(f"Erro ao processar {ticker}: {str(e)}")
                    break

        serializer = AssetSerializer(updated_assets, many=True)
        response_data = {
            'updated': serializer.data,
            'errors': errors
        }
        status_code = status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS
        return Response(response_data, status=status_code)

class AssetTickerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        errors = []
        updated_assets = []

        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                url = f"{BRAPI_BASE_URL}/available?token={BRAPI_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                tickers = data.get('stocks', [])
                if not tickers:
                    raise Exception("Nenhum ticker encontrado na resposta da API")

                break  
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count == MAX_RETRIES:
                        errors.append("Limite de requisições atingido ao obter lista de tickers")
                        logger.error("Limite de requisições atingido ao obter lista de tickers")
                        break
                    wait_time = RETRY_WAIT * (2 ** (retry_count - 1))
                    logger.warning(f"Too Many Requests. Tentativa {retry_count}/{MAX_RETRIES}. Esperando {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    errors.append(f"Erro ao obter lista de tickers: {str(e)}")
                    logger.error(f"Erro ao obter lista de tickers: {str(e)}")
                    break
            except Exception as e:
                errors.append(f"Erro ao obter lista de tickers: {str(e)}")
                logger.error(f"Erro ao obter lista de tickers: {str(e)}")
                break

        if not tickers:
            return Response(
                {'updated': [], 'errors': errors},
                status=status.HTTP_207_MULTI_STATUS
            )

        for ticker in tickers:
            ticker_yf = f"{ticker}.SA" if not ticker.endswith('.SA') else ticker
            retry_count_inner = 0

            while retry_count_inner < MAX_RETRIES:
                try:
                    url_quote = f"{BRAPI_BASE_URL}/quote/{ticker_yf}?fundamental=true&token={BRAPI_TOKEN}"
                    response_quote = requests.get(url_quote)
                    response_quote.raise_for_status()
                    quote_data = response_quote.json()

                    result = quote_data.get('results', [{}])[0]
                    if not result:
                        errors.append(f"Nenhum dado retornado para {ticker_yf}")
                        logger.error(f"Nenhum dado retornado para {ticker_yf}")
                        break

                    asset_name = result.get('longName', result.get('shortName', ticker_yf))
                    current_price = result.get('regularMarketPrice', 0.0)
                    pl = result.get('priceToEarnings')
                    pvp = result.get('priceToBook')
                    dividend_yield = result.get('dividendYield')

                    asset_type = 'FII' if ticker_yf.endswith('11.SA') else 'Ação'

                    asset, created = Asset.objects.get_or_create(
                        ticker=ticker_yf,
                        defaults={
                            'name': asset_name,
                            'type': asset_type,
                            'current_price': round(float(current_price), 2) if current_price else 0.0,
                            'pl': float(pl) if pl is not None else None,
                            'pvp': float(pvp) if pvp is not None else None,
                            'dividend_yield': float(dividend_yield) if dividend_yield is not None else None,
                        }
                    )

                    if not created:
                        asset.name = asset_name
                        asset.type = asset_type
                        asset.current_price = round(float(current_price), 2) if current_price else asset.current_price
                        asset.pl = float(pl) if pl is not None else asset.pl
                        asset.pvp = float(pvp) if pvp is not None else asset.pvp
                        asset.dividend_yield = float(dividend_yield) if dividend_yield is not None else asset.dividend_yield
                        asset.save()

                    updated_assets.append(asset)
                    time.sleep(SLEEP_TIME)
                    break  

                except requests.exceptions.HTTPError as e:
                    if response_quote.status_code == 429:
                        retry_count_inner += 1
                        if retry_count_inner == MAX_RETRIES:
                            errors.append(f"Limite de requisições atingido para {ticker_yf}")
                            logger.error(f"Limite de requisições atingido para {ticker_yf}")
                            break
                        wait_time = RETRY_WAIT * (2 ** (retry_count_inner - 1))
                        logger.warning(f"Too Many Requests para {ticker_yf}. Tentativa {retry_count_inner}/{MAX_RETRIES}. Esperando {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        errors.append(f"Erro ao processar {ticker_yf}: {str(e)}")
                        logger.error(f"Erro ao processar {ticker_yf}: {str(e)}")
                        break
                except Exception as e:
                    errors.append(f"Erro ao processar {ticker_yf}: {str(e)}")
                    logger.error(f"Erro ao processar {ticker_yf}: {str(e)}")
                    break

        serializer = AssetSerializer(updated_assets, many=True)
        response_data = {
            'updated': serializer.data,
            'errors': errors
        }
        status_code = status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS
        return Response(response_data, status=status_code)
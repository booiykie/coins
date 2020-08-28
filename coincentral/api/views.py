"""Views serving GET requuests."""
import time
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from pycoingecko import CoinGeckoAPI


date_format = "%Y/%m/%d"
market_data_offset = 1


class OncePerDayUserThrottle(UserRateThrottle):
    """Throttling class definition."""
    rate = '5/day'


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@throttle_classes([OncePerDayUserThrottle])
def coin_list(request):
    """
    List all coins.
    """
    cg = CoinGeckoAPI()

    if request.method == 'GET':
        coins = cg.get_coins_list()
        return Response(data=coins, status=status.HTTP_200_OK)

    else:
        res = {"code": 405, "message": f"{request.method} method not allowed."}
        return Response(data=json.dumps(res), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@throttle_classes([OncePerDayUserThrottle])
def market_cap(request):
    """
    Retrieve coins market cap. /marketCap?coin_id=ripple&date=2020/08/05&currency=gbp
    """
    cg = CoinGeckoAPI()

    # retrieve query params
    # noqa: needs to be validated.
    # - validate coin_id str foormat, date string format and currency string forma, and avoid `None`
    # - helper module to convert date string to epoch, and parameter reetrieval.
    _coin_id = (request.query_params.dict()).get('coin_id', None)
    _date = datetime.strptime(
        (request.query_params.dict()).get('date', None), 
        date_format
    )
    _currency = (request.query_params.dict()).get('currency', None)


    if request.method == 'GET':
        coin_market_data = cg.get_coin_market_chart_range_by_id(
            id=_coin_id, vs_currency=_currency, from_timestamp=time.mktime(_date.timetuple()), 
            to_timestamp=time.mktime((_date + timedelta(hours=market_data_offset)).timetuple())
        )
        # hard-coded the market cap extraction. If multiple, rather zip currency to multiple vals.
        market_cap = {_currency: coin_market_data.get('market_caps', [[0,0]])[0][1]}
        return Response(data=market_cap, status=status.HTTP_200_OK)

    else:
        res = {"code": 405, "message": f"{request.method} method not allowed."}
        return Response(data=json.dumps(res), status=status.HTTP_405_METHOD_NOT_ALLOWED)
"""Views serving GET requuests."""
import time
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


from pycoingecko import CoinGeckoAPI

from .helpers import datetime_conversion, string_date_to_datetime_format, extract_coin_request_params
from .helpers import OncePerDayUserThrottle



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
    # - validate coin_id str format, date string format and currency string forma, and avoid `None`
    # - helper module to convert date string to epoch, and parameter retrieval.
    _coin_id, _date, _currency = extract_coin_request_params(request)


    if request.method == 'GET':
    	# should the offset be + 1 or from the time given counting backwards?
    	# all offsets in hours.
        coin_market_data = cg.get_coin_market_chart_range_by_id(
            id=_coin_id, vs_currency=_currency,
            from_timestamp=datetime_conversion(_date, 'h', 0),
            to_timestamp=datetime_conversion(_date, 'h', 1)
        )
        # hard-coded the market cap extraction. If multiple, rather zip currency to multiple vals.
        market_cap = {_currency: coin_market_data.get('market_caps', [[0,0]])[0][1]}
        return Response(data=market_cap, status=status.HTTP_200_OK)

    else:
        res = {"code": 405, "message": f"{request.method} method not allowed."}
        return Response(data=json.dumps(res), status=status.HTTP_405_METHOD_NOT_ALLOWED)



    

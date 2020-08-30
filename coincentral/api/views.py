"""Views serving GET requuests."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, throttle_classes

from pycoingecko import CoinGeckoAPI

from .helpers import datetime_conversion, string_date_to_datetime_format, \
    extract_coin_request_params
from .helpers import OncePerDayUserThrottle


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@throttle_classes([OncePerDayUserThrottle])
def coin_list(request):
    """List all coins."""
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
    """Retrieve coins market cap."""
    cg = CoinGeckoAPI()
    _coin_id, _date, _currency = extract_coin_request_params(request)

    if request.method == 'GET':
    	# should the offset be + 1 or from the time given counting backwards?
    	# all offsets in hours.
        coin_market_data = cg.get_coin_market_chart_range_by_id(
            id=_coin_id, vs_currency=_currency,
            from_timestamp=datetime_conversion(_date, 'h', 0),
            to_timestamp=datetime_conversion(_date, 'h', 3)
        )
        _market_cap_pointers = [
            point for _t,point in coin_market_data.get('market_caps', [[0,0]])]
        if len(_market_cap_pointers) > 1:
            market_cap = {_currency: _market_cap_pointers}
        elif len(_market_cap_pointers) == 1:
        	market_cap = {_currency: _market_cap_pointers[0]}
        else:
        	raise Exception(f"No market cap possible with iincorrect time offset.")
        return Response(data=market_cap, status=status.HTTP_200_OK)

    else:
        res = {"code": 405, "message": f"{request.method} method not allowed."}
        return Response(data=json.dumps(res), status=status.HTTP_405_METHOD_NOT_ALLOWED)


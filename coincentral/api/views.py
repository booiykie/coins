"""Views serving GET requuests."""
from djangocache import cache_page
from rest_framework import status
from django.core.cache import cache
from django.views.decorators.http import last_modified
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, throttle_classes

from pycoingecko import CoinGeckoAPI

from .helpers import datetime_conversion, string_date_to_datetime_format, \
    extract_coin_request_params, cache_key_generator
from .helpers import OncePerDayUserThrottle


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@throttle_classes([OncePerDayUserThrottle])
def coin_list(request):
    """List all coins."""
    cg = CoinGeckoAPI()
    cache_key = 'coins'

    if request.method == 'GET':
        is_cached = cache.get(cache_key, False)
        if not is_cached:
            coins = cg.get_coins_list()
            cache.set(cache_key, coins, 600)

        return Response(data=cache.get(cache_key), status=status.HTTP_200_OK)
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
        cache_key = cache_key_generator(_coin_id, _date, _currency)
        is_cached = cache.get(cache_key, False)
        if not is_cached:
            coin_market_data = cg.get_coin_market_chart_range_by_id(
                id=_coin_id, vs_currency=_currency,
                from_timestamp=datetime_conversion(_date, 'h', 0),
                to_timestamp=datetime_conversion(_date, 'h', 1)
            ) 
            cache.set(cache_key, coin_market_data, 60)
        latest_coin_market_data = cache.get(cache_key, False)
        
        _market_cap_pointers = [
            point for _t,point in latest_coin_market_data.get('market_caps', [[0,0]])]
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


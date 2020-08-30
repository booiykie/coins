# coins
###Traded coins API.###


##Steps Followed ##
1. Study the https://www.coingecko.com/en/api and different endpoints, focused mostly on the coin listing, and date ranged market data endpoints.
2. Investigate the python wrapperr library, pycoingecko.
3. Setup the project skeleton and dependency in a virtual environment using pyenv.
4. Create function views for the required endpoints accepting only `GET` requests.
5. Instantiate the API wrapper library with every request. Started with the coin list API view.
6. Added a Json render, as insinuated by requirement, and a throttling class and decorator to try out API throttling.
7. Completetd the firrrst iteration by achieving the main requirements, API request and rersponses.
8. Asses the request flow and highlight areas to enhance. to achieve better scaling, cooding pitfalls and rewrites required.


##1. Setting up the Environment##
Either set the environment globally or using virtual environments.
Install dependencies from the `requirements` file with,
`pip install -r requirements.txt`

##2. Running Tests##
`python manage.py test`

##3. Running Server##
`python manage.py runserver 9000`

The server will be listenning onn port `9000`. Meaning target the api uri with `http://127.0.0.1:9009/`.

Endpoints:

a. `http://127.0.0.1:9009/coinList`
b. `http://127.0.0.1:9009/marketCap?coin_id=ripple&date=2020/08/05&currency=gbp`
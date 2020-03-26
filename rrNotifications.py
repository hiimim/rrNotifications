#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8


# Configuration: Radarr
radarrHost = '192.168.1.5'
radarrPort = '7878'
radarrApiKey = 'xxxxx'
# Configuration: Telegram
telegramToken = 'xxxxx'
telegramChatId = 00000


def rrSearchMovie(search, arg):

	'''
	Search for a Movie
	
	:param str search: The movie name or IMDB Id or TMDB Id
	:param str arg: The type of search according to previous
	argument: 'term', 'imdb' or 'tmdb'
	:return: list of movie(s) or movie object
	:rtype: list of dict, if search by term
			dict, if search by Id
	'''

	# If the year is detected in search query
	if arg == 'term' and search[-4:].isdigit() and search[-5:-2] in (' 19',' 20'):
		search_term = search[:-5]
		search_year = int(search[-4:])
	else:
		search_term = str(search)

	# API endpoints
	url = 'http://' + radarrHost + ':' + radarrPort + '/api/movie/lookup'
	if arg == 'term': url += '?' + arg + '='
	if arg in ['imdb','tmdb']: url += '/' + arg + '?' + arg + 'Id='
	url += search_term.replace(' ', '%20') + '&apikey=' + radarrApiKey

	# Request & Response
	data = json.loads((urlopen(url)).read())

	# Sort & Filter
	if arg == 'term':
		# Filter if year
		if 'search_year' in locals(): data = [obj for obj in data if obj['year'] == search_year]
		# Sort
		data = sorted(data, key=lambda m: (-m['year'], m['title']))

	return data

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


import os
import json
import telepot
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
# Python 2.7 and 3 compatiblity
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen


def rrSearchMovie(search, arg):

	'''
	Search for a movie
	
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


def excerpt(text, limit=250):

	'''
	Collapse and truncate the given text to fit in the given width limit

	:param str text: The text
	:param int arg: Width limit - Default number of characters is 250
	:return: truncated text
	:rtype: str
	'''

	text = text.replace('  ', ' ')

	# Adapt limit to include additional characters
	limit = limit - 6

	if len(text) > limit:
		# Cut
		text_excerpt = text[:limit]
		# If the cut occured in the middle of a word a number
		if text[limit-1].isalnum() and text[limit].isalnum():
			# Find latest punctuation and cut
			text_excerpt = text_excerpt[:max(text_excerpt.rfind(' '), \
				text_excerpt.rfind(','), text_excerpt.rfind(';'), \
				text_excerpt.rfind('.'), text_excerpt.rfind(':'), \
				text_excerpt.rfind('!'), text_excerpt.rfind('?'))]
		# Add space if excerpt does not end with space
		if text[limit-1] != ' ':
			text_excerpt += ' '
		# Add symbol
		text_excerpt += '[...]'

	else:
		text_excerpt = text

	return text_excerpt


def rrNotify():

	'''
	Send notifications on Telegram
	'''

	# Initialize Telegram bot
	bot = telepot.Bot(telegramToken)

	# Get environmental variables
	radarr_isupgrade = 'False'
	if 'radarr_eventtype' in os.environ:
		radarr_eventtype = os.environ.get('radarr_eventtype')
		if radarr_eventtype == 'Download':
			radarr_isupgrade = os.environ.get('radarr_isupgrade')
		radarr_movie_title = os.environ.get('radarr_movie_title')
		radarr_movie_imdbid = os.environ.get('radarr_movie_imdbid')

	# Send notification
	if (radarr_eventtype == 'Download') and (radarr_isupgrade == 'False'):
		movie = rrSearchMovie(radarr_movie_imdbid, 'imdb')
		movie = rrSearchMovie(movie['tmdbId'], 'tmdb')
		msg = '<b>' + movie['title'] + '</b> (' + str(movie['year']) + ') downloaded!\n' + excerpt(movie['overview'])
		
		# Get YouTube trailer
		if 'youTubeTrailerId' in movie:
			movieTrailerURL = 'https://www.youtube.com/watch?v=' + movie['youTubeTrailerId']
		else:
			movieTrailerURL = 'https://www.youtube.com/results?search_query=trailer+' + movie['title'].replace(" ", "+") + '+' + str(movie['year'])

		# Get IMDb page
		if 'imdbId' in movie:
			movieImdbURL = 'https://www.imdb.com/title/' + movie['imdbId']
		else:
			movieImdbURL = 'https://www.imdb.com/find?q=' + movie['title'].replace(" ", "+") + '+' + str(movie['year'])

		# # Get TMDb page
		# if 'tmdbId' in movie:
		# 	movieImdbURL = 'https://www.themoviedb.org/movie/' + movie['tmdbId']
		# else:
		# 	movieImdbURL = 'https://www.themoviedb.org/search?query=' + movie['title'].replace(" ", "+") + '+' + str(movie['year'])

		# Inline Keyboard Buttons
		kTrailerButton  = InlineKeyboardButton(text='Trailer', url=movieTrailerURL)
		kTrailerButton = [kTrailerButton]
		keyboard = kTrailerButton
		kImdbButton  = InlineKeyboardButton(text='IMDB', url=movieImdbURL)
		keyboard.append(kImdbButton)
		keyboard = [keyboard]
		reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
		
		bot.sendPhoto(chat_id=telegramChatId, photo=movie['images'][0]['url'], caption=msg, parse_mode='html', reply_markup=reply_markup)
		

rrNotify()


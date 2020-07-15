import requests
from hardCodedInfo import threads, users
from ScraperService import scrapeThread

testRequest = {
	'secretrealm': ['secret'],
	'MarbleSplotch': ['Hay'],
}

testLinks = ['https://www.deviantart.com/comments/1/840703897/4840503638']

scrapeThread(testLinks, testRequest)
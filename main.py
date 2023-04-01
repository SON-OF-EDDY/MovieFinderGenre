import telebot
import requests

class MovieSearch:
  def __init__(self):
      self.genre = None
      self.number = None

movie_search = MovieSearch()

available_genres = [

'action',
'comedy',
'family',
'history',
'mystery',
'sci_fi',
'war',
'adventure',
'crime',
'fantasy',
'horror',
'news',
'sport',
'western',
'animation',
'documentary',
'film_noir',
'music',
'reality_tv',
'talk_show',
'biography',
'drama',
'game_show',
'musical',
'romance',
'thriller'
  ]
        
########################################################################

# IMDB STUFF
def find_movie(genre='action',quantity='2'):

  quantity = int(quantity)
  
  IMDB_API_KEY = "k_0h9i1te4"
  
  url = f"https://imdb-api.com/en/API/AdvancedSearch/{IMDB_API_KEY}"
  
  params = {
    "genres": genre,
  }
  response = requests.get(url, params=params)
  
  response.raise_for_status()
  
  movies = response.json()["results"][:quantity]
  
  return movies


########################################################################

# TELEGRAM STUFF

API_KEY = '6243417435:AAGl6rwCtzVxXs0rsZKTH8vDPFyNkuG5wTA'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['genres'], content_types=['text'])
def genres(message):
  genres_list = '\n'.join(available_genres)
  bot.send_message(message.chat.id,genres_list)
  
@bot.message_handler(commands=['start','search'], content_types=['text'])
def start(message):
  msg = bot.send_message(
    message.chat.id, """\
Hi there, I am the MovieFinder bot.
Enter a movie genre, such as 'action', or 'horror':
""")
  bot.register_next_step_handler(msg, quantity_handler)
  
def quantity_handler(message):
  
  genre = message.text.lower()
  
  if (genre in available_genres):
    
    movie_search.genre = genre
    msg = bot.send_message(
      message.chat.id, """\
  Enter how many search results would you like (up to 25):
  """)
    bot.register_next_step_handler(msg, movies_with_keyword)
  else:
    bot.send_message(message.chat.id, 'Genre not available! Use the command /genres to see a full list of available genres.')
  
def movies_with_keyword(message):
  
  number = message.text

  if number.isnumeric():

    if int(number) > 25:
      number = '25'

    movie_search.number = number
    
    output = find_movie(movie_search.genre,movie_search.number)
    
    for entry in output:
      formatted = ''
      formatted += f"Title: {entry['title']}\n\nYear: {entry['description']}\n\nRating: {entry['imDbRating']}\n\nCast: {entry['stars']}\n\nPlot: {entry['plot']}\n\nPoster: {entry['image']}"
      #bot.send_photo(message.chat.id, entry['image'])
      bot.send_message(message.chat.id, formatted)

  else:
    bot.send_message(message.chat.id, 'Please enter numbers only!')
  
bot.polling()
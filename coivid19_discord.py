'''
Modules to be installed with CMD
pip install allennlp allennlp-models
pip install discord.py
pip install nltk
pip install google
'''


import discord
import requests 
import bs4
import discord
import nltk
from googlesearch import search

from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.03.19.tar.gz")



from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english', ignore_stopwords=False)

from nltk.stem import WordNetLemmatizer
lemmitizer = WordNetLemmatizer()
def my_question(question):
  #Google search links
  result_links = []

  for res in search(question, tld="co.in", num=3, stop=3):
    result_links.append(res)
  
  #web scraping
  Reference_text = ""
  cond_text=""
  for link in result_links:
    try:
      req = requests.get(link,timeout=5)
    except:
      continue
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    for i in soup.find_all('p'):
      try:
        Reference_text += i.text
      except:
        continue
  Reference_text = Reference_text.replace('\n',' ').strip().split('.')
  s = question.split()
  s = [stemmer.stem(word) for word in s]
  s = [lemmitizer.lemmatize(word,pos='a') for word in s]
  res=[]
  max_match = 0
  max_index = 0
  for i,v in enumerate(Reference_text):
      t = len(set(s)&set(v))
      if t>max_match:
          max_match = t
          max_index = i
  for i,v in enumerate(Reference_text):
    t = len(set(s)&set(v))
    if max_match==t:
      res.append(Reference_text[i])
    cond_text= '.'.join(res)
  result = predictor.predict(
    passage = cond_text,
    question = question
    )
  return(result['best_span_str'])

client = discord.Client()

@client.event
async def on_ready():
  print('Bot is ready')

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  if message.content.startswith('$q'):
    response = my_question(message.content[3:])
    await message.channel.send(response)

client.run("OTM2OTc5OTU2OTQ3MzUzNjEw.YfVElQ.jjSMRFJPBYTH_de-FY_XukffjuY")
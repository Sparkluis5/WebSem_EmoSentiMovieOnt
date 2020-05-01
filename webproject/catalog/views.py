from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import tmdbsimple as tmdb
from stanfordcorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import ConjunctiveGraph, Namespace

local_corenlp_path = 'C:/Users/Luis/PycharmProjects/stanford-corenlp-full-2018-10-05'

#Lexicon and stopword definition
stops = set(stopwords.words("english"))
anew = 'C:/Users/Luis/PycharmProjects/WS/nrc_lex.csv'
lmtzr = WordNetLemmatizer()
nlp = StanfordCoreNLP(local_corenlp_path)

#render homepage
def index(request):
    template = loader.get_template('C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/homepage.html')
    return HttpResponse(template.render())

#search positive sentiment movies in our populated graph
def getPositive(request):
    searchlist = []
    sentisearc = ['Positive']
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        searchlist.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': searchlist})

#search neutral sentiment movies in our populated graph
def getNeutral(request):
    searchlist = []
    sentisearc = ['Neutral']
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        searchlist.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': searchlist})

#search negative sentiment movies in our populated graph
def getNegative(request):
    searchlist = []
    sentisearc = ['Negative']
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        searchlist.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': searchlist})

#search by anger emotion movies in our populated graph
def getAnger(request):
    searchlist = ['Anger']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html' , {'Movies': sentisearc})

#search by fear emotion movies in our populated graph
def getFear(request):
    searchlist = ['Fear']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by antecipation emotion movies in our populated graph
def getAnticipation(request):
    searchlist = ['Anticipation']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by surprise emotion movies in our populated graph
def getSurprise(request):
    searchlist = ['Surprise']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by joy emotion movies in our populated graph
def getJoy(request):
    searchlist = ['Joy']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by joy emotion movies in our populated graph
def getSadness(request):
    searchlist = ['Sadness']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by trust emotion movies in our populated graph
def getTrust(request):
    searchlist = ['Trust']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#search by disgust emotion movies in our populated graph
def getDisgust(request):
    searchlist = ['Anger']
    sentisearc = []
    retMovies = []
    retMovies = queryStore(searchlist, sentisearc)
    for ret in retMovies:
        sentisearc.append(str(ret))
    return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                  {'Movies': sentisearc})

#render about page
def getAbout(request):
    template = loader.get_template('C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showAbout.html')
    return HttpResponse(template.render())

#search box action, uses function defined in DataProcessing.py
def searchAction(request):
    if 'q' in request.GET:
        sentisearc = []
        emot, senti = semanticSearch(str(request.GET['q']))
        retMovies = queryStore(emot, senti)
        for ret in retMovies:
            sentisearc.append(str(ret))
        return render(request, 'C:/Users/Luis/PycharmProjects/WS/webproject/catalog/templates/showResults.html',
                      {'Movies': sentisearc})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

#--------------------------------------------------------------------
#repeated function, necessary
def movieInformation(movie_title):

    search = tmdb.Search()
    response = search.movie(query=movie_title)
    id = 0
    rate = 0
    language = ''
    adult = False
    rel_date = ''
    tot_genres = []
    budget = 0

    for s in search.results:
        if s['title'].lower() == movie_title.lower():
            print(s['title'], s['id'], s['release_date'], s['popularity'])
            print(s)
            id = s['id']
            rate = s['vote_average']
            language = s['original_language']
            adult = s['adult']
            rel_date = s['release_date']
            gen = s['genre_ids']
            movie = tmdb.Movies(id)
            #budget = movie.budget
            print(movie.info())
            for id in gen:
                genre = tmdb.Genres()
                l = genre.movie_list()
                for i in range(0, len(l['genres'])):
                    if id == int(l['genres'][i]['id']):
                        tot_genres.append(l['genres'][i]['name'])

    print(tot_genres)


def dbpediaQuery(SearchTerm):

    inicialquery = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        SELECT DISTINCT ?film WHERE {
                            ?film rdf:type <http://dbpedia.org/ontology/Film>.
                            ?film rdfs:label ?film_name.
                            FILTER (LANG(?film_name)=\"en\" && ?film_name"""

    middlequery = "=\"" + SearchTerm + "\"@en)}"
    finalquery = inicialquery + middlequery

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(finalquery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(results)
    if len(results['head']['link']) == 0:
        retval = 'None'

    for result in results["results"]["bindings"]:
        retval = result['film']['value']

    return retval

def queryStore(emotionSearch,sentimentSearch):

    retVal = []

    graph = ConjunctiveGraph('Sleepycat')
    graph.open("C:/Users/Luis/PycharmProjects/WS/MyStore", create=False)
    print('Triples stored in graph: ', len(graph))

    onyxname = Namespace('http://www.gsi.dit.upm.es/ontologies/onyx/ns#')
    marlname = Namespace('http://purl.org/marl/ns#')


    if len(emotionSearch) == 0 and len(sentimentSearch) == 0:
        return retVal
    else:
        for emo in emotionSearch:
            for s, p, o in graph:
                if p == onyxname.hasEmotion:
                    if emo in o:
                        retVal.append(s)
        for senti in sentimentSearch:
            urlcmp = ''
            if senti == 'Positive':
                urlcmp = marlname.Positive
            if senti == 'Neutral':
                urlcmp = marlname.Neutral
            if senti == 'Negative':
                urlcmp = marlname.Negative
            for s, p, o in graph:
                if p == marlname.hasSentimentm:
                    if str(urlcmp) in str(o):
                        retVal.append(s)

        return retVal

    graph.close()

def semanticSearch(inputText):

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sentiSearch = ['Positive', 'Neutral', 'Negative']
    emoSearch = ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']

    sentiRet = []
    emoRet = []

    tokens = inputText.lower()
    tokens = tokens.split(' ')

    #busca por similaridade, vai aos sinonimos de cada token e procura pela semelhança por alguma emoção
    for token in tokens:
        print(token)
        maxVal = 0
        for syn in wordnet.synsets(token):
            print(syn)
            for emo in emoSearch:
                cmpe = wordnet.synsets(emo)
                aux = cmpe[0].name()
                aux2 = syn.name()
                #print(aux)
                #print(aux2)
                cmpemo = wordnet.synset(str(aux))
                cmpemo2 = wordnet.synset(str(aux2))
                #print(cmpemo)
                b = cmpemo2.name().split('.')
                print(b[0])
                a = cmpemo.wup_similarity(cmpemo2)

                #Em caso de nao ser nada semelhante
                if a is None:
                    continue
                else:
                    #Atualização em procura da emoção com mais semelhança
                    if a > maxVal:
                        print(a)
                        print(emo)
                        maxVal = a
                        if emo in emoRet:
                            continue
                        else:
                            emoRet.append(emo)
            for senti in sentiSearch:
                cmpe = wordnet.synsets(senti)
                aux = cmpe[0].name()
                aux2 = syn.name()
                #print(aux)
                #print(aux2)
                cmpemo = wordnet.synset(str(aux))
                cmpemo2 = wordnet.synset(str(aux2))
                #print(cmpemo)
                b = cmpemo2.name().split('.')
                print(b[0])
                a = cmpemo.wup_similarity(cmpemo2)

                #Em caso de nao ser nada semelhante
                if a is None:
                    continue
                else:
                    #Atualização em procura da emoção com mais semelhança
                    if a > maxVal:
                        print(a)
                        print(senti)
                        maxVal = a
                        if senti in sentiRet:
                            continue
                        else:
                            sentiRet.append(emo)
    print(emoRet)
    print(sentiRet)
    return emoRet, sentiRet
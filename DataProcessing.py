import tmdbsimple as tmdb
import csv
import nltk
from stanfordcorenlp import StanfordCoreNLP
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from SPARQLWrapper import SPARQLWrapper, XML, JSON
import rdflib
from tempfile import mktemp
from rdflib import ConjunctiveGraph, Namespace, Literal
from rdflib.store import NO_STORE, VALID_STORE

#Path do stanford CoreNLP é preciso fazer o Download deste primeiro
local_corenlp_path = 'C:/Users/Luis/PycharmProjects/stanford-corenlp-full-2018-10-05'

tmdb.API_KEY = '9c18977580127eecdc81970dc3f3ce1f'

#Path do léxico e definição das stopwords
stops = set(stopwords.words("english"))
anew = 'C:/Users/Luis/PycharmProjects/WS/nrc_lex.csv'
lmtzr = WordNetLemmatizer()
nlp = StanfordCoreNLP(local_corenlp_path)

# Aceita a sinopse como String e devolve sentimento e emoção associada com recurso ao léxico NRC
def analyzefile(fulltext):
    print(fulltext)

    #tokenização das palavras
    sentences = tokenize.sent_tokenize(fulltext)

    #Análise frase a frase
    for s in sentences:

        print("S:" + s)

        #Variaveis auxiliares
        all_words = []
        found_words = []
        pos_list = []
        neg_list = []
        neut_list = []
        emo_list = [0]*8
        total_pos = 0
        total_neut = 0
        total_neg = 0

        full_emotion = ''

        #Passar para letra pequena
        words = nlp.pos_tag(s.lower())

        #print(words)

        for index, p in enumerate(words):
            #Ignorar pontuação
            #print(index)
            #print(p)
            w = p[0]
            pos = p[1]
            if w in stops or not w.isalpha():
                continue

            #Procurar pela negação da palavra
            j = index-1
            neg = False
            while j >= 0 and j >= index-3:
                if words[j][0] == 'not' or words[j][0] == 'no' or words[j][0] == 'n\'t':
                    neg = True
                    break
                j -= 1

            #lemmatização e PoS tagging
            if pos[0] == 'N' or pos[0] == 'V':
                lemma = lmtzr.lemmatize(w, pos=pos[0].lower())
            else:
                lemma = w

            all_words.append(lemma)

            # Procura no Léxico NRC, existente no ficheiro nrc_lex.csv
            with open(anew) as csvfile:
                reader = csv.DictReader(csvfile, delimiter = ';')
                for row in reader:
                    if row['Word'].casefold() == lemma.casefold():
                        #print(row['Word'].casefold())
                        if neg:
                            #print("Negation Found")
                            if row['Positive'] == str(1):
                                neg_list.append(lemma)
                            else:
                                pos_list.append(lemma)
                            found_words.append("neg-"+lemma)
                        else:
                            if row['Positive'] == str(0) and row['Negative'] == str(0):
                                #print("Neutral Found")
                                neut_list.append(lemma)
                            if row['Positive'] == str(1):
                                #print("Positive Found")
                                pos_list.append(lemma)
                            if row['Negative'] == str(1):
                                #print("Negative Found")
                                neg_list.append(lemma)
                            found_words.append(lemma)

                        if row['Positive'] == str(0) and row['Negative'] == str(0):
                            continue
                        if row['Anger'] == str(1):
                            emo_list[0] = emo_list[0] + 1
                        if row['Anticipation'] == str(1):
                            emo_list[1] = emo_list[1] + 1
                        if row['Disgust'] == str(1):
                            emo_list[2] = emo_list[2] + 1
                        if row['Fear'] == str(1):
                            emo_list[3] = emo_list[3] + 1
                        if row['Joy'] == str(1):
                            emo_list[4] = emo_list[4] + 1
                        if row['Sadness'] == str(1):
                            emo_list[5] = emo_list[5] + 1
                        if row['Surprise'] == str(1):
                            emo_list[6] = emo_list[6] + 1
                        if row['Trust'] == str(1):
                            emo_list[7] = emo_list[7] + 1

        if len(found_words) == 0:  # no words found in ANEW for this sentence
            print("No occurence")
            noemo = 'Neutral'
            nosent = 'Neutral'
            return nosent, noemo
        else:  # output sentiment info for this sentence
            pos = len(pos_list)
            neut = len(neut_list)
            neg = len(neg_list)

            print(len(pos_list))
            print(len(neg_list))



            if (pos > neg) and (pos > neut):
                total_pos = total_pos + 1
            elif (neut > pos) and (neut > neg):
                total_neut = total_neut + 1
            else:
                total_neg = total_neg + 1

            #procurar pela emocao
            em = emo_list.index(max(emo_list))
            emotion = ''
            sentiment = ''
            if em == 0:
                emotion = 'Anger'
            if em == 1:
                emotion = 'Anticipation'
            if em == 2:
                emotion = 'Disgust'
            if em == 3:
                emotion = 'Fear'
            if em == 4:
                emotion = 'Joy'
            if em == 5:
                emotion = 'Sadness'
            if em == 6:
                emotion = 'Surprise'
            if em == 7:
                emotion = 'Trust'
            if emotion == '':
                emotion = 'Neutral'

        full_emotion = full_emotion + emotion + ','

    if (total_pos > total_neg) and (total_pos > total_neut):
        sentiment = 'Positive'
    elif (total_neut > total_pos) and (total_neut > neg):
        sentiment = 'Neutral'
    else:
        sentiment = 'Negative'

    print('Sentiment:' + sentiment)
    print('Emotions:' + full_emotion)

    return sentiment, full_emotion

def readFile():
    filepath = 'C:/Users/Luis/PycharmProjects/WS/newData.csv'

    with open(filepath, 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(str(row[2]))
            sentRet, emoRet = analyzefile(str(row[2]))

            with open('data_emotion.csv', 'a', encoding='utf8') as outf:
                writer = csv.writer(outf)
                writer.writerow([row[1], row[2], sentRet, emoRet])

#--------------------------------------------------------------------

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

def createStore():
    graph = ConjunctiveGraph('Sleepycat')

    rt = graph.open("C:/Users/Luis/PycharmProjects/WS/MyStore", create=False)

    if rt == NO_STORE:
        graph.open("C:/Users/Luis/PycharmProjects/WS/MyStore", create=True)
    else:
        assert rt == VALID_STORE, 'The underlying store is corrupt'

    graph.close()

def populateStore():

    onyx = rdflib.Graph()
    marl = rdflib.Graph()

    onyx.load('http://www.gsi.dit.upm.es/ontologies/onyx/ns')
    marl.load('http://marl.gi2mo.org/0.2/ns.owl')

    for s, p, o in onyx:
        print(s)

    # for s, p, o in marl:
    # print(s, p, o)

    graph = ConjunctiveGraph('Sleepycat')
    graph.open("C:/Users/Luis/PycharmProjects/WS/MyStore", create=False)
    #rdflib = Namespace('http://rdflib.net/test/')
    #graph.bind('test', 'http://rdflib.net/test/')
    #graph.add((rdflib['pic:1'], rdflib.name, Literal('Jane & Bob')))
    #graph.add((rdflib['pic:2'], rdflib.name, Literal('Squirrel in Tree')))
    print('Triples still in graph: ', len(graph))
    graph.close()

def semanticSearch(inputText):

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    posSearch = ['Positive']
    neuSearch = ['Neutral']
    negSearch = ['Negative']

    emoSearch = ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']

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

    print(emoRet)

text = "Havana, Cuba, 1979. Flamboyantly gay artist Diego (Jorge Perugorría) attempts to seduce the straight and strait-laced David, an idealistic young communist, and fails dismally. But David conspires to become friends with Diego so he can monitor the artist's subversive life for the state. As Diego and David discuss politics, individuality and personal expression in Castro's Cuba, a genuine friendship develops between the two. But can it last? Strawberry and Chocolate became an instant hit when it was released, and has become a classic of Cuban cinema due to its charming and authentic exploration of a connection between two people under historical circumstances that seem levelled against them."

#analyzefile(text)
#movieInformation('Toy Story')
#semanticSearch("Show me movies that provoke me anger")
readFile()
#loadOntology()
#populateStore()
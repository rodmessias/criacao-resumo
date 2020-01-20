# -*- coding: utf-8 -*-
import spacy

from spacy.lang.pt.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

import sys
import re

stopWords = list(STOP_WORDS)
nlp = spacy.load('pt_core_news_sm')

def sanitizeContent(post):
    text = post.splitlines()
    textSanitized = []
    for row in text:
        textSanitized.append(row)
    clean = re.compile('(<.*?>)|(&#x2122;)|(&nbsp;)|(&#8220;)|(&#8221;)|(&#8216;)|(&#8211;)')
    return re.sub(clean, ' ', ' '.join(textSanitized))

def removeMultiLines(content):
    file = content.splitlines()
    sentences = ''
    for sentence in file:
        sentences += " ".join(sentence.split()).strip()
    return sentences

def textSummarizer(rawDocx, numberSentences):
    rawText = rawDocx
    docx = nlp(rawText)

    wordFrequencies = {}
    for word in docx:
        if word.text not in stopWords:
            if word.text not in wordFrequencies.keys():
                wordFrequencies[word.text] = 1
            else:
                wordFrequencies[word.text] += 1

    maximumFrequncy = max(wordFrequencies.values())

    for word in wordFrequencies.keys():
        wordFrequencies[word] = (wordFrequencies[word] / maximumFrequncy)

    sentenceList = [sentence for sentence in docx.sents]

    sentenceScores = {}
    for sent in sentenceList:
        for word in sent:
            if word.text.lower() in wordFrequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentenceScores.keys():
                        sentenceScores[sent] = wordFrequencies[word.text.lower()]
                    else:
                        sentenceScores[sent] += wordFrequencies[word.text.lower()]

    summarySentences = nlargest(numberSentences, sentenceScores, key = sentenceScores.get)
    finalSentences = [w.text for w in summarySentences]

    summary = ' '.join(finalSentences)

    return summary

textExample = '<div id="biografiaContent"> <p>Raul Seixas (1945-1989) foi um músico, compositor e cantor brasileiro, um dos grandes representantes do rock no Brasil. É conhecido por músicas como “Maluco Beleza” e “Ouro de Tolo”.</p><p>Raul Santos Seixas (1945-1989) nasceu em Salvador, Bahia, no dia 28 de junho de 1945. Desde a adolescência, ficou impressionado com o fenômeno do Rock and Roll, o que levou a criar uma banda chamada "Os Panteras". Lançou o seu primeiro disco em 1968, “Raulzito e seus Panteras”. Mas o sucesso veio mesmo depois do lançamento do disco “Krig-ha, Bandolo!” (1973), cuja música principal, “Ouro de Tolo”, fez grande sucesso no Brasil. O disco tinha outras músicas de grande repercussão, como “Mosca na Sopa” e “Metamorfose Ambulante”.</p><p>Raul Seixas se envolveu com ocultismo, estudou filosofia e psicologia, o que o fez um dos poucos compositores a tentar imprimir suas idéias em letras aliadas ao som vibrante do Rock, juntamente com ritmos nordestinos.</p><p>Em 1974, criou a Sociedade Alternativa, um conceito de sociedade livre inspirada no ocultista Aleister Crowley e que foi tema de uma de suas canções do disco "Gita" (1974).</p><p>Raul Seixas produziu bons trabalhos como "Novo Aeon" (1975), "Metrô Linha 743" (1983), "Uah-Bap-Lu-Bap-Lah-Béin-Bum!" (1987) e "A Panela do Diabo"(1989), este último, em parceria com o roqueiro Marcelo Nova. Raul Seixas foi considerado um dos maiores músicos brasileiros, com grande número de admiradores.</p><p>Raul Seixas enfrentou sérios problemas com o álcool. Faleceu no dia 21 de agosto de 1989, com apenas 44 anos, vítima de pancreatite aguda.</p> </div>'

summary = textSummarizer(removeMultiLines(sanitizeContent(textExample)), 3)

print(summary)

# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
import difflib

app = Flask(__name__)



###### LOAD #########

dictionary=[]
numResults=9


inPath="thai_vocab"
with open(inPath, 'r') as f:
    for line in f:
        fields = line.strip().split("|")
        dictionary.append(fields)
    #print fields[1]



def getBestWords(word):
    global numResults,dictionary
    #ratio=[difflib.SequenceMatcher(None, word, x[2]).ratio() for x in dictionary]
    ratio=[]
    for x in dictionary:
        thai_sim = difflib.SequenceMatcher(None, word, x[2]).ratio()
        eng_sim = difflib.SequenceMatcher(None, word, x[1]).ratio()
        ratio.append(max(thai_sim,eng_sim))
    bestWordsSorted = sorted(range(len(ratio)), key=lambda k: -ratio[k])
    bestIdx=bestWordsSorted[:numResults]
    return bestIdx


bestIdx=[]
def candidatesList(word):
    global bestIdx
    candidate_list=[]
    bestIdx=getBestWords(word)
    candidateWords = [dictionary[i] for i in bestIdx]
    refNum=0
    for wordDict in candidateWords:
        refNum=refNum+1
        elemList = str(refNum)+" - "+wordDict[0]+" - "+wordDict[1]+" - "+wordDict[2]
        candidate_list.append(elemList)
    return candidate_list




def selected_opt(num):
    global bestIdx,dictionary
    dict_entry_num=bestIdx[num-1]
    definitive_word = dictionary[dict_entry_num][0]
    return definitive_word





@app.route('/_get_options')
def get_options():
    word = request.args.get('word', 0, type=str)
    option_list=candidatesList(word)
    return jsonify(option_list=option_list)



@app.route('/_select_word')
def select_word():
    num = request.args.get('num', 0, type=int)
    selected_word=selected_opt(num)
    return jsonify(selected_word=selected_word)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

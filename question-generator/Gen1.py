import os
from pprint import pprint
import nltk
from nltk.corpus import words as nltk_words
from nltk.corpus import wordnet as wn
from nltk import sent_tokenize
from textblob import TextBlob as tb
import re


def getQuestions(passage, title):
    def questionMark():
        candidateQuestions = passage.split("?")
        questions = []
        for question in candidateQuestions:
            questionLine = question.split(".")[-1]
            if questionLine != "":
                questionLine += "?"
                question = {
                            "Question": questionLine,
                            "Answer": ""
                            }
                questions.append(question)
        return questions

    def namedEntityQuestions():
        dictionary = dict.fromkeys(nltk_words.words(), None)

        chunked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(passage)))
        entities = {"PERSON": [], "ORGANIZATION": [], "GPE": [],
                    "LOCATION": [], "FACILITY": []}
        for c in chunked:
            if isinstance(c, nltk.tree.Tree):
                content = ""
                for cnt in c.leaves():
                    content += cnt[0]
                    content += " "
                try:
                    dictionary[content.lower().strip()]
                except KeyError:
                    entities[c.label()].append(content)

        entities["PERSON"] = list(set(entities["PERSON"]))
        entities["ORGANIZATION"] = list(set(entities["ORGANIZATION"]))
        entities["GPE"] = list(set(entities["GPE"]))
        entities["LOCATION"] = list(set(entities["LOCATION"]))
        entities["FACILITY"] = list(set(entities["FACILITY"]))

        questions = []
        # who questions
        for person in entities["PERSON"]:
            question = {"Question": "Who is " + person + " ?",
                        "Answer": ""}
            questions.append(question)
        # what questions
        for person in entities["PERSON"]:
            question = {"Question": "What role does " + person + " play ?",
                        "Answer": ""}
            questions.append(question)
        return questions

    def synSetsQuestions():
        def get_similar_words(word):
            synsets = wn.synsets(word, pos='n')
            if len(synsets) == 0:
                return []
            else:
                synset = synsets[0]
            hypernym = synset.hypernyms()[0]
            hyponyms = hypernym.hyponyms()
            sim_w = []
            for hyponym in hyponyms:
                similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
                if similar_word != word:
                    sim_w.append(similar_word)
                if len(sim_w) == 8:
                    break
            return sim_w

        def sentence_eval(sentence):
            if sentence.tags[0][1] == 'RB' or len(sentence.words) < 6:
                return None
            tag_map = {word.lower(): tag for word, tag in sentence.tags}
            replace_nouns = []
            for word, tag in sentence.tags:
                if tag == 'NN' and word not in title:
                    for phrase in sentence.noun_phrases:
                        if phrase[0] == '\'':
                            break
                        if word in phrase:
                            [replace_nouns.append(phrase_word) for phrase_word
                                in phrase.split()[-2:]]
                            break
                    if len(replace_nouns) == 0:
                        replace_nouns.append(word)
                    break
            if len(replace_nouns) == 0:
                return None

            question = {
                'answer': ' '.join(replace_nouns)
            }

            if len(replace_nouns) == 1:
                question['similar_words'] = get_similar_words(replace_nouns[0])
            else:
                question['similar_words'] = []

            replace_phrase = ' '.join(replace_nouns)
            blanks_phrase = ('__________ ' * len(replace_nouns)).strip()

            expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
            sentence = expression.sub(blanks_phrase, str(sentence), count=1)

            question['Question'] = sentence
            return question

        data = tb(passage)
        sentences = data.sentences
        sentences.pop(0)

        questions = []
        for sentence in sentences:
            question = sentence_eval(sentence)
            if question:
                questions.append(question)
        return questions

    questions = []
    questions.extend(questionMark())
    questions.extend(namedEntityQuestions())
    questions.extend(synSetsQuestions())
    return questions


def readText(inputType="default"):
    ip = ""
    title = ""
    if inputType == 'stdin':
        ip = input
        title = "Input"
    elif inputType == 'file':
        filePath = input("Enter File Path :")
        fp = open(filePath, 'r')
        ip = fp.read()
        fileName = filePath.split("/")[-1]
        title = fileName
        fp.close()
    elif inputType == 'default':
        fileName = 'HistoryOfIndia'
        filePath = os.path.join("../passages", fileName)
        print("Opening File : {}".format(filePath))
        fp = open(fileName, 'r')
        ip = fp.read()
        title = fileName
        fp.close()
    ip = ip.strip()
    return ip, title


def askQuestions(passage, questions):
    import random
    print("\n\n------------------------\n")
    print("Read the passage and Answer the questions that follow\n")
    print(passage)
    print("\n\n------------------------\n")
    print("Answer the following\n")
    alternateQuestion(questions)
    qLen = len(questions)
    random.shuffle(questions)
    for i, question in enumerate(questions):
        print("Question {}/{}".format(i, qLen))
        pprint(question, indent=4)
        print


def alternateQuestion(questions):
    for i in range(len(questions)):
        question = questions[i]["Question"]
        part = question.split("_")[-1]
        word = part.split(" ")[3]
        ss = wn.synsets(word)
        if not len(ss):
            continue
        hypernym = ss[0].hypernyms()
        if len(hypernym):
            hypernym = hypernym[0]
        else:
            continue
        newWord = hypernym.lemmas()[0].name()
        pos = part.find(word)
        pos_lbalnk = question.rfind("_")
        pos = pos_lbalnk + pos
        newQuestion = question[:pos]+" "+ newWord +" "+ question[pos+1+len(word):]
        questions[i]["AlternateQuestion"] = newQuestion

def main():
    text, title = readText(inputType="file")
    questions = getQuestions(passage=text, title=title)
    askQuestions(text, questions)
    return 0


if __name__ == "__main__":
    exitStatus = main()

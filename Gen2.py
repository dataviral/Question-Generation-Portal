from nltk.corpus import gutenberg
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import datetime
from random import randrange, uniform
import random

text = ""
for file_id in gutenberg.fileids():
    text += gutenberg.raw(file_id)
trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)
tokenizer = PunktSentenceTokenizer(trainer.get_params())
tokenizer._params.abbrev_types.add('dr')

text=[]
f=open('../passages/passage2','r')
line=f.read(5000)
while(len(line)>1):
	data=tokenizer.tokenize(line)
	for i in data:
		i.rstrip()
		i.replace("\n", " ",1)
		if (i[0].isupper()==True and i[len(i)-1] in ['.','!','?']):
			text.append(i)
	line=f.read(5000)
f.close()

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def preprocess(data):
	sentences_with_pronouns = []
	for sentence in data:
		words = word_tokenize(sentence)
		if (words[0].isupper()==False):
			sentences_with_pronouns.append(sentence)
			continue
		for word in words:
			word_pos = pos_tag([word])
			if word_pos[0][1] == 'PRP':
				sentences_with_pronouns.append(sentence)
				break
			if word in ['this', 'their', 'she', 'he', 'whose']:
				sentences_with_pronouns.append(sentence)
				break
	sentences_without_pronouns = [x for x in data if x not in sentences_with_pronouns]
	return sentences_without_pronouns

def questiontype1(data):#year
	for i in data:
		x=i
		s=[]
		for j in range(len(x)-1):
			if(x[j].isdigit()==True and x[j+1].isdigit()==True and x[j+2].isdigit()==True and x[j+3].isdigit()==True and (x[j]=='1' or x[j]=='2' )):
				a=x[j:j+4]
				b=x.replace(a,"____")
				print("Q)\t"+b+" Which Year did this occur?\n")
				c=int(a)
				l = list(range(1,30))
				h=random.shuffle(l)
				for z in range(4):
					s.append(c+h[0])
				s.append(c)
				random.shuffle(s)
				for i in range(5):
					print(s[i])
				print(a)
				print("\n")

def questiontype2(data):#Proper Nouns
	q=[]
	l=[]
	flag=1
	temp=0
	for x in data:
		tagged_sent = pos_tag(x.split())
		propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
		q.append(propernouns)
		if (len(propernouns)!=0):
			a=x
			t=random.randint(0,len(propernouns)-1)
			j=propernouns[t]
			l.append(j)
			r=a.replace(j,"____")
			print("Q)\t"+r+" What are we talking about here?\n")
			print(a)
			print("\n")
			'''
			while(flag==1):
				if (propernouns[len(propernouns)-1-temp] not in l):
					l.append(propernouns[len(propernouns)-1-temp])
					temp=temp+1
					if (temp==3):
						flag=0
			random.shuffle(l)
			for i in range(4):
				print(l[i])
			'''

def questiontype3(data):#True or False
	for x in data:
		loc=0
		flag=0
		if(" was " in x):
			y=x.replace("was ","wasn't ");
			flag=1
		elif(" is " in x ):
			y=x.replace("is ","isn't ");
			flag=1
		elif(hasNumbers(x)==True):
			flag=3
			y=[]
			for i in range(len(x)-1):
				if(i<=loc):
					loc=loc
				elif(x[i].isdigit()==False):
					y.append(x[i])
					loc=i
				else:
					loc=i
					for j in range(i,len(x)-1):
						if(x[j].isdigit()==True):
							loc=j
						else:
							break
					sum=0
					sum=int(x[i:loc+1])
					a=random.randint(1,30)
					sum=sum+a
					y.append(sum)
			for k in y:
				b=str(a)+str(k)
			print("Q) "+b)
			print("True or False?\n(False)")
		l=list(range(0,2))
		random.shuffle(l)
		s=l[0]
		if(s==0 and flag==1):
			print("Q)\t"+y+"\tTrue or False?\n(False)\n")
		elif(s==1 and flag==1):
			print("Q)\t"+x+"\tTrue or False?\n(True)\n")

def questiontype4(data):#subjective
	for i in data:
		loc=0
		if(i.find("is defined as")==True):
			for x in range(len(i)):
				if (i[x:x+12]=="is defined as"):
					f=x-1
					for g in range(0,f):
						if(i[g]==' '):
							loc=g
			print("Q)\t Define"+i[loc:f]+"." )
			print("Answer:"+i)

text2=preprocess(text)
questiontype1(text2)
questiontype2(text2)
questiontype3(text2)
questiontype4(text2)

import re
import os
import sys
import numpy as np
import string
from nltk import *
from operator import itemgetter
from random import randint

num_of_arguments=4
unigrams=dict()
bigrams=dict()
trigrams=dict()
def totaliser(inp_dict):
	summation=0
	for i in inp_dict:
		summation+=inp_dict[i]
	return summation
def total_types_unigrams():
	count=0
	for w1 in unigrams:
		count+=1
	return count
def total_unigrams():
	count=0
	for w1 in unigrams:
		count+=unigrams[w1]
	return count
def total_types_bigrams():
	count=0
	for w1 in bigrams:
		for w2 in bigrams[w1]:
			count+=1
	return count
def total_bigrams():
	for w1 in bigrams:
		for w2 in bigrams[w1]:
			count+=bigrams[w1][w2]
def total_types_trigrams():
	count=0
	for w1 in trigrams:
		for w2 in trigrams[w1]:
			for w3 in trigrams[w1][w2]:
				count+=1

	return count
def total_trigrams():
	count=0
	for w1 in trigrams:
		for w2 in trigrams[w1]:
			for w3 in trigrams[w1][w2]:
				count+=trigrams[w1][w2][w3]
	return count


def running_conditions():
	if len(sys.argv)<num_of_arguments:
		print("Please enter the correct number of arguments and check the input syntax from readme")
		quit()
	elif int(sys.argv[1])>3 and int(sys.argv[1])<1:
		print("The best we solve is trigram , so please ensure that the second argument is less than 4 and greater than 0")
		quit()
	elif sys.argv[2]!="k":
		if sys.argv[2]!="w":
			print("Please go through the readme once again.Also ensure that the caps lock is turned off")
			quit()
	elif os.path.exists(sys.argv[3])==False:
		print("Please check the path to the input file.Also ensure that you have put the file name in quotation marks")
		quit()
def c_unigram(data):
	for sentence in data:
		raw_words=word_tokenize(sentence)
		words = [word for word in raw_words if word.isalpha()]
		for word in words:
			if word not in unigrams:
				unigrams[word]=1
			else:
				unigrams[word]+=1
def c_bigrams(data):
	for sentence in data:
		raw_words=word_tokenize(sentence)
		words = [word for word in raw_words if word.isalpha()]
		# for word in words:
		# 	if word not in bigram:
		# 		bigram[word]={}
		# 	if (as i have to acess the other element as well cannot use this method)
		for k in range(len(words)-1) :
			if words[k] not in bigrams:
				bigrams[words[k]]={}
			if words[k+1] not in bigrams[words[k]]:
				bigrams[words[k]][words[k+1]]=1
			else:
				bigrams[words[k]][words[k+1]]+=1

def c_trigrams(data):
	for sentence in data:
		raw_words=word_tokenize(sentence)
		words = [word for word in raw_words if word.isalpha()]
		for k in range(len(words)-2):
			if words[k] not in trigrams:
				trigrams[words[k]]={}
			if words[k+1] not in trigrams[words[k]]:
				trigrams[words[k]][words[k+1]]={}
			if words[k+2] not in trigrams[words[k]][words[k+1]]:
				trigrams[words[k]][words[k+1]][words[k+2]]=1
			else:
				trigrams[words[k]][words[k+1]][words[k+2]]+=1
def p_kneser_unigram(inp_sen,corpus):
	inp_tokens=word_tokenize(inp_sen)
	t_probab=1
	d=0.75
	reduction_factor=0.0000001
	temp=0
	for i in inp_tokens:
		flag=0
		for j in unigrams:
			if (i==j):
				temp=((max((unigrams[j]-d),0))/totaliser(unigrams))
				temp+=(d/totaliser(unigrams))
				#print(temp)
				t_probab*=temp
				flag=1
				break
			else:
				continue
	if temp==0:
		t_probab=(d*total_types_unigrams())/totaliser(unigrams)
		# if flag==0:
		# 	flag=1
		# 	temp=reduction_factor/totaliser(unigrams)
		# 	temp+=(d/totaliser(unigrams))
		# 	t_probab*=temp
		# 	break

	return t_probab

def p_kneser_bigram(inp_sen,corpus):
	inp_tokens=word_tokenize(inp_sen)
	t_probab=1
	d=0.75
	for i in range(len(inp_tokens)-1):
		if inp_tokens[i] in bigrams:
			w1=inp_tokens[i]
			if inp_tokens[i+1] in bigrams[w1]:
				w2=inp_tokens[i+1]
				temp1=((max((bigrams[w1][w2]-d),0))/unigrams[w1])
				lamda1=(d/unigrams[w1])*(len(bigrams[w1]))
				count_x_w2=0
				for j in bigrams:
					if w2 in bigrams[j]:
						count_x_w2+=1
				temp2=(max((count_x_w2-d),0)/total_types_unigrams())
				lamda2=(d/total_unigrams())
				probab=(temp1+(lamda1*(temp2+lamda2)))
				t_probab*=probab
			else:
				w2=inp_tokens[i+1]
				temp1=0
				lamda1=(d/unigrams[w1])*(len(bigrams[w1]))
				count_x_w2=0
				for j in bigrams:
					if w2 in bigrams[j]:
						count_x_w2+=1
				temp2=(max((count_x_w2-d),0)/total_types_unigrams())
				lamda2=(d/total_unigrams())
				probab=(temp1+(lamda1*(temp2+lamda2)))
				t_probab*=probab
		else:
			tempo=(total_types_unigrams()*d)/(totaliser(unigrams)*total_types_bigrams())
			t_probab*=tempo
	return t_probab
def p_kneser_trigram(inp_sen,corpus):
	inp_tokens=word_tokenize(inp_sen)
	t_probab=1
	d=0.75
	temp=0
	for i in range(len(inp_tokens)-2):
		if inp_tokens[i] in trigrams:
			w1=inp_tokens[i]
			if inp_tokens[i+1] in trigrams[w1]:
				w2=inp_tokens[i+1]
				if inp_tokens[i+2] in trigrams[w1][w2]:
					w3=inp_tokens[i+2]
					temp1=(max((trigrams[w1][w2][w3]-d),0)/bigrams[w1][w2])
					lamda1=(d/bigrams[w1][w2])*(len(trigrams[w1][w2]))
					count_x_w2_w3=0
					for j in trigrams:
						if w2 in trigrams[j]:
							if w3 in trigrams[j][w2]:
								count_x_w2_w3+=1
					count_x_w2=0
					for j in bigrams:
						if w2 in bigrams[j]:
							count_x_w2+=1
					temp2= (max((count_x_w2_w3-d),0)/count_x_w2)
					lamda2=(d/unigrams[w1])*len(bigrams[w1])
					count_x_w3=0
					for j in bigrams:
						if w3 in bigrams[j]:
							count_x_w3+=1
					temp3=(max((count_x_w3-d),0)/total_types_unigrams())
					lamda3=(d/total_unigrams())
					probab=(temp1 + (lamda1*(temp2+(lamda2*(temp3+lamda3)))))
					t_probab*=probab
				else:
					w3=inp_tokens[i+2]
					temp1=0
					lamda1=(d/bigrams[w1][w2])*(len(trigrams[w1][w2]))
					count_x_w2_w3=0
					for j in trigrams:
						if w2 in trigrams[j]:
							if w3 in trigrams[j][w2]:
								count_x_w2_w3+=1
					count_x_w2=0
					for j in bigrams:
						if w2 in bigrams[j]:
							count_x_w2+=1
					temp2= (max((count_x_w2_w3-d),0)/count_x_w2)
					lamda2=(d/unigrams[w1])*len(bigrams[w1])
					count_x_w3=0
					for j in bigrams:
						if w3 in bigrams[j]:
							count_x_w3+=1
					temp3=(max((count_x_w3-d),0)/total_types_unigrams())
					lamda3=(d/total_unigrams())
					probab=(temp1 + (lamda1*(temp2+(lamda2*(temp3+lamda3)))))
					t_probab*=probab
			else:
				tempo=(total_types_unigrams()*d)/(totaliser(unigrams)*total_types_trigrams())
				t_probab*=tempo
		else:
			tempo=(total_types_unigrams()*d)/(totaliser(unigrams)*total_types_trigrams())
			t_probab*=tempo

	return t_probab

def p_bell_unigram(inp_sen,corpus):
	inp_tokens=word_tokenize(inp_sen)
	t_probab=1
	for i in (inp_tokens):
		if i in unigrams:
			probab=(unigrams[i])/(total_types_unigrams()*total_unigrams())
			t_probab*=probab
		else:
			probab=t_probab=(d*total_types_unigrams())/totaliser(unigrams)
	return t_probab

def p_bell_bigram(inp_sen,corpus):
	inp_tokens=word_tokenize(inp_sen)
	t_probab=1
	for i in range(len(inp_tokens)-1):
		if inp_tokens[i] in bigrams:
			w1=inp_tokens[i]
			if inp_tokens[i+1] in bigrams[w1]:
				w2=inp_tokens[i+1]
				count_d_w1_x=0
				for i in bigrams[w1]:
					count_d_w1_x+=1
				count_w1_x=0
				for i in bigrams[w1]:
					count_w1_x+=bigrams[w1][i]
				lamda=1-(count_d_w1_x/(count_w1_x+count_d_w1_x))
				temp1=lamda*(bigrams[w1][w2]/(count_d_w1_x+count_w1_x))
				temp2=(1-lamda)*(unigrams[w2]/total_unigrams())
				temp=temp1+temp2
				t_probab*=temp
			else:
				tempo=(total_types_unigrams()*d)/(totaliser(unigrams)*total_types_bigrams())
				t_probab*=tempo
		else:
			w1=inp_tokens[i]
			w2=inp_tokens[i+1]
			count_d_w1_x=0
			for i in bigrams[w1]:
				count_d_w1_x+=1
			count_w1_x=0
			for i in bigrams[w1]:
				count_w1_x+=bigrams[w1][i]
			z=total_types_unigrams()-count_d_w1_x
			lamda=1-(count_d_w1_x/(count_w1_x+count_d_w1_x))
			temp1=lamda*(count_d_w1_x/(z*(count_w1_x+count_d_w1_x)))
			temp2=(1-lamda)*(unigrams[w2]/total_unigrams())
			temp=temp1+temp2
			t_probab*=temp

	return t_probab
running_conditions()
file=open(sys.argv[3],'r').readline(s)
c_unigram(file)
c_bigrams(file)
c_trigrams(file)

while (1):
	inp_sentence=input("Input Sentence: ")
	inp_sentence=inp_sentence.lower()
	inp_sentence=re.sub(r'[^\w\s]','',inp_sentence)
	#print(inp_sentence)
	if inp_sentence=='q' or inp_sentence=='Q':
		quit()
	if sys.argv[1]=='1' and sys.argv[2]=='k':
		jam=p_kneser_unigram(inp_sentence,unigrams)
		print(jam)
	if sys.argv[1]=='2' and sys.argv[2]=='k':
		jam=p_kneser_bigram(inp_sentence,unigrams)
		print(jam)
	if sys.argv[1]=='3' and sys.argv[2]=='k':
		jam=p_kneser_trigram(inp_sentence,unigrams)
		print(jam)
	if sys.argv[1]=='1' and sys.argv[2]=='w':
		jam=p_bell_unigram(inp_sentence,unigrams)
		print(jam)
	if sys.argv[1]=='2' and sys.argv[2]=='w':
		jam=p_bell_bigram(inp_sentence,unigrams)
		print(jam)
	if sys.argv[1]=='3' and sys.argv[2]=='w':
		jam=p_bell_trigram(inp_sentence,unigrams)
		print(jam)





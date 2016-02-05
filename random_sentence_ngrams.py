import random
import nltk
from nltk import ngrams
import string
import sys


def remv(mystr,punctuations):
	'''(str)->str
	remove the listed punctuations in the string mystr
	'''
	mystr = "".join([c for c in mystr if c not in list(punctuations)])
	return mystr

def non_blankword(path):
	'''(str)->list
	This function take string refering the path of a file and process the document in the file 
	including strip blank lines, remove punctuations and split lines in lists. The output is 
	a list of words
	''' 
        with open(path) as f:
                lines = [line.strip() for line in f]
                lines = [remv(line,string.punctuation) for line in lines]
                lines = [l for l in lines if l]
                lines = list(l.split(" ") for l in lines)
        lines = reduce(lambda x,y: x+y,lines)
        return lines

def sort_by_value(mydict):
    ''' (dict) -> list
    this function takes mydict as input and return a list of all items sorted by value in decreasing order
    as output, it returns a list of 2-tupples.
    >>> sort_by_value({"lucie":2,"lu":1,"lily":3})
    [('lily', 3), ('lucie', 2), ('lu', 1)]
    '''
    return sorted(mydict.items(),key = lambda x:x[1],reverse = True)

def counts_cumul(l):
    ''' (list) -> list
    this function takes a list 2-tupples as input, for each item i, it calculates the cumulated value 
    of all the previous items and as output, it returns a list of 2-tupples.
    <<< counts_cumul([('lily', 3), ('lucie', 2), ('lu', 1)])
    [('lily', 3), ('lucie', 5), ('lu', 6)]
    '''
    if len(l)==1:
	return l
    else:
        list1 = []
c = 0
        for i in range(len(l)):
          if i==0:
            list1.append((l[i][0],l[i][1]))
          else: 
            list1.append((l[i][0],l[i][1]+list1[i-1][1]))
        return list1

def choose_random(mydict):
    ''' (dict) -> str
    this function takes mydict (which contains words as mydict.keys and counts of words as mydict.values) as input,
    and returns a randomly selected key taking account of the counts as proportions.
    '''
    #change the un_ordered dictionary mydict to list
    #mylist = mydict.items() 
    # or even generate a sorted list
    mylist = sort_by_value(mydict)

    # creat another list of 2-tupple while the second item is the cumulated value of counts
    list2 = counts_cumul(mylist)
   
    # generate a random number between the interval 1 and the sum of counts
    
    randnumber = random.randint(1,list2[-1][1])
    # given a random number between the interval 1:sum of counts, find in list2 the first value greater than this
    # random number and return the relevant key 
    for i in range(len(list2)):
        if (list2[i][1]>=randnumber):
		return list2[i][0]
      


def generate_model_rand(cfdist,word,steps=10):
        ''' (dict,str,int) -> None   
        this function print a 10 words which begins from the input word, and followed by a word chosen randomly in accord
        with conditional frequency distribution in each step. no result is returned.
        '''
	print(word)
	for i in range(steps):
		if cfdist[word]:
			tup = choose_random(cfdist[word])
			print ' '.join([c for c in tup])
			word = tup[-1]
		else:
			print("no other word after this word")
			break


if __name__ == "__main__":
	path = sys.argv[1]
	# process a file and returns a list of words 
	listofwords = non_blankword(path)
	# do bigrams on the list of words
	mygrams = list(ngrams(listofwords,n=int(sys.argv[2])))
	#count the number of occurences of w2 given the previous word is w1
	cfd = nltk.ConditionalFreqDist()
	for i in mygrams:
		condition = i[0]
		cfd[i[0]][i[1:]]+=1

	while True:
        	r = raw_input("write a word(to stop, pls type 'youcanstop'): ")
     		if r == 'youcanstop':
        		break
    		generate_model_rand(cfd,r)


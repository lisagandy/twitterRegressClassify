import numpy as np
import MySQLdb as mdb
import re
import copy
#from celeb_retweets import RetweetCollector

upperRange = None
lsPosWords=None
lsNegWords=None

celebIDS=None

def lenCelebIDS():
   global celebIDS
   getCelebIDS()
   return len(celebIDS)

def getCelebIDS():
   global celebIDS
   
   if celebIDS==None:
      celebIDS=[]
      fOpen = open("/home/lisagandy/tweets/celeb_pol_ids.txt")
      line = fOpen.read()
      celebIDS = [line.strip() for line in line.split("\r")]
      celebIDS = list(set(celebIDS))
      #print celebIDS
   return celebIDS

def isCelebID(celeb_id): 
   getCelebIDS()
   if str(celeb_id) in celebIDS:
      return True
   return False
   
def findNumFollowersAll():
    print 'HERE'
    conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCollector');
    cursor = conn.cursor(mdb.cursors.DictCursor)
    lsAllNums=[]
    #rc = RetweetCollector()
    
    for i,user_id in enumerate(getCelebIDS()):
         sqlStr = "Select followers from user_info where user_id=%s" % user_id
         cursor.execute(sqlStr)
         dRes = cursor.fetchone()
         if dRes:
            lsAllNums.append(dRes['followers'])
    
    lsAllNums.sort()        
    print lsAllNums
    origMed = lsAllNums[int(len(lsAllNums)/2.0)]#np.median(lsAllNums)
    lsRangeMed = [abs(num2-origMed) for num2 in lsAllNums]
    lsRangeMed.sort()
    print lsRangeMed
    print int(len(lsRangeMed)/2.0)
    madE = lsRangeMed[654]*1.482*2#np.median(lsRangeMed) * 1.483 * 2
   
    print origMed
    print madE
    lowerRange = origMed-madE
    upperRange = origMed+madE
    
    f = open("upper_lower_range_followers.txt",'w')
    f.write(str(lowerRange)+"\n")
    f.write(str(upperRange)+"\n")
    f.write(str(origMed)+" " + str(madE)+"\n")
    f.close()  
      
#uses the MADe detection method for finding outliers
def isOutlier(num,lsAllNums,newNum=True):
   global upperRange
   
   if newNum:
      origMed = np.median(lsAllNums)
      lsRangeMed = [abs(num2-origMed) for num2 in lsAllNums]
      MADe = np.median(lsRangeMed) * 1.483 * 2
      upperRange = origMed + MADe
   
   if num >= upperRange:
      return True
   else:
      return False
      
def weirdChars(sStr):

    cMatch = re.compile(r'(([A-Z]+[0-9]+)|([0-9]+[A-Z]+))')
    cMatch2 = re.compile(r'\s+')

    lList = cMatch.findall(sStr)
    lList2 = cMatch2.findall(sStr)

    if len(lList) > 0:
        num1 = float(len(lList))
        num2 = float(len(lList2))

        #if 10% or more of the words are something
        #like A200, 2GHZ, and so on get rid of
        #story
        #print num1/num2
        if num2 > 0 and num1/num2 >= .1:
            return True

    return False

def findHighAffectWords():
   f = open("pos_words_wordnet.txt",'w')
   
   from nltk.corpus import wordnet as wn
   lsPos = []
   lsNeg = []
   lsPosHF = [word.strip() for word in open("/home/lisagandy/tweets/pos_words_anew.txt").read().split('\n')]
   lsNegHF = [word.strip() for word in open("/home/lisagandy/tweets/neg_words_anew.txt").read().split('\n')]
   #read in terms from file
   # lsPosHF = ["fun","joy","car","win","joke","gift","sex","cash","kiss","brave","plane","song","happy","heart","talent","quick","lucky","couple","rescue","engaged","pretty","loved","travel","leader","passion","desire","holiday","inspired","memories","progress","success","laughter","birthday","romantic","exercise","promotion","surprised","beautiful","confident","excitement"]
   #    lsPosLF = ["nude","lust","sexy","fame","alert","champ","thrill","cheer","glory","flirt","dazzle","casino","richs","erotic","dancer","aroused","dollar","elated","miracle","admired","orgasm","terrific","intimate","reunion","ecstasy","treasure","sunlight","festive","graduate","fireworks","adventure","athletics","affection","valentine","intercourse","infatuation","astonished","triumphant","millionaire","rollercoaster"]
   #    
   #    lsNegLF = ["demon","shark","rude","rage","toxic","venom","slap","snake","devil","annoy","detest","tumour","betray","sinful","insult","scared","killer","leprosy","poison","hatred","pervert","wicked","destroy","intruder","outrage","torture","hostile","disloyal","terrified","assassin","ambulance","slaughter","nightmare","humiliate","jealousy","cockroach","distressed","unfaithful","hurricane","suffocate"]
   #    lsNegHF = ["mad","gun","war","fire","rape","evil","fight","pain","crash","hate","bomb","anger","angry","fear","burn","abuse","victim","afraid","horror","tense","bloody","guilty","cancer","trouble","panic","surgery","danger","tragedy","assault","stress","pressure","confused","divorce","violent","accident","disaster","rejected","nervous","suspicious","controlling"]
   #    
   pos_terms = []
   for term in lsPosHF:
      pos_terms.append(term)
      syn_sets = wn.synsets(term)
      for syn_set in syn_sets:
         pos_terms.extend(syn_set.lemma_names)
   
   # for term in lsPosLF:
   #     syn_sets = wn.synsets(term)
   #     pos_terms.append(term)
   #     for syn_set in syn_sets:
   #        pos_terms.extend(syn_set.lemma_names)
   
   pos_terms = list(set(pos_terms))
   for term in pos_terms:
      if len(term)<=2:
         continue
      f.write(term.replace("_"," ").lower())
      f.write("\n")
   f.close()
   
   f = open("neg_words_wordnet.txt",'w')
   pos_terms = []
   for term in lsNegHF:
      pos_terms.append(term)
      syn_sets = wn.synsets(term)
      for syn_set in syn_sets:
         pos_terms.extend(syn_set.lemma_names)
   
   # for term in lsNegLF:
   #       pos_terms.append(term)
   #       syn_sets = wn.synsets(term)
   #       for syn_set in syn_sets:
   #          pos_terms.extend(syn_set.lemma_names)
   
   pos_terms = list(set(pos_terms))
   for term in pos_terms:
      if len(term) <= 2:
         continue
      f.write(term.replace("_"," ").lower())
      f.write("\n")
   f.close()

def getPosWords(text):
   global lsPosWords
   if (lsPosWords==None):
      f = open("pos_words_wordnet.txt")
      lsPosWords = f.readlines()
      lsPosWords = [word.replace('\n','').strip() for word in lsPosWords]
   
   retWords=[]
   lsText = text.split()
   for word in lsPosWords:
      if word in ["or","x","can"]:
         continue
      for tempWord in lsText:
         if tempWord==word:
            retWords.append(word)
   
   return retWords

def getNegWords(text):
      global lsNegWords
      if (lsNegWords==None):
         f = open("neg_words_wordnet.txt")
         lsNegWords = f.readlines()
         lsNegWords = [word.replace('\n','').strip() for word in lsNegWords]

      retWords=[]
      lsText = text.split()
      for word in lsNegWords:
            if word in ["or","x","can"]:
               continue
            for tempWord in lsText:
               if tempWord==word: 
                  retWords.append(word)

      return retWords     

def removePunctuation(text, spaces = True,lsExcept=[]):
     """
     Removes punctuation from a string.

     @type text: C{string}
     @param text: a string with punctuation.

     @rtype: C{string}
     @return: the string without punctuation.
     """

     spacePunctuation = ["'",'-','_','=','+','/','\\']
     noSpacePunctuation = ['.','?','!',',',':',';','(',')','[',']','{','}','@','#','$','%','^','&','*','"']

     if spaces:
         for punct in spacePunctuation:
             if punct not in lsExcept:
                 text = text.replace(punct,' ')
     else:
         for punct in spacePunctuation:
             if punct not in lsExcept:
                 text = text.replace(punct,'')
     for punct in noSpacePunctuation:
         if punct not in lsExcept:
             text = text.replace(punct,'')

     return text.strip(' ')

def tweetIncomp(sStr):
    sStr2 = removePunctuation(copy.copy(sStr))
    sStr2 = ''.join(word.strip() for word in sStr2.split())
    
    cMatch = re.compile(r'(([A-Z]*[0-9]*)|([0-9]*[A-Z]*))')
    cMatch2 = re.compile(r'\w*')

    lList = cMatch.findall(sStr2)
    lList2 = cMatch2.findall(sStr2)
    # print lList
    # print lList2
    num1=None
    if len(lList) > 0:
        num1 = float(len(lList))
        num2 = float(len(lList2))
        #print num1/num2

        if num1/num2 < 2:
            print "TWEET IN FOREIGN LANGUAGE OR SOMETHING WEIRD"
            print sStr2
            return True
            
    
    if num1:
       return False


if __name__ == '__main__':
   findNumFollowersAll()
   #findHighAffectWords()
   #print hasPosWord("happy")
   #
   #findUpperRangeFollowers()   
   #print isOutlier(70,[1,2,3,4,5,6,7,8])   
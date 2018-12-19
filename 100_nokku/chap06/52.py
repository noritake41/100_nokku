import codecs
import re
from stemming.porter2 import stem

fin = codecs.open('nlp.txt', 'r', 'utf_8')
punctuation = ""
src = []
string = []
word = ""

if __name__ == "__main__":
  n = 0
  for line in fin:
    for x in line:
      if n == 100:
        break
      punctuation = punctuation + x
      if len(punctuation) > 3:
        punctuation = punctuation[1:4]
        if re.search(r'\.\s[A-Z]|\;\s[A-Z]|\:\s[A-Z]|\?\s[A-Z]|\!\s[A-Z]',punctuation):
          src.append(string)
          string = []
          word = ""
      if x == " ":
        if word != "":
          string.append(word)
          word = ""
          n = n + 1
      elif x == "\n":
        if word != "":
          string.append(word)
          word = ""
          n = n + 1
      elif x == "." or x == ",":
        print("",end="")
      else:
        word = word + x
  src.append(string)

  for stringx in src:
    for wordx in stringx:
      print(wordx,"\t",stem(wordx))
    print("")

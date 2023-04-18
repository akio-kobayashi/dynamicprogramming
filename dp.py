from enum import Enum
from IPython.core.display import display, HTML

'''
  Tag クラス
  置換，挿入，脱落の誤りの定義
'''
class Tag(Enum):
  Correct=1
  Substitution=2
  Deletion=3
  Insertion=4

'''
  Nodeクラス
  格子の頂点の定義
    スタートから格子点までの得点
    経路の種類
    バックポインタ(どこからきたか)
'''
class Node:
  def __init__(self):
    self.score=0
    self.ptr=None
    self.tag=None

def dynamic_programming(str1,str2):

  if str1[0] != '<b>':
    str1.insert(0, '<b>')
    str1.append('<e>')
  if str2[0] != '<b>':
    str2.insert(0, '<b>')
    str2.append('<e>')

  M,N=len(str1),len(str2)

  lattice = [ [Node() for n in range(N+1) ] for m in range(M+1) ]
  for m in range (M+1):
    lattice[m][0].score=m
    if m>0:
      lattice[m][0].ptr=[m-1,0]
  for n in range (N+1):
    lattice[0][n].score=0
    if n>0:
      lattice[0][n].ptr=[0,n-1]
  
  for m in range(1, M+1):
    for n in range(1, N+1):
      node=Node()
      # (m-1, n-1) -> (m, n)
      if str1[m-1] == str2[n-1]: # correct
        node.score=lattice[m-1][n-1].score
        node.tag=Tag.Correct
      else: # substitution
        node.score=lattice[m-1][n-1].score+1
        node.tag=Tag.Substitution
      node.ptr=[m-1, n-1]

      # (m-1, n) -> (m, n) deletion
      score=lattice[m-1][n].score+1
      if score <= node.score:
        node.score=score
        node.ptr=[m-1, n]
        node.tag=Tag.Deletion

      # (m, n-1) -> (m, n) # insertion
      score=lattice[m][n-1].score+1
      if score <= node.score:
        node.score=score
        node.ptr=[m,n-1]
        node.tag=Tag.Insertion

      lattice[m][n]=node

  return lattice

def backtrace(lattice, str1, str2):
  tags=[]
  M, N=len(str1), len(str2)
  curr_node=lattice[M][N]
  while True:
    if curr_node.tag == None:
      break
    tags.append(curr_node.tag)
    curr_node=lattice[curr_node.ptr[0]][curr_node.ptr[1]]

  tags.reverse()
  
  return tags

def html_text(tags, str1, str2):
  str1_html,str2_html=[],[]
  n_str1=n_str2=0
  for tag in tags:
    if tag == Tag.Correct:
      str1_html.append(str1[n_str1])
      str2_html.append(str2[n_str2])
      n_str1+=1
      n_str2+=1
    elif tag == Tag.Substitution:
      str1_html.append("<font color='red'>"+str1[n_str1]+"</font>")
      str2_html.append("<font color='red'>"+str2[n_str2]+"</font>")
      n_str1+=1
      n_str2+=1
    elif tag == Tag.Deletion:
      str1_html.append("<font color='blue'>"+str1[n_str1]+"</font>")
      n_str1+=1
    elif tag == Tag.Insertion:
      str2_html.append("<font color='green'>"+str2[n_str2]+"</font>")
      n_str2+=1

  str1_html.pop(0)
  str1_html.pop(-1)
  str2_html.pop(0)
  str2_html.pop(-1)
 
  str1_html=''.join(str1_html)
  str2_html=''.join(str2_html)

  return str1_html, str2_html


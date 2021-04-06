import sys
import re
import copy
from collections import deque
temp_transition_probs=[]
emmision_probs=[]
tags=[]
transition_probs={}
initial_probs=[]
sum_transition_probs=[]
sum_emission_probs=[]
sum_emission_probs_after=[]
sum_transition_probs_after=[]
for i in range(46):
    initial_probs.append(0)
    sum_transition_probs.append(0)
    sum_emission_probs.append(0)
    sum_emission_probs_after.append(0)
    sum_transition_probs_after.append(0)

with open('hmmmodel.txt', 'r') as f:
    lines=f.readlines()
    for i in range(len(lines)):
        x=lines[i].split()
        # print(x)
        if len(x)==5:
            temp=[]
            temp.append(x[0])
            temp.append(x[2])
            temp.append(float(x[4]))
            if x[0]!="Begin":
                for y in range(len(tags)):
                    if x[0]==tags[y]:
                        sum_transition_probs[y]+=float(x[4])
                        break
            temp2=copy.copy(temp)
            temp_transition_probs.append(temp2)
        if len(x)==4 and i>0:
            temp=[]
            y=x[1].split("|")
            y1=y[0].split("(")
            y2=y[1].split(")")
            temp.append(y1[1])
            temp.append(y2[0])
            temp.append(float (x[3]))
            for z in range(len(tags)):
                if y2[0]==tags[z]:
                    sum_emission_probs[z]+=float(x[3])
                    break
            temp2=copy.copy(temp)
            emmision_probs.append(temp2)
        if len(x)>40:
            for i in range(1,len(x)):
                tags.append(x[i])


for i  in temp_transition_probs:
    if i[0]!='Begin':
        for j in range(len(tags)):
            if i[0]==tags[j]:
                i[2]/=sum_transition_probs[j]
                break
for i  in temp_transition_probs:
    if i[0]!='Begin':
        for j in range(len(tags)):
            if i[0]==tags[j]:
                sum_transition_probs_after[j]+=i[2]
                break
for i in temp_transition_probs:
    if i[1] in transition_probs:
        temp=[]
        for j in range(len(tags)):
            if i[0]==tags[j]:
                temp.append(int(j))
                break
        temp.append(i[0])
        temp.append(float(i[2]))
        transition_probs[i[1]].append(temp)
    else:
        transition_probs[i[1]]=[]
        temp=[]
        for j in range(len(tags)):
            if i[0]==tags[j]:
                temp.append(int(j))
                break
        temp.append(i[0])
        temp.append(float(i[2]))
        transition_probs[i[1]].append(temp)

for i in emmision_probs:
    for j in range(len(tags)):
        if i[1]==tags[j]:
            i[2]/=sum_emission_probs[j]
for i in emmision_probs:
    for j in range(len(tags)):
        if i[1]==tags[j]:
            sum_emission_probs_after[j]+=i[2]
sum_initial_probs=0
for j in temp_transition_probs:
    if j[0]=='Begin':
        for i in range(len(tags)):
            if j[1]==tags[i]:
                initial_probs[i]=float(j[2])
                sum_initial_probs+=float(j[2])
                break
for i in range(46):
    initial_probs[i]/=sum_initial_probs

def assign_tags(matrix,line):
    length=len(matrix[0])
    ans=[]
    for j in range(length):
        max=0
        for i in range(46):
            if matrix[i][j]>matrix[max][j]:
                max=i

        ans.append(tags[max])
    for i in range(len(ans)):
        print(ans[i], end=" ")


def viterbi(line):
    adj_matrix=[]
    for i in range(46):
        temp=[]
        for j in range(len(line)):
            temp.append(0)
        adj_matrix.append(temp)

    for i in range(len(line)):
        
        for j in range(46):
            if i==0:
                num=1
                for k in emmision_probs:
                    if k[0]==line[0] and k[1]==tags[j]:
                        num*=float(k[2])
                        break
                if num==1:
                    adj_matrix[j][i]=0
                else:
                    #print(num)
                    #print(tags[j])
                    num*=initial_probs[j]
                    adj_matrix[j][i]=num
            else:
                prod=1
                max_el=0                        
                for z in emmision_probs:
                    if z[0]==line[i] and z[1]==tags[j]:
                        for k in transition_probs[tags[j]]:
                            if k[0]!="Begin":
                                prod=1
                                prod*=float(k[2])
                                prod*=adj_matrix[k[0]][i-1]
                                prod*=float(z[2])
                                if (prod>max_el and prod!=1):
                                    prod2=copy.copy(prod)
                                    max_el=prod2
                                

                                
                            
                adj_matrix[j][i]=max_el
        

    # for i in adj_matrix:
    #     print(i)
    assign_tags(adj_matrix,line)
            
        




val= input("")

line=val.split()
viterbi(line)



#print(transition_probs)
#print(emmision_probs)
#print(tags)
#print(initial_probs)

#print(temp_transition_probs)
# for i in range(len(sum_transition_probs)):
#     print(tags[i])
#     print(sum_transition_probs_after[i])



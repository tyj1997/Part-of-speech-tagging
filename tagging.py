import  numpy as np
import re
# ******************************Created by Tan yijia******************************
# ******************************Class:2015211303******************************
# ******************************Number:2015211207******************************
lines=0
Part_of_speech={}                                      #转移概率
Part_of_speech_num=0
word_num=0
word_list=[]                                            #所有单词列表
speech_list=[]                                          #所有标注列表
test_word=[]                                            #测试集句子序列
test_speech=[]                                          #测试集标注
result_speech=[]                                        #测试集标注模型结果
probablity={}                                           #发射概率
accuracy=1                                              #测试结果准确率
with open("C:/Users/Administrator/Desktop/1998-01-105-带音.txt") as wf:
    for i in wf:
        lines+=1
train_size=0.8*lines
test_size=0.2*lines                                       #训练集80%，测试集20%
with open("C:/Users/Administrator/Desktop/1998-01-105-带音.txt") as wf:
    for i in wf:
        train_size-=1
        count1 = i.split()
        if train_size < 0:
            temp=[]
            temps=[]
            for j in range(0, len(count1)):
                w=count1[j].split("/")[0]
                s=count1[j].split("/")[-1]
                temp.append(w)
                temps.append(s)
                if w not in word_list:
                     word_num+=1
                     word_list.append(w)

            if temp!=[]:
                test_word.append(temp)

            if temps!=[]:
                test_speech.append(temps)

            continue
        for j in range(0, len(count1)):
            temp_speech = count1[j].split("/")[-1]
            temp_word = count1[j].split("/")[0]

            if temp_word not in word_list:
                 word_num+=1
                 word_list.append(temp_word)


            if temp_speech not in Part_of_speech:
                Part_of_speech_num += 1
                speech_list.append(temp_speech)
                Part_of_speech[temp_speech]={}

            if temp_speech not in probablity:
                probablity[temp_speech]={}

            if j < len(count1) - 1:
               if count1[j + 1].split("/")[-1] not in Part_of_speech[temp_speech]:
                   Part_of_speech[temp_speech][count1[j + 1].split("/")[-1]]=1
               else:
                   Part_of_speech[temp_speech][count1[j + 1].split("/")[-1]] +=1

            if temp_word not in probablity[temp_speech]:

                probablity[temp_speech][temp_word]=1
            else:
                probablity[temp_speech][temp_word] +=1

    for (k, v) in Part_of_speech.items():
        for i in speech_list:
            if i not in v:
                Part_of_speech[k][i]=1
            else:
                Part_of_speech[k][i] +=1                                      #对转移概率Part_of_speech进行Laplace平滑处理

    for (k, v) in probablity.items():
        for i in word_list:
            if i not in v:
                probablity[k][i]=1
            else:
                probablity[k][i] +=1                                        #对发射概率probablity进行Laplace平滑处理


    for (k,v) in Part_of_speech.items():
        count=0
        for (i,j) in v.items():
            count+=j
        for (i, j) in v.items():
            Part_of_speech[k][i]/=count


    for (k,v) in probablity.items():
        count=0
        for (i,j) in v.items():
            count+=j
        for (i, j) in v.items():
            probablity[k][i]/=count






    for test in test_word:                                       #对测试集进行标注(Viterbi) 算法
        count=0
        now_state=""
        t_speech=[]
        for word in test:
            if count==0:
                max_ini_pro=0
                for sp in speech_list:
                    if probablity[sp][word]>max_ini_pro:
                        int_state=sp
                        max_ini_pro=probablity[sp][word]
                count=1
                t_speech.append(int_state)
                now_state=int_state
            else:
                max_pro_temp=0
                for state in speech_list:
                    pro_move=Part_of_speech[now_state][state]*probablity[state][word]
                    if pro_move>max_pro_temp:
                        max_pro_temp=pro_move
                        temp_state=state
                now_state=temp_state
                t_speech.append(now_state)
        result_speech.append(t_speech)


    #
    # for test in test_word:                                       #对测试集进行标注,以最大频率作为标注
    #     count=0
    #     now_state=""
    #     t_speech=[]
    #     for word in test:
    #         if count==0:
    #             max_ini_pro=0
    #             for sp in speech_list:
    #                 if probablity[sp][word]>max_ini_pro:
    #                     int_state=sp
    #                     max_ini_pro=probablity[sp][word]
    #             count=1
    #             t_speech.append(int_state)
    #             now_state=int_state
    #         else:
    #             max_pro_temp=0
    #             for sp in speech_list:
    #                 pro_move=probablity[sp][word]
    #                 if pro_move>max_pro_temp:
    #                     max_pro_temp=pro_move
    #                     temp_state=sp
    #             now_state=temp_state
    #             t_speech.append(now_state)
    #     result_speech.append(t_speech)




    print("word    test    result")
    for i in range(0,len(result_speech[0])):
        print(test_word[0][i]+'    ',end="")
        print(test_speech[0][i]+'    ',end="")
        print(result_speech[0][i])
    for i in range(0,len(result_speech)):
        sum=0
        true=0
        for j in range(0,len(result_speech[i])):
            sum+=1
            if result_speech[i][j]==test_speech[i][j]:
                true+=1
        temp_accuracy=true/sum
        accuracy+=temp_accuracy
    accuracy/=len(result_speech)
    print("Accuracy:"+str(accuracy))


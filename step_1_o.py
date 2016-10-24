import codecs, sys, os, re
from os import listdir
from os.path import join as joinpath
from os.path import isfile

verbm=['Tense_form','Intransitive_verb','Tense', 'Verb_pattern','Verb_form', 'Tense_choice', 'Seq_of_tenses',
       'Tense_choice_in_conditionals','Voice', 'Voice_choice', 'Voice_form', 'Negative_form',
       'Trans_prep', 'Participial_constr', 'Infinitive_constr','Choice_in_cond', 'Verb_obj_prep_Gerund', 'Prepositional_verb'
       'Participial_constr', 'Verb_pattern', 'Verb_adj', 'Modals_choice', 'Transitive']
adresa=[]
tree=os.walk('C:/Users/Regina5/Desktop/kur_t/')
mistakes=codecs.open('Cor_opechatki.txt', 'w', 'utf-8')
mistak={}
for d, dirs, files in tree:
    for f in files:
        path=os.path.join(d,f)
        adresa.append(path)
withno=codecs.open('Noright_word.txt', 'w', 'utf-8')
#withn={}
#without_right_word=codecs.open('Correction_wtht_wrghtwrd.txt', 'w', 'utf-8')
verb_pattern=codecs.open('verb_pattern.txt', 'w', 'utf-8')
b=0
e=0
dic={}
mas=[]
new_adres=''
maskey_ann=[]
masval_txt=[]
strange=[]
dic2={}
dic3={}
verbal_mist=[]
dic4=['??','?','???', None]#, reg] ? тоже
for fil in adresa:
    if fil.endswith('.ann'):
        maskey_ann.append(fil)
    elif fil.endswith('.txt'):
        masval_txt.append(fil)
for i in range(len(maskey_ann)):
    if maskey_ann[i].split('.')[0]==masval_txt[i].split('.')[0]:
        dic[maskey_ann[i]]=masval_txt[i]
lines_for_correction=codecs.open('Correction.txt', 'w', 'utf-8')#
lines_to_correct = {}#
borders=[]
for key, value in dic.items():#ann
    content=codecs.open(key, 'r', 'utf-8') # избавляться от пустых ann как-то желательно..
    txt_content=codecs.open(value, 'r', 'utf-8')
    deletem=[]
    dic2={}
    dic3={}
    dic8={}
    counter_txt=0
    for line in content:
        if line.startswith ('A') and line.split('\t')[1].split()[0]=='Delete':
            m7=re.search('T(\d+)', line)
            if m7!=None:
                deletem.append(m7.group(1))#(line.split('\t')[1].split()[1])
        elif line.startswith('T'):
            #if '\\' in line or '/' in line:#
             #   mistak[line]=str(key)#
            #elif 'А-я' in line:
             #   lines_to_correct[line]=str(key)#
            if 'Verb_pattern' in line:
                verb_pattern.write(str(line) + str(key) + '\r\n')
            borders=[]
            if len(line.split('\t'))<2 or len(line.split('\t')[1].split())==0:
                print(str(key)+ str(line))
            else:
                m5=re.search('pos_', line.split('\t')[1].split()[0])
                if line.split('\t')[1].split()[0] != 'suggestion' and m5 == None:
                    m = re.search('^T(\d+)', line)
                    if m != None:

                        error_name = line.split('\t')[1].split()[0]

                        wordwrong = line.split('\t')[2].split()
                        b = int(line.split('\t')[1].split()[1])
                        e_preview = line.split('\t')[1].split()[2]
                        if ';' not in e_preview:
                            e = int(line.split('\t')[1].split()[2])
                        else:
                            e = int(line.split('\t')[1].split()[3])
                        borders.append(error_name)
                        borders.append(b)
                        borders.append(e)
                        borders.append(wordwrong)
                        dic2[m.group(1)] = borders  # ключ у dic3 - это dic2

        elif line.startswith('#'):
            if '\\' in line or '/' in line:#
                mistak[line]=str(key)#
            elif 'А-я' in line:
                lines_to_correct[line]=str(key)
            #if len(line.split('\t')) < 2:
             #   withno.write(str(key)+' ' +str(line)+'\r\n')
            m = re.search('T(\d+)', line)
            if m != None:
                if m.group(1) in dic2.keys():
                    wordright = line.split('\t')[2].strip()
                    m44 = re.search('[A-Z|\s]{6,}', wordright)
                    #if m44!=None:#
                     #   lines_to_correct[line]=str(key)#
                    # m4=re.search('[^a-z|\s|\d]{6,}', wordright)#####рег выр: чтоб только
                    m6 = re.search('GULAG', wordright)
                    m7 = re.search('REALEC', wordright)
                    if m6==None and m7==None and m44!=None:#######
                        lines_to_correct[line]=str(key)#######

                    if wordright not in dic4 and m44 == None:# or m6 != None or m7 != None:  # if '??'etc 'NOT TRUE 'CAUSE YOU...' (caps) не включ в словарь dic2
                        dic2[m.group(1)].append(wordright)  #### {номер:[назв_ош, 2, 8, непр_сл, прав_сл]}
                    elif  wordright not in dic4 and m6!=None:
                        dic2[m.group(1)].append(wordright)  #### {номер:[назв_ош, 2, 8, непр_сл, прав_сл]}
                    elif  wordright not in dic4 and m7!=None:
                        dic2[m.group(1)].append(wordright)  #### {номер:[назв_ош, 2, 8, непр_сл, прав_сл]}


        elif line == None:
            dic2 = {}
    wer = []
    w = []
    dic5 = {}
    for dk,dv in dic2.items():#удаляем из dic2 удаляемые ошибки
        if dv[1] not in wer:
            wer.append(dv[1])
        else:# начало ошибки уже встречалось
            w.append(dv[1])#w- массив начал эл-тов, которые больше 1 раза встреч
    for kr,vr in dic2.items():
        if vr[1] in w and kr not in deletem:# if начало ошибки в списке совпадающих начал - добавить эту пару в dic5
            dic5[kr]=vr# словарь повторяющихся пар
    dic6 = {}
    #gf = []# gf - массив с ]]. Создаем словарь без gf. с повторениями повторения, чтобы потом добавлять их в dic2
    if dic5!={}:
        for ds,fs in dic5.items():
            if len(fs)==5:
                dic6[ds]=fs
            else:
                #gf.append(fs)
                #lines_to_correct[line]=str(key)
                withno.write(str(fs)+ ' ' +str(key)+ '\r\n')
                #withn[fs]=str(ds)
    dic7={}
    if dic6!={}:
        mind=[]
        for ele in w:
            mind=[]
            for ew,rw in dic6.items():
                if rw[1]==ele:
                    mind.append(rw[4])#все прав слова
            rty=1
            rtyu=''
            for elem in mind:
                if len(elem)>rty:
                    rtyu=elem
                    rty=len(elem)
            az=0
            for ew, rw in dic6.items():
                if rw[4]==rtyu and az==0:
                    dic7[ew]=rw# dic7 - это без повторов ,наибольшая длина, чтоб потом остальные похожие удалить - это уже dic3 в итоге будет без повторов
                    az+=1

    mas_ke=[]
    for ka,va in dic2.items():
        if ka in dic7:
            mas_ke.append(ka)
        #elif ka in dic5 and ka not in dic7:
         #   print('repeated mist: ' + str(va))
        elif ka not in dic7 and ka not in dic5:
            mas_ke.append(ka)
    for ju, ku in dic2.items():
        if ju in mas_ke:
            dic8[ju]=ku
    if dic8 != {}:#dictionary of repeated mistakes
        new_adres = str(value) + '_se_tred6'  # naming new txt modified files
        new_text = codecs.open(new_adres, 'w', 'utf-8')
        dic8_copy=dic8.copy()
        for k,v in dic8_copy.items():
            if k in deletem: # убираем ошибки в delete
                del dic8[k]
            elif len(v)<5:
                del dic8[k]
            elif '/' in v[4] or '\\' in v[4]:
                #mistakes.write(str(key)+ ' ' +str(v)+ '\r\n')
                mistak[str(v)] = str(key)

            elif '?' in v[4] or 'А-я' in v[4]:
                #lines_to_correct[line]=str(key)
                lines_to_correct[str(v)]=str(key)

                del dic8[k]
            else:
                dic3[dic8[k][1]] = dic8[k]  # making dictionary with begin indexes as keys, without duplicates

# go through the .txt files by counter_txt and make their copies with verbal mistakes showed only, others are changed on rightword


        counter_txt == 1
        add_txt = 0
        for line2 in txt_content:  # line in txt

            for letter_txt in line2:
                if counter_txt not in dic3.keys() and add_txt == 0:  # no mistake
                    new_text.write(letter_txt)
                    counter_txt += 1
                elif counter_txt not in dic3.keys() and add_txt != 0:  # no, but IN mistaken word
                    counter_txt += 1
                    add_txt -= 1
                elif counter_txt in dic3.keys() and add_txt != 0: # ошибка в ошибке?
                    counter_txt += 1
                    add_txt -= 1
                else:  # mistake
                    for keyp, values in dic3.items():
                        if keyp == counter_txt:
                            if dic3[keyp][0] not in verbm and add_txt == 0:  # not verb and not
                                if len(dic3[keyp]) == 5:
                                    if ' OR ' in dic3[keyp][4]:
                                        s = re.sub(' OR.*', '', dic3[keyp][4])
                                        if s != None:
                                            lines_to_correct[str(values)]=str(key)#
                                            #lines_to_correct[line]=str(key)#
                                            new_text.write(str(s))
                                    elif ' // ' in dic3[keyp][4]:
                                        s=re.sub (' //.*', '', dic3[keyp][4])
                                        if s!=None:
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            new_text.write(str(s))
                                    elif '/' in dic3[keyp][4] or '\\' in dic3[keyp][4]:
                                        s=re.sub ('/.*', '', dic3[keyp][4])
                                        s1=re.sub ('\\.*', '', dic3[keyp][4])
                                        if s!=None:
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            new_text.write(str(s))
                                        if s1!=None:
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            new_text.write(str(s1))
                                    else:
                                        new_text.write(str(dic3[keyp][4]))
                                else:#####
                                    withno.write(str(line)+ ' '+ str(key) + '\r\n')#####
                                    #withn[line]=str(key)
                            elif dic3[keyp][0] in verbm and keyp not in w:# there are duplicates
                                if len(values)>4:#
                                    if ' OR ' in dic3[keyp][4]:
                                        s1 = re.sub(' OR.*', '', dic3[keyp][4])#Here\'s OR in verbal mistake:
                                        if s1 !=None:#
                                            #lines_to_correct[line] = str(key)#
                                            lines_to_correct[str(values)]=str(key)#

                                            dic3[keyp][4]=s1#
                                            new_text.write(str(s1))# не включаем в новый текст ,только прав вар записываем
                                    elif ' \\\\ ' in dic3[keyp][4]:
                                        s1 = re.sub(' \\.*', '', dic3[keyp][4])#
                                        if s1 !=None:#Here\'s \\ in verbal mistake:
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            dic3[keyp][4]=s1#
                                            new_text.write(str(s1))#
                                    elif '//' in dic3[keyp][4]:
                                        s1 = re.sub('//.*', '', dic3[keyp][4])#Here\'s // in verbal mistake:
                                        if s1 !=None:#
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            dic3[keyp][4]=s1#
                                            new_text.write(str(s1))
                                    elif '/' in dic3[keyp][4]:
                                        s1 = re.sub('//.*', '', dic3[keyp][4])#
                                        if s1 !=None:#Here\'s / in verbal mistake:
                                            mistak[str(values)]=str(key)
                                            #mistakes.write(str(key) + ' ' + str(v) + '\r\n')

                                            dic3[keyp][4]=s1#
                                            new_text.write(str(s1))
                                    else:#
                                        new_text.write(str(dic3[keyp]))#this one is written OK
                                else:######
                                    withno.write(str(line) + ' ' + str(key) + '\r\n')  #####
                                    #withn[line]=str(key)

                                    #   lines_to_correct[line]=str(value)#this is verb but len<=4
                            elif dic3[keyp][0] in verbm and keyp in w:# если не одна ошибка глагольная (нач индекс одинаков у неск-х ошибок)
                                new_text.write(str(dic3[keyp][4]))# не пишем []
                            add_txt += (dic3[keyp][2] - dic3[keyp][1] - 1)
                            counter_txt += 1
        new_text.close()
    deletem = []
for k1, v1 in mistak.items():
    mistakes.write(str(v1)+ ' ' + str(k1)+ '\r\n')
print(lines_to_correct)
for k_, v_ in lines_to_correct.items():
    lines_for_correction.write(str(v_)+ ' ' + str(k_)+ '\r\n')
lines_for_correction.close()
mistakes.close()
verb_pattern.close()
#for l, ll in withn.items():
 #   withno.write(str(ll)+ ' '+ str(l)+ '\r\n')
withno.close()






import codecs, sys, os, re, nltk
from nltk.tokenize import sent_tokenize
from nltk import WordPunctTokenizer
from nltk.stem import WordNetLemmatizer
from os import listdir
from os.path import join as joinpath
from os.path import isfile

lem = WordNetLemmatizer()
mistake = 'Infinitive_constr'
verbm = ['Tense_form', 'Intransitive_verb', 'Tense', 'Verb_pattern', 'Verb_form', 'Tense_choice', 'Seq_of_tenses',
         'Tense_choice_in_conditionals', 'Voice', 'Voice_choice', 'Voice_form', 'Negative_form',
         'Trans_prep', 'Participial_constr', 'Infinitive_constr', 'Choice_in_cond', 'Verb_obj_prep_Gerund',
         'Prepositional_verb', 'Verb_adj', 'Modals_choice', 'Transitive']
clear = []
clc = 0
counter_clear = 0
counter_adv = 0
ok = ['VBZ', 'VB', 'VBG', 'TO', 'MD', 'VBN', 'VBP', 'VBD']
cleared = codecs.open(mistake + '_clear4.txt', 'w', 'utf-8')
cleared_ad = codecs.open(mistake + '_clear_adverbs4.txt', 'w', 'utf-8')
cleared_ad_file = codecs.open(mistake + '_clear_adverbs_files2.txt', 'w', 'utf-8')
adresa2 = []
mas_txt_for_exerc = []
tree = os.walk('C:/Users/Regina5/Desktop/kur_t/')
for d, dirs, files in tree:
    for f in files:
        path = os.path.join(d, f)
        adresa2.append(path)
for new in adresa2:
    if new.endswith('_tred4'):
        mas_txt_for_exerc.append(new)
counter_of_sent = 0
massive = []
j = ''
k = ''
for one_file in mas_txt_for_exerc:
    content_ex = codecs.open(one_file, 'r', 'utf-8')
    massy = []
    mas_all = []
    for line_ex in content_ex:
        m = ''
        li = sent_tokenize(line_ex)
        counter_sent = -1
        for sent in li:
            counter_sent += 1
            m9 = re.search('[\w\d]', sent)
            if m9 != None:
                if mistake in sent and sent not in mas_all:
                    mas_all = []
                    mas_all.append(sent)
                    if counter_sent >= 1:
                        r = li[counter_sent - 1]
                        mas_all.insert(0, r)
                    if counter_sent >= 2:
                        r2 = li[counter_sent - 2]
                        mas_all.insert(0, r2)

                    if counter_sent + 1 < len(li):
                        e = li[counter_sent + 1]
                        mas_all.append(e)
                    if counter_sent + 2 < len(li):
                        e2 = li[counter_sent + 2]
                        mas_all.append(e2)

                    # print('mas_all: ' + str(mas_all) # из абзаца от 1 до 5 предложений, которые в обрабатываются для упражнения
                    massive = []
                    for one_s in mas_all:
                        m11 = re.findall('\[\'' + mistake + '\'.+?\[.+?\].*?\]', one_s)
                        m7 = re.search('\[\'' + mistake + '\'.+?\[.+?\].*?\]', one_s)
                        if m7 != None:
                            m = re.search(mistake + '\', (\d.+?), ', one_s)
                            if m != None:
                                massive.append(m.group(1))
                    massy = []
                    for one2 in mas_all:  # для предложения в массиве предложений
                        m10 = re.search('\[\'' + mistake + '\'.+?\[.+?\].*?\]', one2)
                        if m10 != None:
                            m = re.search('(.*?\[\'' + mistake + '\', ' + max(massive) + ', .*?\]), ', one2)
                            if m != None:
                                if massive != []:
                                    tre = re.search(
                                        '\[\'' + mistake + '\', ' + max(massive) + ', .+?\[.+?\], \'(.*?)\'\]', one2)
                                    wrong = re.search(
                                        '\[\'' + mistake + '\', ' + max(massive) + ', .+?\[(.+?)\], \'.*?\'\]', one2)
                                    if wrong != None:
                                        wr_word = wrong.group(1)
                                        w = ''
                                        wr_w = wr_word.split(', ')
                                        for woi in wr_w:
                                            w = w + woi + ' '
                                        w_w = w.replace('\'', '')
                                        # w_tag=nltk.word_tokenize(w_w)
                                        # w_tag2=nltk.pos_tag(w_tag)

                                    if tre != None:  # если с макс индексом предложение
                                        l = tre.group(1)  # берем последнее слово\правильное
                                        l2 = l.split(' ')
                                        mlem = ''
                                        co = 0
                                        adverb=0
                                        for onel2 in l2:

                                            mlem_ta = onel2.lower()
                                            mlem_tag = nltk.word_tokenize(mlem_ta)
                                            mlem_tag2 = nltk.pos_tag(mlem_tag)
                                            print('mlem_tag2' + str(mlem_tag2))
                                            mlem_tag_serc = re.search(', \'([A-Z]{2,})\'', str(mlem_tag2))
                                            if mlem_tag_serc.group(1) not in ok:
                                                adverb+=1
                                                print('an adv here: '+str(mlem_tag_serc.group(1)))
                                            else:
                                                print(mlem_tag_serc.group(1))
                                            lemma = lem.lemmatize(mlem_ta, pos='v')

                                            light_verbs = ['be', 'have', 'to', 'will',
                                                           'shall']  # , 'could', 'would', 'should']
                                            if len(
                                                    l2) > 1:  # не для ошибок, в которых вставить предлог нужно ,т.к. в подсказке он есть
                                                if lemma in light_verbs and co > 0 and len(l2) == 2:
                                                    mlem += lemma

                                                elif co==0 and lemma not in light_verbs:  # co==0 and lemma not in light_verbs; co>0 and lemma not in light_verbs
                                                    mlem += lemma + ' '
                                                elif co>0 and lemma not in light_verbs:
                                                    mlem+= lemma + ' '
                                                co += 1
                                            else:
                                                mlem = lemma
                                    print('mlem' + str(mlem))
                                    m13 = re.findall('\[\'' + mistake + '\'.+?\[.+?\].*?\]', one2)
                                    in_senum = 0
                                    for in_sent in m13:
                                        in_senum += 1
                                    #adverb = 0
                                    if in_senum >= 2:
                                        #for one_t in mlem_tag2:
                                         #   print('insenum>2 and one_t is:' + str(one_t))
                                         #   ok = ['VBZ', 'VB', 'VBG', 'TO', 'MD', 'VBN', 'VBP', 'VBD']
                                         #   mles = re.search(', \'([A-Z]{2,})\'', str(one_t))
                                         #   if mles != None:
                                         #       print(mles.group(1))
                                         #   else:
                                         #       print(mles.group(1))
                                         #   if str(mles.group(1)) not in ok:
                                         #       adverb += 1
                                        k = re.sub(
                                            '\[\'' + mistake + '\', ' + max(massive) + ', .+?\[.+?\], \'(.*?)\'\]',
                                            '(:' + w_w + ':) (' + mlem + ') [' + l + ' ]', one2)
                                        j1 = re.sub('\[\'[^' + mistake + '\'].+?\[.+?\], \'(.*?)\'\]', '\\1',
                                                    k)
                                        m12 = re.search('\[\'' + mistake + '\'.+?\[.+?\].*?\]', j1)
                                        if m12 != None:
                                            m13 = re.search(mistake + '\', (\d.+?), ', j1)
                                            if m13 != None and m.group(1) != max(massive):
                                                j = re.sub('\[\'' + mistake + '\'.+?\[.+?\], \'(.*?)\'\]', '\\1', j1)
                                    if in_senum == 1:
                                        #for one_t in mlem_tag2:
                                        #    print('insenum=1 and one_t is:' + str(one_t))#
#                                           ok = ['VBZ', 'VB', 'VBG', 'TO', 'MD', 'VBN', 'VBP']
                                            #mles = re.search(', \'([A-Z]{2,})\'', str(one_t))
                                            #if mles != None:
                                            #    print(mles.group(1))
                                            #else:
                                            #    print(mles.group(1))
                                            #if str(mles.group(1)) not in ok:
                                            #    adverb += 1
                                        k = re.sub(
                                            '\[\'' + mistake + '\', ' + max(massive) + ', .+?\[.+?\], \'(.*?)\'\]',
                                            '(:' + w_w + ':) (' + mlem + ') [' + l + ' ]', one2)
                                        j = re.sub('\[.*?\[.*?\], \'(.*?)\'\]', '\\1', k)

                                    print('sents with max M after red: ' + str(j))
                                    # если не с макс ошибкой
                            else:  # these's a _mistake_ but in other sent there is a max_massive
                                k = re.sub('\[\'' + mistake + '\'.+?\[.+?\], \'(.*?)\'\]', '\\1', one2)
                                j = re.sub('\[\'[^' + mistake + '\'].+?\[.+?\], \'(.*?)\'\]', '\\1', k)
                        else:  # no _mistake_ but can be others
                            j = re.sub('\[.*?\[.*?\], \'(.*?)\'\]', '\\1', one2)
                        if j not in massy:
                            massy.append(j)
                    mas2 = " ".join(massy)
                    print('almost an exercise: ' + str(mas2))
                    counter_of_sent += 1
                    for a in verbm:
                        if a in mas2:
                            clc += 1
                    if clc == 0 and '()' not in mas2 and '[' in mas2 and ' ...' not in mas2 and '....' not in mas2 and '((' not in mas2:
                        mas2 = mas2.replace(',,', ',')
                        mas2 = mas2.replace('(?)', '')
                        mas2 = mas2.replace(' ]', ']')
                        mas2 = mas2.replace(' )', ')')
                        mas2 = mas2.replace(' ,', ',')
                        mas2 = mas2.replace(' . ', '. ')
                        mas2 = mas2.replace(' :)', ':)')
                        m15 = re.search('\(.+?\)', mas2)

                        if m15 != None:
                            k = re.search('\([A-z]{1,} [A-z]{1,} [A-z]{1,} [A-z]{1,} [A-z]{1,}.*?\) \[', mas2)
                            if k == None:
                                if adverb == 0:
                                    print('adverb ' + str(adverb))
                                    counter_clear += 1

                                    cleared.write(str(counter_clear) + ')' + str(mas2) + '\r\n')
                                else:
                                    counter_adv += 1
                                    cleared_ad.write(str(counter_adv) + ')' + str(mas2) + '\r\n')
                                    cleared_ad_file.write(
                                        str(counter_adv) + ')' + str(mas2) + ' ' + str(one_file) + '\r\n')

                    clc = 0

cleared.close()
cleared_ad.close()
cleared_ad_file.close()



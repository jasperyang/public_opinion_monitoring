# 脚本作用：将本文件夹下的politic_related_words.xlsx这个文件转换成dict.txt提供给后续使用

import xlrd


politic_related_words = xlrd.open_workbook('politic_related_words.xlsx')


sheet_keywords = politic_related_words.sheet_by_name('关键词')
dict_file = open('extra_data/dict.txt','w+')
for i in range(1,sheet_keywords.nrows):
    word = str(sheet_keywords.cell(i,0))[6:-1]
    words = word.strip().split(' ')
    word = ''
    for w in words:
        word += w
    dict_file.write(word + ' 1\n')
    
dict_file.close()
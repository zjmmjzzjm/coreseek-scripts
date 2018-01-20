#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: mawenbao@hotmail.com
# @date: 2014-09-03

'''
将两个libmmseg中文词典合并为一个。
'''

# check python version
import sys
if sys.version_info[0] == 2:
    import itertools
    map = itertools.imap
    filter = itertools.ifilter
    if sys.version_info[1] < 7:
        print("Require python version 2.7+")
        sys.exit(1)

import argparse

def parse_mmseg_dict(dictPath):
    with open(dictPath, 'r') as f:
        s = set(map(lambda x: x.strip(), filter(lambda x: x.strip()[0] != 'x', f)))
        d = dict()
        for k in s:
           keyword = k.split()[0]
           value = k.split()[1]
           d[keyword]=value
        return d

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description=u'合并libmmseg中文字典文件，不检查词典文件格式。')
    argParser.add_argument('-a', dest='mainDict', required=True, help=u'mmseg主词典的路径，如果合并时有重复词组，则以主词典为准')
    argParser.add_argument('-b', dest='secondDict', required=True, help=u'被合并mmseg词典的路径')
    argParser.add_argument('-o', dest='output', required=True, help=u'输出文件的路径')
    args = argParser.parse_args()

    mainWordSet = parse_mmseg_dict(args.mainDict)
    mainWordSetLen = len(mainWordSet)
    secondWordSet = parse_mmseg_dict(args.secondDict)
    secondWordSetLen = len(secondWordSet)

    mainWordSet.update(secondWordSet)
    numMergedWords = len(mainWordSet)
    numOmittedWords = mainWordSetLen + secondWordSetLen - numMergedWords

    with open(args.output, 'w') as f:
        for word,v in mainWordSet.items():
            f.write('{0}\t{1}\nx:{1}\n'.format(word, v))
    print(u'成功合并2个词典文件 {}({}) + {}({}) =>  {}({})'.format(
        args.mainDict, mainWordSetLen, args.secondDict, secondWordSetLen, args.output, numMergedWords))
    if (0 != numOmittedWords):
        print(u'{}中的{}个重复词组被忽略'.format(args.secondDict, numOmittedWords))

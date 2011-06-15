#-*- coding:utf-8 -*-

import sys
from dochelpers import functions



def test_paramdoc_generator():
    u'''
    デコレータ形式
    '''

    @functions.paramdoc_generator(u'何か返す', 'str',
                                  a=(u'あいうえお', 'int'),
                                  b=u'かきくけこ',
                                  argl=(u'かきくけこ', 'aaa'))
    def test(a, b, c, *argl, **argd):
        u'''テストですヨ'''
        pass


    assert len(test.__doc__) > 10



def test_class():
    u'''
    メタクラス形式
    '''


    class test(object):
        u'''テストですヨ'''

        __metaclass__ = functions.paramdoc_meta(u'何か返す', 'str',
                                                a=(u'あいうえお', 'int'),
                                                b=u'かきくけこ',
                                                argl=(u'かきくけこ', 'aaa'))
        

        def __init__(self, a, b, c, *argl, **argd):
            pass


    print >> sys.stderr, test.__doc__


    assert len(test.__doc__) > 10


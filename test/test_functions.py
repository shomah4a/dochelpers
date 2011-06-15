#-*- coding:utf-8 -*-


from dochelpers import functions



def test_paramdoc_generator():

    @functions.paramdoc_generator(u'何か返す', 'str',
                                  a=(u'あいうえお', 'int'),
                                  b=u'かきくけこ',
                                  argl=(u'かきくけこ', 'aaa'))
    def test(a, b, c, *argl, **argd):
        u'''テストですヨ'''
        pass


    assert len(test.__doc__) > 10

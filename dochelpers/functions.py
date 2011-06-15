#-*- coding:utf-8 -*-

import sys
import os
import inspect


def paramdoc_generator(_retdoc, _rettype=None, **argd):
    u'''
    sphinx 用 docstring を生成

    :param str _retdoc: 返り値の説明
    :param str _rettype: 返り値の型
    :param **argd: 引数名 -> (説明, 型) なキーワード引数群。説明だけでも可
    '''

    def decorator(f):
        u'''
        デコレータですヨ
        '''

        argspec = inspect.getargspec(f)

        args = argspec.args

        if argspec.varargs:
            args.append(argspec.varargs)
        if argspec.keywords:
            args.append(argspec.keywords)

        docs = []

        for arg in args:
            
            if arg not in argd:
                docs.append(':param {0}:'.format(arg))
                continue

            v = argd[arg]

            if isinstance(v, tuple):
                desc, typ = v
            else:
                desc, typ = v, None

            docs.append(':param {0}: {1}'.format(arg, desc))

            if typ is not None:
                docs.append(':type {0}: {1}'.format(arg, typ))


        docs.append(':return: {0}'.format(_retdoc))

        if _rettype is not None:
            docs.append(':rtype: {0}'.format(_rettype))

        if f.__doc__ is None:
            f.__doc__ = ''

        f.__doc__ = f.__doc__ + '\n' + '\n'.join(docs)

        return f

    return decorator


@paramdoc_generator(u'何か返す', 'str',
                    a=(u'あいうえお', 'int'),
                    b=u'かきくけこ',
                    argl=(u'かきくけこ', 'aaa'))
def test(a, b, c, *argl, **argd):
    '''テストですヨ
    '''
    pass


print test.__doc__
        

    


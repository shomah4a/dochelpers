#-*- coding:utf-8 -*-

import sys
import os
import inspect
import types



class _Dummy(object):
    pass


def get_args(tgt):
    u'''
    クラスか関数から引数名リストを返す
    '''

    def getargspec_from_method(meth):
        u'''
        self を抜いた argspec と同等の情報
        '''
        argspec = inspect.getargspec(meth)
        tmp = _Dummy()
        tmp.args = argspec.args[1:]
        tmp.varargs = argspec.varargs
        tmp.keywords = argspec.keywords
        argspec = tmp

        return tmp
        
    if isinstance(tgt, types.FunctionType):
        argspec = inspect.getargspec(tgt)
    elif isinstance(tgt, dict):
        __init__ = tgt['__init__']
        argspec = getargspec_from_method(__init__)
        
    elif hasattr(tgt, '__init__'):
        argspec = getargspec_from_method(tgt.__init__)
    else:
        raise ValueError, 'unknown type: {0}'.format(tgt)

    args = argspec.args

    args = zip(args, args)

    if argspec.varargs:
        args.append((argspec.varargs, '*'+argspec.varargs))
    if argspec.keywords:
        args.append((argspec.keywords, '**'+argspec.keywords))

    return args



def paramdoc_meta(_retdoc, _rettype=None, **argd):
    u'''
    __init__ の引数情報を cls.__doc__ に追加するためのメタクラス

    :param str _retdoc: 返り値の説明
    :param str _rettype: 返り値の型
    :param **argd: 引数名 -> (説明, 型) なキーワード引数群。説明だけでも可
    :return: メタクラスとして使うためのオブジェクト
    '''

    f = paramdoc_generator(_retdoc, _rettype, **argd)

    def meta(name, bases, attrs):
        u'''
        メタクラス同等品ですヨ
        '''

        attrs = f(attrs)

        return type(name, bases, attrs)

    return meta



def paramdoc_generator(_retdoc, _rettype=None, **argd):
    u'''
    sphinx 用 docstring を生成

    :param str _retdoc: 返り値の説明
    :param str _rettype: 返り値の型
    :param **argd: 引数名 -> (説明, 型) なキーワード引数群。説明だけでも可
    :return: デコレータ
    '''

    def decorator(f):
        u'''
        デコレータですヨ
        '''

        args = get_args(f)

        docs = []

        for (arg, name) in args:
            
            if arg not in argd:
                docs.append(':param {0}:'.format(name))
                continue

            v = argd[arg]

            if isinstance(v, tuple):
                desc, typ = v
            else:
                desc, typ = v, None

            docs.append(':param {0}: {1}'.format(name, desc))

            if typ is not None:
                docs.append(':type {0}: {1}'.format(name, typ))


        docs.append(':return: {0}'.format(_retdoc))

        if _rettype is not None:
            docs.append(':rtype: {0}'.format(_rettype))


        if isinstance(f, dict):
            f['__doc__'] = f.get('__doc__', '') + '\n' + '\n'.join(docs)

        else:
            if not hasattr(f, '__doc__') or f.__doc__ is None:
                f.__doc__ = ''
            f.__doc__ = f.__doc__ + '\n' + '\n'.join(docs)
            

        return f

    return decorator


        

    


# coding=utf-8
import A

if __name__ == '__main__':

    ##构建A
    a = A.A(A.Node([[2,8,3],[1,0,5],[4,7,6]]), A.Node([[1,2,3],[4,5,6],[7,8,0]]));
    print "A start:";
    ##开始寻路
    if a.start():
        a.showPath();
    else:
        print "no way";

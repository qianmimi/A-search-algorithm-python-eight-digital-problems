# coding=utf-8
from __future__ import print_function
import copy

def showMap(array2d):
    for x in xrange(0, 3):
        for y in xrange(0, 3):
            print(array2d[x][y], end='')
        print(" ")
    print("--------")
    return;

def move(array2d, srcX, srcY, drcX, drcY):
    temp = array2d[srcX][srcY]
    array2d[srcX][srcY] = array2d[drcX][drcY]
    array2d[drcX][drcY] = temp
    return array2d;

#计算是奇数列还是偶数列
def getStatus(array2d):
    y = 0;

    for i in xrange(0, 3):
        for j in xrange(0, 3):
            for m in xrange(0, i+1):
                for n in xrange(0, j):
                    if array2d[i][j] > array2d[m][n]:
                        y += 1;
    return y;
#描述A算法中的节点数据 
class Node:     
    def __init__(self, array2d, g = 0, h = 0):  
        self.array2d = array2d        #二维数组  
        self.father = None        #父节点  
        self.g = g                #g值
        self.h = h                #h值  
  
    """
    估价公式
     """
    def setH(self, endNode):
        for x in xrange(0, 3):
            for y in xrange(0, 3):
                for m in xrange(0, 3):
                    for n in xrange(0, 3):
                        if self.array2d[x][y] == endNode.array2d[m][n]:
                            self.h += abs(x*y - m*n)

    
    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

class A:
    """
    A 算法 
    python 2.7 
    """
    def __init__(self, startNode, endNode):
        """ 
        startNode:  寻路起点 
        endNode:    寻路终点 
        """  
        #开放列表
        self.openList = []
        #封闭列表  
        self.closeList = []
        #起点  
        self.startNode = startNode
        #终点
        self.endNode = endNode 
        #当前处理的节点
        self.currentNode = startNode
        #最后生成的路径
        self.pathlist = []
        #step步
        self.step = 0
        return;

    def getMinFNode(self):
        """ 
        获得openlist中F值最小的节点 
        """  
        nodeTemp = self.openList[0]  
        for node in self.openList:  
            if node.g + node.h < nodeTemp.g + nodeTemp.h:  
                nodeTemp = node  
        return nodeTemp

    def nodeInOpenlist(self,node):
        for nodeTmp in self.openList:  
            if nodeTmp.array2d == node.array2d:  
                return True  
        return False

    def nodeInCloselist(self,node):
        for nodeTmp in self.closeList:  
            if nodeTmp.array2d == node.array2d:  
                return True  
        return False

    def endNodeInOpenList(self):  
        for nodeTmp in self.openList:  
            if nodeTmp.array2d == self.endNode.array2d:  
                return True  
        return False

    def getNodeFromOpenList(self,node):  
        for nodeTmp in self.openList:  
            if nodeTmp.array2d == node.array2d:  
                return nodeTmp  
        return None

    def searchOneNode(self,node):
        """ 
        搜索一个节点
        """  
        #忽略封闭列表
        if self.nodeInCloselist(node):  
            return  
        #G值计算 
        gTemp = self.step

        #如果不再openList中，就加入openlist  
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            #H值计算 
            node.setH(self.endNode);
            self.openList.append(node)
            node.father = self.currentNode
        #如果在openList中，判断currentNode到当前点的G是否更小
        #如果更小，就重新计算g值，并且改变father 
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp  
                nodeTmp.father = self.currentNode  
        return;

    def searchNear(self):
        """ 
        搜索下一个可以动作的数码
        找到0所在的位置并以此进行交换
        """ 
        flag = False
        for x in xrange(0, 3):
            for y in xrange(0,3):
                if self.currentNode.array2d[x][y] == 0:
                    flag = True
                    break;
            if flag == True:
                break;

        self.step += 1
        if x - 1 >= 0:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x - 1, y)
            self.searchOneNode(Node(arrayTemp));
        if x + 1 < 3:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x + 1, y)
            self.searchOneNode(Node(arrayTemp));
        if y - 1 >= 0:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x, y - 1)
            self.searchOneNode(Node(arrayTemp));
        if y + 1 < 3:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x, y + 1)
            self.searchOneNode(Node(arrayTemp));

        return;

    def start(self):
        ''''' 
        开始寻路 
        '''
        #根据奇数列和偶数列判断是否有解
        startY = getStatus(self.startNode.array2d)
        endY = getStatus(self.endNode.array2d)

        if startY%2 != endY%2:
            return False;
        #将初始节点加入开放列表
        self.startNode.setH(self.endNode);
        self.startNode.setG(self.step);
        self.openList.append(self.startNode)

        while True:
            #获取当前开放列表里F值最小的节点
            #并把它添加到封闭列表，从开发列表删除它
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.step = self.currentNode.getG();

            self.searchNear();

            #检验是否结束
            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp);
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True;
            elif len(self.openList) == 0:
                return False;
            elif self.step > 30:
                return False;

        return True;

    def showPath(self):
        for node in self.pathlist[::-1]:
            showMap(node.array2d)

import Tkinter
import tkMessageBox

import random
#from timeit import default_timer as timer

import chordalGraphUnified_V4 as CG

def isStrInt(str):
    try: 
        int(str)
        return True
    except ValueError:
        return False
    
class gui_tk(Tkinter.Tk):
    """This is the main class contains mainly gui_tk"""
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.initGraph = CG.ChordalGraph(0, 0)
        self.DeletionStart = False
        self.InsertionStart = False
        self.CGDelete = False
        self.CGInsert = False
        #self.dStartMid = 0
        #self.dEndMid = 0
        #self.iStartMid = 0
        #self.iEndMid = 0
        
    def initialize(self):
        self.grid()

        self.lblNumNodesText = Tkinter.StringVar()
        lblNodes = Tkinter.Label(self, textvariable=self.lblNumNodesText)
        lblNodes.grid(row=0, column=0, sticky=Tkinter.W)
        self.lblNumNodesText.set(u'No. of Nodes ')

        self.nodesEntry = Tkinter.Entry(self)
        self.nodesEntry.grid (row=0, column=1, sticky=Tkinter.W)
        
        self.lblNumEdgesText = Tkinter.StringVar()
        lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
        lblEdges.grid(row=1, column=0, sticky=Tkinter.W)
        self.lblNumEdgesText.set(u'No. of Edges ')
    
        self.edgesEntry = Tkinter.Entry(self)
        self.edgesEntry.grid (row=1, column=1, sticky=Tkinter.W)
        
        self.lblNumEdgesText = Tkinter.StringVar()
        lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
        lblEdges.grid(row=2, column=1, sticky=Tkinter.W)
        self.lblNumEdgesText.set(u'+++EITHER+++')
        
        buttonCreateCoG = Tkinter.Button(self,text=u'Generate Complete Graph', 
                                           command=self.onCreateCoGClick)
        buttonCreateCoG.grid(row=3, column=0, sticky=Tkinter.W)
        
        buttonViewCoG = Tkinter.Button(self,text=u'View Complete Graph', 
                                          command=self.onViewCoGClick)
        buttonViewCoG.grid(row=3, column=1, sticky=Tkinter.W)
        
        self.lblNumEdgesText = Tkinter.StringVar()
        lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
        lblEdges.grid(row=4, column=1, sticky=Tkinter.W)
        self.lblNumEdgesText.set(u'+++OR+++')
        
        buttonCreateTree = Tkinter.Button(self,text=u'Generate Tree', 
                                            command=self.onCreateTreeClick)
        buttonCreateTree.grid(row=5, column=0, sticky=Tkinter.W)
        
        buttonViewTree = Tkinter.Button(self,text=u'View Tree', 
                                            command=self.onViewTreeClick)
        buttonViewTree.grid(row=5, column=1, sticky=Tkinter.W)
        
        self.lblNumEdgesText = Tkinter.StringVar()
        lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
        lblEdges.grid(row=6, column=1, sticky=Tkinter.W)
        self.lblNumEdgesText.set(u'===THEN===')
    
        buttonCreateCT = Tkinter.Button(self,text=u'Generate Clique Tree', 
                                          command=self.onCreateCTClick)
        buttonCreateCT.grid(row=7, column=0, sticky=Tkinter.W)        
        
        buttonViewCT = Tkinter.Button(self,text=u'View Clique Tree', 
                                          command=self.onViewCTClick)
        buttonViewCT.grid(row=7, column=1, sticky=Tkinter.W)
    
        buttonCreateCG = Tkinter.Button(self,text=u'Generate Chordal Graph', 
                                             command=self.onCreateCGClick)
        buttonCreateCG.grid(row=8, column=0, sticky=Tkinter.W)
    
        buttonViewCG = Tkinter.Button(self,text=u'View Chordal Graph', 
                                           command=self.onViewCGClick)
        buttonViewCG.grid(row=8, column=1, sticky=Tkinter.W)
        
    def onCreateCoGClick(self):
        """function to check valid input and to call Chordal Graph"""

        noNodes = self.nodesEntry.get()
        if isStrInt(noNodes):
            noNodes = int (self.nodesEntry.get())
            if (noNodes < 0):
                tkMessageBox.showwarning("Warning","Entry for nodes is less than 0.")
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for nodes is not an integer.")
            return
        
        noEdges = self.edgesEntry.get()
        if isStrInt(noEdges):
            noEdges = int (self.edgesEntry.get())
            if (noEdges < 0):
                tkMessageBox.showwarning("Warning","Entry for edges is less than 0.")
                return
            if (noEdges < (noNodes-1)):
                tkMessageBox.showwarning("Warning","Entry for edges must be enough for a tree structure. Needs %d." %(noNodes-1))
                return
            if (noEdges > (noNodes*(noNodes-1))/2)  :
                tkMessageBox.showwarning("Warning","Entry for edges provided is more than a complete graph." )
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for edges is not an integer.")
            return
        
        self.initGraph = CG.ChordalGraph(noNodes, noEdges)
        self.InsertionStart = False
        print "=========Deletion Start========="
        self.DeletionStart = True
        #self.dStartMid = timer()
        #self.initGraph.createCompleteGraph()
        
    def onViewCoGClick(self):
        """function to call plotGraph"""
        if self.initGraph.completeGraph:
            self.initGraph.plotGraph(self.initGraph.inputCompleteGraph, 1)
        else:
            tkMessageBox.showwarning("Warning","Create Complete Graph first to view Complete Graph.")
            return
    
    def onCreateTreeClick(self):
        """function to check valid input and to call create Tree"""

        noNodes = self.nodesEntry.get()
        if isStrInt(noNodes):
            noNodes = int (self.nodesEntry.get())
            if (noNodes < 4):
                tkMessageBox.showwarning("Warning","Entry for nodes is less than 4.")
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for nodes is not an integer.")
            return
        
        noEdges = self.edgesEntry.get()
        if isStrInt(noEdges):
            noEdges = int (self.edgesEntry.get())
            if (noEdges < 3):
                tkMessageBox.showwarning("Warning","Entry for edges is less than 3.")
                return
            if (noEdges < (noNodes-1)):
                tkMessageBox.showwarning("Warning","Entry for edges must be enough for a tree structure. Needs %d." %(noNodes-1))
                return
            if (noEdges > (noNodes*(noNodes-1))/2)  :
                tkMessageBox.showwarning("Warning","Entry for edges provided is more than a complete graph." )
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for edges is not an integer.")
            return
        
        self.initGraph = CG.ChordalGraph(noNodes, noEdges)
        self.DeletionStart = False
        print "=========Insertion Start========="
        self.InsertionStart = True
        #self.iStartMid = timer()
        self.initGraph.createTree()
        
    def onViewTreeClick(self):
        """function to call plotGraph"""
        if self.initGraph.chordalTree:
            self.initGraph.plotGraph(self.initGraph.chordalTree, 2)
        else:
            tkMessageBox.showwarning("Warning","Create Tree first to view Tree.")
            return
        
    def onCreateCTClick(self):
        """function to call createCT"""
        if self.DeletionStart:
            self.initGraph.createCT(self.initGraph.completeGraph) ###
            self.CGDelete = True
        elif self.InsertionStart:
            self.initGraph.createCT(self.initGraph.chordalTree) ###
            self.CGInsert = True
        else:
            tkMessageBox.showwarning("Warning","Create Complete Graph/Tree first before create Clique Tree.")
            return
        
    def onViewCTClick(self):
        """function to call plotGraph"""
        if self.initGraph.cliqueTree:
            self.initGraph.plotGraph(self.initGraph.cliqueTree, 3)
        else:
            tkMessageBox.showwarning("Warning","Create Weighted Clique Graph first to view Clique Tree.")
            return
    
    def onCreateCGClick(self):
        """function to call createCG"""
        if self.initGraph.cliqueTree:
            if self.DeletionStart and self.CGDelete:
                self.initGraph.createCGByDeletion()
                self.initGraph.dfsCaller()
                self.initGraph.rip()
                #self.dEndMid = timer()
                #print "=========>Time elapsed for Deletion is: "+str(self.dEndMid-self.dStartMid)
            elif self.InsertionStart and self.CGInsert:
                self.initGraph.createCGByInsertion()
                self.initGraph.dfsCaller()
                self.initGraph.rip()
                #self.iEndMid = timer()
                #print "=========>Time elapsed for Insertion is: "+str(self.iEndMid-self.iStartMid)
            self.initGraph.printInfo(self.initGraph.chordalGraph)
        else:
            tkMessageBox.showwarning("Warning","Create Clique Tree before create Chordal Graph.")
            return
    
    def onViewCGClick(self):
        """function to call plotGraph"""
        if self.CGDelete or self.CGInsert:
            self.initGraph.plotGraph(self.initGraph.chordalGraph, 4)
        else:
            tkMessageBox.showwarning("Warning","Create Chordal Graph first to view Chordal Graph.")
            return
    
def center(toplevel):
    """function to compute the center of the screen and place the window in the center"""
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

if __name__ == "__main__":
    """main function which is the starting point of this chordal graph generation technique"""
    app = gui_tk(None)
    app.title("Chordal Graph (CG) Generation (Unified Way)")  
    app.geometry('280x220')#window size
    center(app)
    app.mainloop()
    app.quit()
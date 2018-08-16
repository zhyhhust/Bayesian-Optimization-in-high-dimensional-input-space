import numpy as np
import copy
import math
import pandas as pd
PI=3.1416
class Score(object):
    '''
    Note that this function is to calculate the score, which is known as 
    the objective function in this task, the function is black-box function.
    '''
    def __init__(self):
        self.score=0
        self.RSRPThre=-105
        self.SINRThre=3
        self.RSRPLambda=2
        self.SINRLambda=2
        self.gridFile='Huawei/GridList.txt'
        self.cellFile='Huawei/cellList.txt'
        self.gridCellMRFile='Huawei/GridCellRSRP.xlsx'
        self.cellIDFile='Huawei/cellIDList.txt'
        self.cellList=dict()
        self.gridList=dict()
        self.gridCellLossList=dict()
        self.gridCellRSRPList=dict()
        self.gridCellNewRSRPList=dict()
        self.gridNewRSRPList=dict()
        self.gridNewSINRList=dict()
        self.cellAntennaGainList=dict()
        self.cellIdList=[]
        self.paraType=['ElectricalTilt','RS Power','MechanicalTilt','Azimuth']
        self. Init()
    def InitGridCellInfo(self):
        for key,value in self.gridList.items():
            self.gridCellRSRPList[key]=dict()
            self.gridCellLossList[key]=dict()
            self.gridCellNewRSRPList[key]=dict()
    def GetGridList(self,filename):
        for a in open(filename,'r'):
            grid=dict()
            gridID=''
            a=a[:-2]
            A=a.split(',')
            for i in A:
                b = i.split(':')
                key = b[0]
                try:
                    value = b[1]
                except:
                    continue
                if key=='ID':
                    gridID=value
                else:
                    grid[key]=value
            self.gridList[gridID]=grid
    def GetCellList(self,filename):
        fp=open(filename,'r')
        for a in fp.readlines():
            cellID=''
            cell=dict()
            a=a[:-2]
            A=a.split(',')
            for i in A:
                b = i.split(':')
                key = b[0]
                try:
                    value = b[1]
                except:
                    continue
                if key=='ID':
                    cellID=value
                else:
                    cell[key]=value
            self.cellList[cellID]=cell
    def GetCellIdList(self,filename):
         for line in open(filename,'r'):
            line= line.strip('\r\n')
            self.cellIdList.append(line)
    def RecoverCellList(self,paraList):
        for i in range(len(paraList)):
            self.cellList[self.cellIdList[int(i/4)]][self.paraType[i%4]]=paraList[i]
    def GetCellAntennaGainList(self):
        for key,value in self.cellList.items():
            filename='Huawei/'+value['AntennaModel']+'.txt'
            type=0
            cellAntennaGain=dict()
            antennaH=[]
            antennaV=[]
            for a in open(filename,'r'):
                a.strip()
                if 'HORIZONTAL' in a or 'VERTICAL' in a:
                    type+=1
                elif type==0 and 'GAIN' in a:
                    #print a
                    x,y,z=a.split(' ')
                    cellAntennaGain['Gain']=float(y)
                elif type==1:
                    x,y=a.split(' ')
                    antennaH.append(float(y))
                elif type==2:
                    #print a
                    x,y=a.split(' ')
                    antennaV.append(float(y))
            cellAntennaGain['H']=antennaH
            cellAntennaGain['V']=antennaV
            self.cellAntennaGainList[key]=cellAntennaGain
    def GetEarthAzimuth(self,gridLon,gridLat,cellLon,cellLat):
        dx=float(gridLon)-float(cellLon)
        dy=float(gridLat)-float(cellLat)
        earthAzimuth=0
        if dy==0:
            if dx>=0:
                earthAzimuth=PI/2
            else:
                earthAzimuth=PI*3/2
        elif dx>=0 and dy>0:
            earthAzimuth=math.atan(abs(dx/dy))
        elif dx>=0 and dy<0:
            earthAzimuth=PI-math.atan(abs(dx/dy))
        elif dx<0 and dy<0:
            earthAzimuth=PI+math.atan(abs(dx/dy))
        else:
            earthAzimuth=2*PI-math.atan(abs(dx/dy))
        return earthAzimuth
    def GetEarthTile(self,gridLon,gridLat,cellLon,cellLat,cellHeight):
        dx=float(gridLon)-float(cellLon)
        dy=float(gridLat)-float(cellLat)
        ddx=dx*111000*math.cos(float(gridLat)*math.pi/180)
        ddy=dy*111000
        dis=math.sqrt(ddx*ddx+ddy*ddy)
        earthTile=math.atan(float(cellHeight)/dis)
        return earthTile
    def CalcH(self,cellID,x):
        mmin=int(x)
        mmax=mmin+1
        minx=(mmin+360)%360
        maxx=(mmax+360)%360
        return self.cellAntennaGainList[cellID]['Gain']-(self.cellAntennaGainList[cellID]['H'][minx]*(mmax-x)+self.cellAntennaGainList[cellID]['H'][maxx]*(x-mmin))
    def CalcV(self,cellID,x):
        
        #len1 =len(self.cellList[cellID]['ElectricalTilt'])
        #if len1 !=1:
        #    pdb.set_trace()
        try:
            if x<=90:
                x-=float(self.cellList[cellID]['ElectricalTilt'])
            else:
                x+=float(self.cellList[cellID]['ElectricalTilt'])
        except Exception:
            import pdb
            pdb.set_trace()
            
        mmin=int(x)
        mmax=mmin+1
        minx=(mmin+360)%360
        maxx=(mmax+360)%360
        return self.cellAntennaGainList[cellID]['Gain']-(self.cellAntennaGainList[cellID]['V'][minx]*(mmax-x)+self.cellAntennaGainList[cellID]['V'][maxx]*(x-mmin))
    def GetGridCellAntennaGain(self,cellID,gridID):
        aTX=self.cellList[cellID]['Azimuth']
        eTX=self.cellList[cellID]['MechanicalTilt']
        aRX=self.GetEarthAzimuth(self.gridList[gridID]['Longitude'], self.gridList[gridID]['Latitude'], self.cellList[cellID]['Longitude'], self.cellList[cellID]['Latitude'])
        eRX=self.GetEarthTile(self.gridList[gridID]['Longitude'], self.gridList[gridID]['Latitude'], self.cellList[cellID]['Longitude'], self.cellList[cellID]['Latitude'], self.cellList[cellID]['AntennaHeight'])
        aTX=float(aTX)*math.pi/180
        eTX=float(eTX)*math.pi/180
        aRX=float(aRX)
        eRX=float(eRX)
        if aRX==aTX:
            az=0
            el=eRX-eTX
        else:
            az=math.atan(1/(math.cos(eTX)/math.tan(aRX-aTX)+math.sin(eTX)*math.tan(eRX)/math.sin(aRX-aTX)))
            el=math.atan(math.sin(az)*(math.cos(eTX)*math.tan(eRX)/math.sin(aRX-aTX)-math.sin(eTX)/math.tan(aRX-aTX)))
        if math.sin(az)*math.sin(aRX-aTX)<0:
            az+=PI
        az=az*180/PI
        el=el*180/PI
        if az>180:
            az-=360
        gain=self.CalcH(cellID, az)-((180-math.fabs(az))/180*(self.CalcH(cellID, 0)-self.CalcV(cellID, el))+math.fabs(az)/180*(self.CalcH(cellID, 180)-self.CalcV(cellID, 180-el)))
        #gain+=self.cellAntennaGainList[cellID]['Gain']-max(self.cellAntennaGainList[cellID]['H'])
        return gain
    def GetGridCellRSRP(self,filename):
        data=pd.read_excel(filename,sheetname=0)
        for i in range(len(data)):
            #if self.gridCellRSRPList.has_key(data['GridID'][i]):
            if data['GridID'][i] in self.gridCellRSRPList:
                self.gridCellRSRPList[data['GridID'][i]][data['CellID'][i]]=data['TotalRSRP'][i]
            else:
                cellRSRP=dict()
                cellRSRP[data['CellID'][i]]=data['TotalRSRP'][i]
                self.gridCellRSRPList[data['GridID'][i]]=cellRSRP
    def GetGridCellLoss(self):
        for gridID,cellRSRPList in self.gridCellRSRPList.items():
            for cellID,cellRSRP in cellRSRPList.items():
                cellID=str(cellID)
                cellGain=self.GetGridCellAntennaGain(cellID, gridID)
                loss=float(self.cellList[cellID]['RS Power'])+cellGain-float(cellRSRP)
                #if self.gridCellLossList.has_key(gridID):
                if gridID in self.gridCellLossList:
                    self.gridCellLossList[gridID][cellID]=loss
                else:
                    cellLoss=dict()
                    cellLoss[cellID]=loss
                    self.gridCellLossList[gridID]=cellLoss
    def GetGridCellNewRSRP(self): 
        for gridID,cellLossList in self.gridCellLossList.items():
            for cellID,cellLoss in cellLossList.items():
                cellGain=self.GetGridCellAntennaGain(cellID, gridID)
                RSRP=float(self.cellList[cellID]['RS Power'])+cellGain-float(cellLoss)
                #if self.gridCellNewRSRPList.has_key(gridID):
                if gridID in self.gridCellNewRSRPList:
                    self.gridCellNewRSRPList[gridID][cellID]=RSRP
                else:
                    cellNewRSRP=dict()
                    cellNewRSRP[cellID]=RSRP
                    self.gridCellNewRSRPList[gridID]=cellNewRSRP
    def GetGridNewRSRP(self):
        for gridID,cellRSRPList in self.gridCellNewRSRPList.items():
            self.gridNewRSRPList[gridID]=max(cellRSRPList.values())
    def GetGridNewSINR(self):
        for gridID,cellRSRPList in self.gridCellNewRSRPList.items():
            #maxKey=max(cellRSRPList,key=cellRSRPList.get())
            maxRSRP=max(cellRSRPList.values())
            secRSRP=math.pow(10,-125.0/10)-math.pow(10,float(maxRSRP)/10)
            for cellID,cellRSRP in cellRSRPList.items():
                secRSRP+=math.pow(10,float(cellRSRP)/10)
            secRSRP=10*math.log10(secRSRP)
            self.gridNewSINRList[gridID]=maxRSRP-secRSRP
    def GetScore(self):
        sumMRNum=0
        for gridID,grid in self.gridList.items():
            sumMRNum+=int(grid['TotalMRCount'])
            self.score+=int(grid['TotalMRCount'])*(0.5/(1+math.exp(-self.RSRPLambda*(self.gridNewRSRPList[gridID]-self.RSRPThre)))+0.5/(1+math.exp(-self.SINRLambda*(self.gridNewSINRList[gridID]-self.SINRThre))))
        self.score/=sumMRNum
    #def CalcScore(self,paraList):
    def CalcScore(self,paraList):
        #import pdb
        paraList=np.array(paraList).reshape(112,)
        #pdb.set_trace()
        self.RecoverCellList(paraList)
        self.GetGridCellNewRSRP()
        self.GetGridNewRSRP()
        self.GetGridNewSINR()
        self.GetScore()
        return self.score
    def Init(self):
        self.GetGridList(self.gridFile)
        self.GetCellList(self.cellFile)
        self.GetGridCellRSRP(self.gridCellMRFile)
        self.GetCellIdList(self.cellIDFile)
        self.GetCellAntennaGainList()
        self.GetGridCellLoss()
    def CulDiff(self,paralist,paranum):
        paralistup=copy.deepcopy(paralist)
        paralistdown=copy.deepcopy(paralist)
        paralistup[paranum]+=0.1
        paralistdown[paranum]-=0.1
        valueup=self.CalcScore(paralistup)
        valuedown=self.CalcScore(paralistdown)
        return (valueup-valuedown)/2/0.1
if __name__=='__main__':
    score=Score()
    score.Init()
    test=[0]*112
    print (score.CalcScore(test))  
    print (score.CulDiff(test,2))         

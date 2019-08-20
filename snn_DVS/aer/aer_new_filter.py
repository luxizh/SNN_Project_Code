import struct
#from PIL import Image
import math
import numpy as np
import scipy.io as sio
import os, time
import matplotlib.pyplot as plt
from matplotlib import cm
import cPickle

#/Users/luxi/Desktop/ic/project/SNN_DVS_un/aer_recored
readfold='SNN_DVS_un/aer_recored/'#Mul6_8_2/'
readfold='SNN_DVS_un/aer_recored/record_8_18/'
#savefold='SNN_DVS_un/aermat/'
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
#                               MY AEDAT OBJECT CLASS
#
#  Paer library developed by Dario not working --> ValueError: invalid literal for int() with base 16 when trying to 
#  read some of the recording files (problem with jAER that adds new line and incorrect time-stamps)
#                paer lib: https://github.com/darioml/python-aer
#
#     --> Created my own (simpler) set of functions to read and use Address-Event Representation (AER) data in python
#  
#  AER data --> .aedat extention (recorded using DVS and jAER)
#  Dario: class aedata and class aefile; why two classes ?
#  Faustine: I made only one class (aedatObj) with more attributes and the methods needed to preprocess the data. 
#            load_data inspired from loadaerdat.py (https://github.com/SensorsINI/processAEDAT/tree/master/jAER_utils)
#            Other source of inspiration: https://github.com/GergelyBoldogkoi/SpinVision/tree/master/SpinVision 
#            Still wondering if I should use Matlab files (.mat) or AER files (.aedat) as input for the neural network
#            PROBABLY .MAT: CONVERSION TO ARRAYS REQUIRED; DONE ONCE AT BEGINNING --> FILE SAVED --> AVOIDS TO DO
#  CONVERSION EVERY TIME THE SIMU IS RUN...  
#
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

"""
obj := class aedatObj
data := {'filename': self.filename, 'x': self.x, 'y': self.y, 'pol': self.pol, 'ts': self.ts, 'dim': self.dim} : associative array (dictionary) --> useful to save to mat
mat --> +/- like data
"""

class aedatObj(object):
    obj_list = [] # class attibute (instead of instance attribute) --> list of aedatObj 
    data_list = [] # list of data

    def __init__(self, filename=None, max_events=1e6):
        self.max_events = max_events # always < 60 000 in my recordings
        self.td = 0.000001  # timestep is 1us
        if filename == None:
            self.filename = 'new_obj_not_from_file' # could leave it to None
            self.x, self.y, self.pol, self.ts = np.array([]), np.array([]), np.array([]), np.array([])
            self.video_t = 0 
            self.header = ''
            self.dim = (0,0)
        else:
            self.filename = filename[0:-6]
            self.x, self.y, self.pol, self.ts, self.video_t, self.header = self.load_data()
            self.dim = (128,128)
        # obj/data in list not modified when real obj modified --> pointeur ?
        # only add obj created from file? 
        if len(self.ts) > 0: # don't add empty obj (ex temporary obj in fct)
            aedatObj.obj_list.append(self)
            aedatObj.data_list.append({'filename': self.filename, 'x': self.x, 'y': self.y, 'pol': self.pol, 'ts': self.ts, 'dim': self.dim})
        
        
    def load_data(self, debug=1):
        """    
        load AER data file and parse these properties of AE events:
        - timestamps (in us), 
        - x,y-position [0..127]
        - polarity (0/1)
        @param debug - 0 = silent, 1 (default) = print summary, >=2 = print all debug
        @return (xaddr, yaddr, pol, timestamps, video_duration, header) 
                --> 4 lists containing data of all events, 1 float of video duration, 1 string for the header
        """
      # constants
        aeLen = 8  # 1 AE event takes 8 bytes
        readMode = '>II'  # struct.unpack(), 2x ulong, 4B+4B
           
    
        xmask = 0x00fe
        xshift = 1
        ymask = 0x7f00
        yshift = 8
        pmask = 0x1
        pshift = 0
        ###################################
        #y x p?
        xmask = 0x00fe
        xshift = 1
        ymask = 0x7f00
        yshift = 8
        pmask = 0x1
        pshift = 0

        datafile = self.filename+'.aedat'
    
        aerdatafh = open(readfold+datafile, 'rb')
        k = 0  # line number
        p = 0  # pointer, position on bytes
        statinfo = os.stat(readfold+datafile)
        length = statinfo.st_size    
        print ("file size", length)
        #######################################
        #print file size?
    
        # header
        lt = aerdatafh.readline()
        header = ''
        while lt and lt[0] == "#":
            p += len(lt)
            k += 1
            lt = aerdatafh.readline() 
            header = header + str(lt) + '\n'
            if debug >= 2:
                #print (str(lt))
                #error utf-8 print str problem
                pass
            continue
        ###############################
        #wait to see debug change
        #multiple line header
        
        header = str(lt)

        # variables to parse
        timestamps = []#np.array([])
        xaddr = []#np.array([])
        yaddr = []#np.array([])
        pol = []#np.array([])
        ######################
        #what is pol?-on-1 off-0 polar
    
        # read data-part of file
        aerdatafh.seek(p)
        s = aerdatafh.read(aeLen)
        #print type(s)
        p += aeLen
    
        print (xmask, xshift, ymask, yshift, pmask, pshift)  

        while p < length:
            addr, ts = struct.unpack(readMode, s)# s char 1 byte
            #print type(addr)
            #print('%#x'%addr)
            x_addr = (addr & xmask) >> xshift
            y_addr = (addr & ymask) >> yshift
            a_pol = (addr & pmask) >> pshift

            if debug >= 2: 
                print("ts->", ts) 
                print("x-> ", x_addr)
                print("y-> ", y_addr)
                print("pol->", a_pol)

            timestamps.append(ts)
            xaddr.append(x_addr)
            yaddr.append(y_addr)
            pol.append(a_pol)
            #np array catch
                  
            aerdatafh.seek(p)
            s = aerdatafh.read(aeLen)
            p += aeLen        

        video_duration = (timestamps[-1] - timestamps[0]) * self.td#time duration

        if debug > 0:
            try:
                print 'file name =', self.filename
                print ("read %i (~ %.2fM) AE events, duration= %.2fs" % (len(timestamps), len(timestamps) / float(10 ** 6), (timestamps[-1] - timestamps[0]) * self.td))
                n = 5
                print ("showing first %i:" % (n))
                print ("timestamps: %s \nX-addr: %s\nY-addr: %s\npolarity: %s" % (timestamps[0:n], xaddr[0:n], yaddr[0:n], pol[0:n]))
            except:
                print ("failed to print statistics")

        return (np.array(xaddr,dtype=np.int8), np.array(yaddr,dtype=np.int8), np.array(pol,dtype=np.int8), 
                np.array(timestamps,dtype=np.int64), video_duration, header)
 
    def save_object(self,save_filename=None):
        savefold='SNN_DVS_un/aerobj/'
        if save_filename == None:
            save_filename = self.filename
        output=open(savefold+save_filename+'.pkl','wb')
        cPickle.dump(self,output,-1)
        output.close()

    def save_object_r(self,save_filename=None):
        savefold='SNN_DVS_un/aerobj_r/'
        if save_filename == None:
            save_filename = self.filename
        output=open(savefold+save_filename+'.pkl','wb')
        cPickle.dump(self,output)
        output.close()

    def save_to_mat(self, mat_filename=None): # mat_filename=self.filename[0:3] not possible --> set default arg to None and define inside
        """    
        save the aedatObj as a .mat file
        --> all attributes are saved
        @param mat_filename - if None, save new .mat file with the same name as .aedat file
        """
        savefold='SNN_DVS_un/aermat/'
        if mat_filename == None:
            mat_filename = self.filename
        sio.savemat(savefold+mat_filename, {'filename': mat_filename, 'x': self.x, 'y': self.y, 'pol': self.pol, 'ts': self.ts, \
        'video_t': self.video_t, 'header': self.header, 'dim': self.dim, 'max_events': self.max_events}) # save all attributes?
        # filename[0:3] --> name = 1-1.mat and not 1-1.aedat.mat
        # remember in python index starts at 0 and in [start:end], idx start is included but end is not
    

    # From G - but does not produce anything (YET)
    #############################
    #want to show what????????
    def interactive_animation(self, step=5000, limits=(0,128), pause=0):
        plt.ion()
        fig = plt.figure(figsize=(6,6))
        plt.show()
        ax = fig.add_subplot(111)

        start = 0
        end = step-1
        while(start < len(self.x)):
            ax.clear()
            ax.scatter(self.x[start:end], self.y[start:end], s = 20, c = self.pol[start:end], marker = 'o') #, cmap = cm.jet )
            ax.set_xlim(limits)
            ax.set_ylim(limits)
            start += step
            end += step
            plt.draw()
            time.sleep(pause)
            plt.show() #added by F


    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #                           DATA PRE-PROCESSING
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def simple_process(self,new_dim=(32,32),pos_red=4,time_red=1000,th=9):
        assert self.dim[0]%new_dim[0] is 0
        assert self.dim[1]%new_dim[1] is 0

        d_ts = np.floor(self.ts/time_red)
        d_ts=d_ts-d_ts[0]+1
        #start form 1
        d_x = np.floor(self.x/(self.dim[0] / new_dim[0]))
        d_y = np.floor(self.y/(self.dim[1] / new_dim[1]))
        rtn_ts=[]
        rtn_x=[]
        rtn_y=[]
        #d_pol = self.pol
        spikes=[[] for i in range(new_dim[0]*new_dim[1])]

        p_ts=d_ts[0]
        #start_ts=d_ts[0]
        count_on=np.zeros(new_dim,dtype=np.int8)
        for i in range(len(d_ts)):
            c_ts=d_ts[i]
            if c_ts==p_ts:
                if self.pol[i]==0:
                    count_on[int(d_x[i]),int(d_y[i])]+=1
            else:
                on_ind=np.where(count_on>=th)
                for j in range(len(on_ind[0])):
                    rtn_ts.append(p_ts)
                    rtn_x.append(on_ind[0][j])
                    rtn_y.append(on_ind[1][j])
                    #print(on_ind[0][j]*new_dim[0]+on_ind[1][j])
                    (spikes[(on_ind[0][j]*new_dim[0]+on_ind[1][j])]).append(p_ts)
                p_ts=c_ts
                count_on=np.zeros(new_dim,dtype=np.int8)
        on_ind=np.where(count_on>=th)
        for j in range(len(on_ind[0])):
            rtn_ts.append(p_ts)
            rtn_x.append(on_ind[0][j])
            rtn_y.append(on_ind[1][j])
            spikes[on_ind[0][j]*new_dim[0]+on_ind[1][j]].append(p_ts)

        rtn = aedatObj()
        rtn.dim=new_dim
        rtn.td=self.td*time_red
        rtn.filename = self.filename + '_sp_'+str(new_dim[0])
        rtn.video_t = self.video_t
        rtn.pol=np.zeros((1,len(rtn_ts)),dtype=np.int8)
        rtn.ts=np.array(rtn_ts,dtype=np.int64)
        rtn.x=np.array(rtn_x,dtype=np.int8)
        rtn.y=np.array(rtn_y,dtype=np.int8)
        return rtn,spikes

    def downsample(self, new_dim=(32,32)):
        """    
        downsample aedatObj--> reduce resolution
        @param new_dim - new desired dimensions 
        @return rtn - new aedatObj with lower resolution
        """
        # TODO
        # Make this cleaner
        assert self.dim[0]%new_dim[0] is 0
        assert self.dim[1]%new_dim[1] is 0

        rtn = aedatObj() 

        rtn.filename = self.filename + '_'+str(new_dim[0]) #
        rtn.ts = self.ts# is it suitable to change ts -->ts/1000
        rtn.pol = self.pol
        rtn.video_t = self.video_t
        rtn.x = np.floor(self.x / (self.dim[0] / new_dim[0]))
        rtn.y = np.floor(self.y / (self.dim[1] / new_dim[1]))
        rtn.dim = (new_dim[0], new_dim[1])
        rtn.header = 'Downsample of file ' + self.filename + ' to dim = ' + str(new_dim[0])

        return rtn


    def filter_noise(self, windowSize=3, threshold=12, exposureTime_ms=20): # from Gergely
        """    
        filter noise out aedatObj: keep only events concerning rolling ball
            --> square mask of size (windowSize, windowSize) moved across entire "frame" (128,128)
                at each step, counts number of ON and OFF events falling within the mask during a given time (exposureTime)
                if number of events reaches threshold, middle pixel is set to ON or OFF event
        @param windowSize - mask size (default=2)
        @param threshold - minimum number of events within mask and time required to keep the spike (default=12)
        @param exposureTime_ms - duration considered as same "time unit" (default=20)
        
        @return rtn - new aedatObj with noise filtered out
        """
        # this function converts all events into ON events
        # Gergely:  windowSiwze = 5
        #           threshold = 13 (empirically determined)
        #           exposureTime_ms = 20 (DVS exposure time)
        # Faustine: windowSiwze = 2 
        #           threshold = 12 (empirically determined)
        #           exposureTime_ms = 20 (DVS exposure time) 

        # TODO
        # Create different modes (pol_type) and compare in learning: 
        #   - all converted to ON 
        #   - only ON / (only OFF) 
        #   - keep ON and OFF --> this one reauires 2x more connections in first layer
        # Optimize
        # TODO problem
        # delete multiple repeat event ->time solt? or time slot downsampling
        # it is in ts sequence, so can find repeat event
        new_ts = []
        new_x = []
        new_y = []
        new_pol = []
        exposureTime_us = exposureTime_ms * 1000

        for i in range(len(self.ts)):
            #find all events within plus-minus expTime
            # compare their x,y values, then if there are more than 4 in a 4x4 window, produce an output spike.
            #eventCounter = 0
            ONcounter = 0
            #OFFcounter = 0
            #go down
            j = i
            while(j >= 0 and abs(self.ts[j] - self.ts[i]) < exposureTime_us):
                #ignore polarity of data for now
                xdiff = abs(self.x[j] - self.x[i])
                ydiff = abs(self.y[j] - self.y[i])
                if xdiff <= windowSize and ydiff <= windowSize:
                    #eventCounter += 1
                    if(self.pol[j]):
                        OFFcounter += 1
                    #else:
                    #    ONcounter += 1
                j -= 1
                
            #go up
            k = i + 1
            while (k < len(self.ts) and abs(self.ts[k] - self.ts[i]) < exposureTime_us):
                # ignore polarity of data for now
                xdiff = abs(self.x[k] - self.x[i])
                ydiff = abs(self.y[k] - self.y[i])
                if xdiff <= windowSize and ydiff <= windowSize:
                    #eventCounter += 1
                    if (self.pol[k]):
                        OFFcounter += 1
                    #else:
                    #    ONcounter += 1
                k += 1

            if eventCounter >= threshold:
                new_ts.append(self.ts[i])
                new_x.append(self.x[i])
                new_y.append(self.y[i])
                if OFFcounter > ONcounter:
                    new_pol.append(1) # Add OFF event
                else:
                    new_pol.append(0) # Add ON event

        rtn = aedatObj()

        rtn.filename = self.filename + '_filtered'
        rtn.ts = np.array(new_ts,dtype=np.int8)
        rtn.x = np.array(new_x,dtype=np.int8)
        rtn.y = np.array(new_y,dtype=np.int8)
        rtn.pol = np.array(new_pol,dtype=np.int8)
        rtn.video_t = self.video_t
        rtn.dim = self.dim
        rtn.header = 'Filtered file ' + self.filename + ' \n Threshold = ' + str(threshold) + ' \n Window size = (' + \
                    str(windowSize) +', ' + str(windowSize) + ' \n Exposure time = ' + str(exposureTime_ms) + ' ms'

        return rtn

#AerTest=aedatObj(filename="mul6_fast_1.aedat")
'''
AerRaw=aedatObj(filename="single3_1.aedat")
#AerRAW.save_to_mat()
#AerRaw.save_object()
AerSp,spikes=AerRaw.simple_process()
#AerSp.save_object()
#AerSp.save_to_mat()

savefold='SNN_DVS_un/aerobj/'
output=open(savefold+AerSp.filename+'_spikes.pkl','wb')
cPickle.dump(spikes,output,-1)
sio.savemat(savefold+AerSp.filename+'_spikes', {'spikes': spikes})
output.close()
'''
'''
AerTest=aedatObj(filename="mul6_mid_5.aedat")
AerTest.save_to_mat()
After_down=AerTest.downsample()
After_filter=After_down.filter_noise()
After_filter.save_to_mat()
'''
'''
loadf=open('SNN_DVS_un/aerpkl/mul6_mid_6.pkl','rb')
load_Aer=cPickle.load(loadf)
a=load_Aer.simple_process()
a.save_object()
'''
'''
a=[[]]*5
a[0].append(3)
print a
b=[[],[],[],[]]
b[0].append(3)
print(b)
'''




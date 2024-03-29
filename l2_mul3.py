import pyNN.spiNNaker as sim
import numpy as np
import math
import random
from pyNN.random import NumpyRNG, RandomDistribution
import pyNN.utility.plotting as pplt
import matplotlib.pyplot as plt
import cPickle
import sys
sys.path.append("/Users/luxi/Desktop/ic/project/SNN_DVS_un/SNN_Project_Code/snn_DVS/aer")
from aer_new_filter import aedatObj

#trylabel=53
trylabel=1
#def parameters
__delay__ = 1#0.250 # (ms) 
tauPlus = 25#25 #20 # 15 # 16.8 from literature
tauMinus = 15# #20 # 30 # 33.7 from literature
aPlus = 0.200  #tum 0.016 #9 #3 #0.5 # 0.03 from literature
aMinus = 0.100 #255 #tum 0.012 #2.55 #2.55 #05 #0.5 # 0.0255 (=0.03*0.85) from literature 
wMax = 1.5 #1 # G: 0.15 1
wMaxInit = 0.4#0.5#0.1#0.100
wMin = 0
nbIter = 5
testWeightFactor = 1#0.05177
x = 3 # no supervision for x first traj presentations
y = 0# for inside testing of traj to see if it has been learned /!\ stdp not disabled

input_len=32#y 30
input_class=32#x 3
input_size=input_len*input_class
output_size=9
inhibWeight = -1
stimWeight = 20

v_co=1

cell_params_lif = {'cm': 1,#70
                   'i_offset': 0.0,
                   'tau_m': 20.0,#20
                   'tau_refrac': 20.0,#2 more that t inhibit#10
                   'tau_syn_E': 2.0,#2
                   'tau_syn_I': 10.0,#5
                   'v_reset': -70.0,
                   'v_rest': -65.0,
                   'v_thresh': -55.0
                   }

def generate_data():
    spikesTrain=[]
    organisedData = {}
    for i in range(input_class):
        for j in range(input_len):
            neuid=(i,j)
            organisedData[neuid]=[]
    for i in range(input_len):
        for j in range(output_size):
            neuid=(j,i)
            organisedData[neuid].append(j*input_len*v_co*5+i*v_co)
            organisedData[neuid].append(j*input_len*v_co*5+input_len*v_co*1+i*v_co)
            organisedData[neuid].append(j*input_len*v_co*5+input_len*v_co*2+i*v_co)
            organisedData[neuid].append(j*input_len*v_co*5+input_len*v_co*3+i*v_co)
            organisedData[neuid].append(j*input_len*v_co*5+input_len*v_co*4+i*v_co)
            organisedData[neuid].append(input_len*v_co*(3*5+j)+i*v_co)

        #organisedData[neuid].append(i*v_co+2)

#        if neuid not in organisedData:
#            organisedData[neuid]=[i*v_co]
#        else:
#            organisedData[neuid].append(i*v_co)
    for i in range(input_class):
        for j in range(input_len):
            neuid=(i,j)
            organisedData[neuid].sort()
            spikesTrain.append(organisedData[neuid])

    runTime = int(max(max(spikesTrain)))
    sim.setup(timestep=1)
    
    noise=sim.Population(input_size,sim.SpikeSourcePoisson(),label='noise')

    
    noise.record(['spikes'])#noise
    
    sim.run(runTime)
    neonoise= noise.get_data(["spikes"])
    spikesnoise = neonoise.segments[0].spiketrains#noise
    sim.end()
    for i in range(input_size):
        for noisespike in spikesnoise[i]:
            spikesTrain[i].append(noisespike)
            spikesTrain[i].sort()
    return spikesTrain
'''    
    for neuronSpikes in organisedData.values():
        neuronSpikes.sort()
        spikesTrain.append(neuronSpikes)
'''
    

def train(spikeTimes,untrained_weights=None):
    organisedStim = {}
    labelSpikes = []
    #spikeTimes = generate_data()

    for i in range(output_size):
        labelSpikes.append([])
        labelSpikes[i] = [i*input_len*v_co*5+(input_len-1)*v_co+1,
                            i*input_len*v_co*5+(input_len-1)*v_co*2+1,
                            i*input_len*v_co*5+(input_len-1)*v_co*3+1]
        #for j in range(5):
        #    labelSpikes
        
    #labelSpikes[label] = [(input_len-1)*v_co+1,(input_len-1)*v_co*2+1,(input_len-1)*v_co*3+1,]
    
    
    if untrained_weights == None:
        untrained_weights = RandomDistribution('uniform', low=wMin, high=wMaxInit).next(input_size*output_size)
        #untrained_weights = RandomDistribution('normal_clipped', mu=0.1, sigma=0.05, low=wMin, high=wMaxInit).next(input_size*output_size)
        untrained_weights = np.around(untrained_weights, 3)
        #saveWeights(untrained_weights, 'untrained_weightssupmodel1traj')
        print ("init!")

    print "length untrained_weights :", len(untrained_weights)

    if len(untrained_weights)>input_size:
        training_weights = [[0 for j in range(output_size)] for i in range(input_size)] #np array? size 1024x25
        k=0
        for i in range(input_size):
            for j in range(output_size):
                training_weights[i][j] = untrained_weights[k]
                k += 1
    else:
        training_weights = untrained_weights

    connections = []
    for n_pre in range(input_size): # len(untrained_weights) = input_size
        for n_post in range(output_size): # len(untrained_weight[0]) = output_size; 0 or any n_pre
            connections.append((n_pre, n_post, training_weights[n_pre][n_post], __delay__)) #index
    runTime = int(max(max(spikeTimes/2)))+100
    #####################
    sim.setup(timestep=1)
    #def populations
    layer1=sim.Population(input_size,sim.SpikeSourceArray, {'spike_times': spikeTimes},label='inputspikes')
    layer2=sim.Population(output_size,sim.IF_curr_exp,cellparams=cell_params_lif,label='outputspikes')
    #supsignal=sim.Population(output_size,sim.SpikeSourceArray, {'spike_times': labelSpikes},label='supersignal')

    #def learning rule
    stdp = sim.STDPMechanism(
                            weight=untrained_weights,
                            #weight=0.02,  # this is the initial value of the weight
                            #delay="0.2 + 0.01*d",
                            timing_dependence=sim.SpikePairRule(tau_plus=tauPlus, tau_minus=tauMinus,A_plus=aPlus, A_minus=aMinus),
                            #weight_dependence=sim.MultiplicativeWeightDependence(w_min=wMin, w_max=wMax),
                            weight_dependence=sim.AdditiveWeightDependence(w_min=wMin, w_max=wMax),
                            #weight_dependence=sim.AdditiveWeightDependence(w_min=0, w_max=0.4),
                            dendritic_delay_fraction=1.0)
    #def projections

    #stdp_proj = sim.Projection(layer1, layer2, sim.FromListConnector(connections), synapse_type=stdp)
    stdp_proj = sim.Projection(layer1, layer2, sim.AllToAllConnector(), synapse_type=stdp)
    inhibitory_connections = sim.Projection(layer2, layer2, sim.AllToAllConnector(allow_self_connections=False), 
                                            synapse_type=sim.StaticSynapse(weight=inhibWeight, delay=__delay__), 
                                            receptor_type='inhibitory')
    #stim_proj = sim.Projection(supsignal, layer2, sim.OneToOneConnector(), 
    #                            synapse_type=sim.StaticSynapse(weight=stimWeight, delay=__delay__))
    
    layer1.record(['spikes'])

    layer2.record(['v','spikes'])
    #supsignal.record(['spikes'])
    sim.run(runTime)

    print("Weights:{}".format(stdp_proj.get('weight', 'list')))

    weight_list = [stdp_proj.get('weight', 'list'), stdp_proj.get('weight', format='list', with_address=False)]
    neo = layer2.get_data(["spikes", "v"])
    spikes = neo.segments[0].spiketrains
    v = neo.segments[0].filter(name='v')[0]
    #neostim = supsignal.get_data(["spikes"])
    #spikestim = neostim.segments[0].spiketrains
    neoinput= layer1.get_data(["spikes"])
    spikesinput = neoinput.segments[0].spiketrains

    plt.close('all')
    pplt.Figure(
    pplt.Panel(spikesinput,xticks=True, yticks=True, markersize=2, xlim=(0,runTime),xlabel='(a) Spikes of Input Layer'),
    #pplt.Panel(spikestim, xticks=True, yticks=True, markersize=2, xlim=(0,runTime),xlabel='(c) Spikes of Supervised Layer'),
    pplt.Panel(spikes, xticks=True, xlabel="(b) Spikes of Output Layer", yticks=True, markersize=2, xlim=(0,runTime)),
    pplt.Panel(v, ylabel="Membrane potential (mV)", xticks=True, yticks=True, xlim=(0,runTime),xlabel='(c) Membrane Potential of Output Layer\nTime (ms)'),
    title="Three lanes Training",
    annotations="Three lanes Training"
                ).save('SNN_DVS_un/plot_for_mul3/'+str(trylabel)+'_training.png')
    #plt.hist(weight_list[1], bins=100)
    
    plt.close('all')
    plt.hist([weight_list[1][0:input_size], weight_list[1][input_size:input_size*2], weight_list[1][input_size*2:]], bins=20, label=['neuron 0', 'neuron 1', 'neuron 2'], range=(0, wMax))
    plt.title('weight distribution')
    plt.xlabel('Weight value')
    plt.ylabel('Weight count')
    #plt.show()
    #plt.show()
                
    sim.end()
    return weight_list[1]


def test(spikeTimes,trained_weights):

    #spikeTimes = extractSpikes(sample)
    runTime = int(max(max(spikeTimes)))+100

    ##########################################

    sim.setup(timestep=1)

    pre_pop = sim.Population(input_size, sim.SpikeSourceArray, {'spike_times': spikeTimes}, label="pre_pop")
    post_pop = sim.Population(output_size, sim.IF_curr_exp , cell_params_lif, label="post_pop")
   
    if len(trained_weights) > input_size:
        weigths = [[0 for j in range(output_size)] for i in range(input_size)] #np array? size 1024x25
        k=0
        for i in range(input_size):
            for j in range(output_size):
                weigths[i][j] = trained_weights[k]
                k += 1
    else:
        weigths = trained_weights

    connections = []
    
    #k = 0
    for n_pre in range(input_size): # len(untrained_weights) = input_size
        for n_post in range(output_size): # len(untrained_weight[0]) = output_size; 0 or any n_pre
            #connections.append((n_pre, n_post, weigths[n_pre][n_post]*(wMax), __delay__))
            connections.append((n_pre, n_post, weigths[n_pre][n_post]*(wMax)/max(trained_weights), __delay__)) #
            #k += 1

    prepost_proj = sim.Projection(pre_pop, post_pop, sim.FromListConnector(connections), synapse_type=sim.StaticSynapse(), receptor_type='excitatory') # no more learning !!
    inhib_proj = sim.Projection(post_pop, post_pop, sim.AllToAllConnector(), synapse_type=sim.StaticSynapse(weight=inhibWeight, delay=__delay__), receptor_type='inhibitory')
    # no more lateral inhib
    pre_pop.record(['spikes'])
    post_pop.record(['v', 'spikes'])
    sim.run(runTime)

    neo = post_pop.get_data(['v', 'spikes'])
    spikes = neo.segments[0].spiketrains
    v = neo.segments[0].filter(name='v')[0]
    neoinput= pre_pop.get_data(["spikes"])
    spikesinput = neoinput.segments[0].spiketrains
    
    plt.close('all')
    pplt.Figure(
    # plot voltage 
    
    # raster plot
    pplt.Panel(spikesinput,xticks=True, yticks=True, markersize=2, xlim=(0,runTime),xlabel='(a) Spikes of Input Layer'),
    pplt.Panel(spikes, xlabel="(b) Spikes of Output Layer", xticks=True, yticks=True, markersize=2, xlim=(0, runTime+100)),
    pplt.Panel(v, ylabel="Membrane potential (mV)", xticks=True, yticks=True, xlim=(0, runTime+100),xlabel='(c) Membrane Potential of Output Layer\nTime (ms)'),
    title='Three lanes Test'#,
    #annotations='T'
                ).save('SNN_DVS_un/plot_for_mul3/'+str(trylabel)+'_test1.png')
    #f1.fig.texts=[]
    print("Weights:{}".format(prepost_proj.get('weight', 'list')))

    weight_list = [prepost_proj.get('weight', 'list'), prepost_proj.get('weight', format='list', with_address=False)]
    #predict_label=
    sim.end()
    return spikes

#====================================================
#========some visualization =========================
#====================================================

def plot_weight_reconstruction(neuron_index,weight):
    plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    '''
    ax.set_yticks(range(len(yLabel)))
    ax.set_yticklabels(yLabel, fontproperties=font)
    ax.set_xticks(range(len(xLabel)))
    ax.set_xticklabels(xLabel)
    '''
    #weight=weight.reshape()
    #作图并选择热图的颜色填充风格，这里选择hot
    im = ax.imshow(weight, cmap=plt.cm.gray_r,origin='lower')
    #增加右侧的颜色刻度条
    plt.colorbar(im)
    #增加标题
    plt.title("reconstrucion of neuron"+str(neuron_index))
    #show
    
    plt.savefig('SNN_DVS_un/plot_for_mul3/'+str(trylabel)+'_neuron.png')
    plt.show()
    plt.close('all')
    pass
    return fig

def plot_all_weight_reconstructions(weight,neurons,input_len,input_class,wMax):
    plt.close('all')
    sub_size=int(math.ceil(math.sqrt(neurons)))
    fig,ax= plt.subplots(sub_size,sub_size)
    ax=ax.flatten()
    plt.subplots_adjust(hspace=0.3,wspace=0.1)

    
    #plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None)
    for i in range(neurons):
        #ax = fig.add_subplot(sub_size,sub_size,i+1)
        ax[i].set_title('neuron '+str(i),fontsize=10,fontweight='bold')
        #ax[i].set_xticklabels([0,31])
        ax[i].set_yticks(range(0,input_len,input_len-1))
        ax[i].set_xticks(range(0,input_class,input_class-1))
        ax[i].tick_params(labelsize=8)
        im = ax[i].imshow(weight[:,i].reshape((input_len,-1),order='F'), cmap=plt.cm.gray,vmax=wMax,origin='lower')
    fig.colorbar(im,ax=ax[:])
    fig.suptitle('Reconstrucions',fontweight='bold')
    fig.savefig('SNN_DVS_un/plot_for_mul3/'+str(trylabel)+'_neurons.png')
    plt.show()
    plt.close('all')
    return fig 
    


#==============main================
'''
readfold='SNN_DVS_un/aer_recored/record_8_12/'
AerRaw=aedatObj(filename="mul3_4.aedat")
#AerRAW.save_to_mat()
#AerRaw.save_object()
AerSp,spikes=AerRaw.simple_process(time_red=1000)
AerSp.save_object()
#AerSp.save_to_mat()

savefold='SNN_DVS_un/aerobj_6/'
output=open(savefold+AerSp.filename+'_spikes.pkl','wb')
cPickle.dump(spikes,output,-1)
#sio.savemat(savefold+AerSp.filename+'_spikes', {'spikes': spikes})
output.close()

'''

loadfold='SNN_DVS_un/aerobj_6/'
in_f=open(loadfold+'mul3_2_sp_32_spikes.pkl','rb')
spikes=cPickle.load(in_f)
in_f.close()


weight_list=None
weight_list=train(spikeTimes=spikes,untrained_weights=weight_list)
np.save("SNN_DVS_un/weight/l2_weight_mul3/"+str(trylabel)+".npy",weight_list)

weight_list=np.load("SNN_DVS_un/weight/l2_weight_mul3/"+str(trylabel)+".npy")
neuron_ind=4
weight_re=weight_list.reshape(input_size,-1)
#plot_weight_reconstruction(neuron_ind,(weight_re[:,neuron_ind]).reshape((input_len,-1),order='F'))
plot_all_weight_reconstructions(weight_re,output_size,input_len,input_class,wMax)
#for i in range(10):
#    spikeTimes=generate_data(1)

#np.save("class_result/noiseweight"+str(trylabel)+".npy",weight_list)


'''
loadfold='SNN_DVS_un/aerobj/'
in_f=open(loadfold+'single3_3_sp_32_spikes.pkl','rb')
testspikes=cPickle.load(in_f)
in_f.close()

weight_list=np.load("SNN_DVS_un/weight/l2_weight/"+str(trylabel)+".npy")
test(testspikes,weight_list)


'''
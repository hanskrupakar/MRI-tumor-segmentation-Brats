import glob
import numpy as np
import matplotlib.pyplot as plt

#epoch-patient: 1, 1, iter: 1-200, p%: 0.4592, loss: 2.0885, acc_flair_t2: 54.08%, acc_t1_t1ce: 33.25%

class Averager:
    def __init__(self):
        self.sum = 0
        self.num = 0

    def add(self, no):
        self.sum += no
        self.num += 1

    def get(self):
        return self.sum / float(self.num)
    
class LogFile:
    def __init__(self, fname):
        self.steps = []
        with open(f, 'r') as g:
            l = [x.strip() for x in g.readlines()]
        
        prev_epoch, self.num_steps_per_epoch, self.num_patients, self.max_epochs = 1, 1, 1, 1
        for i, line in enumerate(l):
            if 'epoch-patient' in line:
                ptr = 15
                epoch = int(line[ptr:ptr+4].split(',')[0])
                ptr += len(str(epoch)) + 2
                patient_id = int(line[ptr:ptr+4].split(',')[0])
                ptr += len(str(patient_id)) + 8
                num_patches = int(line[ptr:ptr+8].split('-')[-1].split(',')[0])
                ptr += 8
                prob_pos = float(line[ptr:ptr+8].split(',')[0].split(':')[-1])     
                ptr += 10
                loss = float(line[ptr:ptr+16].split(':')[-1].split(',')[0])
                ptr += 17
                acc_flair_t2 = float(line[ptr:ptr+20].split(':')[-1].split('%')[0])
                ptr += 20
                acc_t1_t1ce = float(line[ptr:].split(':')[-1].split('%')[0])
                
                if prev_epoch < epoch:
                    prev_epoch = np.inf
                    self.num_steps_per_epoch = i
                    self.num_patients = self.prev_patient
                    
                self.prev_patient = patient_id

                self.steps.append({'epoch':epoch,
                                   'patient_id': patient_id,
                                   'prob_pos': prob_pos,
                                   'loss': loss,
                                    'acc_flair_t2': acc_flair_t2,
                                    'acc_t1_t1ce': acc_t1_t1ce,
                                    })
                self.max_epochs = epoch

    def plot_loss_graph(self, fig, ax, fname, vistype='global'):
    # vistype: global and per-patient
    
        if vistype=='global':
            
            losses, loss_acc, flag = [], Averager(), True
            
            for step in self.steps:
                loss_acc.add(step['loss'])
                losses.append(loss_acc.get())
                
                if step['epoch']==1 and flag:
                    flag = False
                    
            ax.plot([i/self.num_steps_per_epoch  for i in range(len(self.steps))], losses, label='%s'%fname.split('.txt')[0].split('log_')[-1])
        else:
            cmap = plt.get_cmap('hsv')
            colors = [cmap(i) for i in np.linspace(0, 1, self.num_patients)] 
            
            accum = [Averager() for _ in range(self.num_patients)]
            
            losses = [[] for _ in range(self.num_patients)]
            for step in self.steps:
                pat_id = step['patient_id']
                accum[pat_id-1].add(step['loss'])
                losses[pat_id-1].append(accum[pat_id-1].get())
                
            for i, (loss, color) in enumerate(zip(losses, colors)):
                ax.plot(np.linspace(0, self.max_epochs+1, len(loss)), loss, color=color, label='Patient %d'%(i))
        
        return fig, ax
    
    def plot_accuracy_graph(self, fig, ax, fname):
        
        t1acc, t2flacc = [], []
        t1_avg, t2_avg = Averager(), Averager()

        for step in self.steps:
            t1_avg.add(step['acc_t1_t1ce'])
            t2_avg.add(step['acc_flair_t2'])

            t1acc.append(t1_avg.get())
            t2flacc.append(t2_avg.get())

        ax.plot([i/self.num_steps_per_epoch  for i in range(len(self.steps))], t1acc, label='T1, T1ce: %s'%fname.split('.txt')[0].split('log_')[-1])
        ax.plot([i/self.num_steps_per_epoch  for i in range(len(self.steps))], t2flacc, label='T2, flair: %s'%fname.split('.txt')[0].split('log_')[-1])
        
        return fig, ax

fig, ax = plt.subplots()

for f in glob.glob("log_*.txt"):
    
    fobj = LogFile(f)

    print fobj.num_steps_per_epoch

    #fig, ax = fobj.plot_accuracy_graph(fig, ax, f)
    fig, ax = fobj.plot_loss_graph(fig, ax, f)
    
    #plt.savefig(f.split('.txt')[0]+'.png', bbox_inches='tight')

plt.legend(loc='best')
plt.xlabel('Number of epochs')
plt.ylabel('DICE Loss')
plt.savefig('loss.png', bbox_inches='tight')

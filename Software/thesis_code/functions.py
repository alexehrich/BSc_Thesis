from unittest import FunctionTestCase
from matplotlib.ft2font import LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import scipy as sp
from scipy import signal



#THIS FUNCTION CORRECT THE LENGTH FROM THE SIGNALS
def correct_length(gest):
  new_gest = []
  for i in range(0,len(gest),99):
    new_gest += gest[i:i+99] + [0]
  return new_gest



#THIS FUNCTION REMOVES THE OFFSET FROM  THE SIGNAL
def rmv_mean(gest, time):
  for i in range(0,len(gest),100):
    emg_correctmean = gest - np.mean(gest)
  return emg_correctmean



#THIS FUNCTION CREATES A BANDPASS FILTER
def bp_filter(x, low_f, high_f, samplerate, plot=False):
    x = x - np.mean(x)

    low_cutoff_bp = low_f / (samplerate / 2)
    high_cutoff_bp = high_f / (samplerate / 2)

    [b, a] = signal.butter(5, [low_cutoff_bp, high_cutoff_bp], btype='bandpass')

    x_filt = signal.filtfilt(b, a, x)

    if plot:
        t = np.arange(0, len(x) / samplerate, 1 / samplerate)
        plt.plot(t, x)
        plt.plot(t, x_filt, 'k')
        plt.autoscale(tight=True)
        plt.xlabel('Time (sec)')
        plt.ylabel('EMG (mV)')
        plt.ylim(-1.7,1.7)
        plt.show()

    return x_filt



#THIS FUNCTION CREATES A NOTCH FILTER
def notch_filter(x, samplerate, plot=False):
    x = x - np.mean(x)

    high_cutoff_notch = 59 / (samplerate / 2)
    low_cutoff_notch = 61 / (samplerate / 2)

    [b, a] = signal.butter(4, [high_cutoff_notch, low_cutoff_notch], btype='stop')

    x_filt = signal.filtfilt(b, a, x.T)

    if plot:
        t = np.arange(0, len(x) / samplerate, 1 / samplerate)
        plt.plot(t, x)
        plt.plot(t, x_filt, 'k')
        plt.autoscale(tight=True)
        plt.xlabel('Time (sec)')
        plt.ylabel('EMG (mV)')
        plt.ylim(-1.7,1.7)
        plt.show()
    
    return x_filt



#THIS FUNCTION CALCULATES THE FEATURES
def features(gest_filtered):
  l_mav = []
  l_max_val = []
  l_min_val = []
  l_rms = []
  l_var = []
  l_damv = []
  l_dvarv = []
  l_iasd = []
  l_ie = []

  for i in range(0, len(gest_filtered), 100):
    signal = gest_filtered[i:i+100]
    n = len(signal)

    #calculamos MAV
    mav = np.sum(np.abs(signal))/n
    l_mav.append(mav)
    
    #calculamos max y min
    max_val = signal.max()
    l_max_val.append(max_val)
    min_val = signal.min()
    l_min_val.append(min_val)

    #calculamos RMS
    rms = np.sqrt(np.sum(np.square(signal))/n)
    l_rms.append(rms)

    #calculamos VAR
    var = np.var(signal)
    l_var.append(var)

    # Derivada de signal
    signal_1 = signal[1:]
    signal_q = signal[:-1]

    #calculamos DAMV
    damv = (np.sum(np.abs(signal_1 - signal_q)))/(n-1)
    l_damv.append(damv)

    #calculamos DVARV
    dvarv = (np.sum(np.square(signal_1 - signal_q)))/(n-2)
    l_dvarv.append(dvarv)

    #calculamos IASD
    signal_prima = signal_1 - signal_q
    signal_prima_1 = signal_prima[1:]
    signal_prima_q = signal_prima[:-1]
    iasd = np.sum(np.abs(signal_prima_1 - signal_prima_q))
    l_iasd.append(iasd)

    #calculamos IE
    ie = np.sum(np.exp(signal))
    l_ie.append(ie)
  
  return l_mav, l_max_val, l_min_val, l_rms, l_var, l_damv, l_dvarv, l_iasd, l_ie



#THIS FUNCTION CALCULATES THE FEATURES, WITH A SAMPLED SIGNAL
def features_2(gest_filtered):
  l_mav = []
  l_max_val = []
  l_min_val = []
  l_rms = []
  l_var = []
  l_damv = []
  l_dvarv = []
  l_iasd = []
  l_ie = []
  l_mav2 = []
  l_max_val2 = []
  l_min_val2 = []
  l_rms2 = []
  l_var2 = []
  l_damv2 = []
  l_dvarv2 = []
  l_iasd2 = []
  l_ie2 = []

  for i in range(0, len(gest_filtered), 100):
    signal = gest_filtered[i:i+50]
    signal2 = gest_filtered[i+50:i+100]
    n = len(signal)


    #calculation of MAV
    mav = np.sum(np.abs(signal))/n
    l_mav.append(mav)

    mav2 = np.sum(np.abs(signal2))/n
    l_mav2.append(mav2)
    

    #calculation of MAX and MIN
    max_val = signal.max()
    l_max_val.append(max_val)
    min_val = signal.min()
    l_min_val.append(min_val)
    
    max_val2 = signal2.max()
    l_max_val2.append(max_val2)
    min_val2 = signal2.min()
    l_min_val2.append(min_val2)


    #calculation of RMS
    rms = np.sqrt(np.sum(np.square(signal))/n)
    l_rms.append(rms)

    rms2 = np.sqrt(np.sum(np.square(signal2))/n)
    l_rms2.append(rms2)


    #calculation of VAR
    var = np.var(signal)
    l_var.append(var)

    var2 = np.var(signal2)
    l_var2.append(var2)


    #signal and signal2 derivate
    signal_1 = signal[1:]
    signal_q = signal[:-1]

    signal2_1 = signal2[1:]
    signal2_q = signal2[:-1]


    #calculation of DAMV
    damv = (np.sum(np.abs(signal_1 - signal_q)))/(n-1)
    l_damv.append(damv)

    damv2 = (np.sum(np.abs(signal2_1 - signal2_q)))/(n-1)
    l_damv2.append(damv2)


    #calculation of DVARV
    dvarv = (np.sum(np.square(signal_1 - signal_q)))/(n-2)
    l_dvarv.append(dvarv)

    dvarv2 = (np.sum(np.square(signal2_1 - signal2_q)))/(n-2)
    l_dvarv2.append(dvarv2)


    #Signal and signal2 second derivate
    signal_prima = signal_1 - signal_q
    signal_prima_1 = signal_prima[1:]
    signal_prima_q = signal_prima[:-1]

    signal2_prima = signal2_1 - signal2_q
    signal2_prima_1 = signal2_prima[1:]
    signal2_prima_q = signal2_prima[:-1]


    #calculation of IASD
    iasd = np.sum(np.abs(signal_prima_1 - signal_prima_q))
    l_iasd.append(iasd)

    iasd2 = np.sum(np.abs(signal2_prima_1 - signal2_prima_q))
    l_iasd2.append(iasd2)


    #calculation of IE
    ie = np.sum(np.exp(signal))
    l_ie.append(ie)

    ie2 = np.sum(np.exp(signal2))
    l_ie2.append(ie2)

  
  return l_mav, l_max_val, l_min_val, l_rms, l_var, l_damv, l_dvarv, l_iasd, l_ie, l_mav2, l_max_val2, l_min_val2, l_rms2, l_var2, l_damv2, l_dvarv2, l_iasd2, l_ie2



#THIS FUNCTION CALCULATES THE FEATURES FOR THE EVALUATION
def preprocessing_3(gest_filtered):
  l_mav = []
  l_max_val = []
  l_min_val = []
  l_rms = []
  l_var = []
  l_damv = []
  l_dvarv = []
  l_iasd = []
  l_ie = []
  l_mav2 = []
  l_max_val2 = []
  l_min_val2 = []
  l_rms2 = []
  l_var2 = []
  l_damv2 = []
  l_dvarv2 = []
  l_iasd2 = []
  l_ie2 = []

  for i in range(0, 100, 100):
    signal = gest_filtered[i:i+50]
    signal2 = gest_filtered[i+50:i+100]
    n = len(signal)


    #calculation of MAV
    mav = np.sum(np.abs(signal))/n
    l_mav.append(mav)

    mav2 = np.sum(np.abs(signal2))/n
    l_mav2.append(mav2)
    

    #calculation of MAX and MIN
    max_val = signal.max()
    l_max_val.append(max_val)
    min_val = signal.min()
    l_min_val.append(min_val)
    
    max_val2 = signal2.max()
    l_max_val2.append(max_val2)
    min_val2 = signal2.min()
    l_min_val2.append(min_val2)


    #calculation of RMS
    rms = np.sqrt(np.sum(np.square(signal))/n)
    l_rms.append(rms)

    rms2 = np.sqrt(np.sum(np.square(signal2))/n)
    l_rms2.append(rms2)


    #calculation of VAR
    var = np.var(signal)
    l_var.append(var)

    var2 = np.var(signal2)
    l_var2.append(var2)


    #signal and signal2 derivate
    signal_1 = signal[1:]
    signal_q = signal[:-1]

    signal2_1 = signal2[1:]
    signal2_q = signal2[:-1]


    #calculation of DAMV
    damv = (np.sum(np.abs(signal_1 - signal_q)))/(n-1)
    l_damv.append(damv)

    damv2 = (np.sum(np.abs(signal2_1 - signal2_q)))/(n-1)
    l_damv2.append(damv2)


    #calculation of DVARV
    dvarv = (np.sum(np.square(signal_1 - signal_q)))/(n-2)
    l_dvarv.append(dvarv)

    dvarv2 = (np.sum(np.square(signal2_1 - signal2_q)))/(n-2)
    l_dvarv2.append(dvarv2)


    #Signal and signal2 second derivate
    signal_prima = signal_1 - signal_q
    signal_prima_1 = signal_prima[1:]
    signal_prima_q = signal_prima[:-1]

    signal2_prima = signal2_1 - signal2_q
    signal2_prima_1 = signal2_prima[1:]
    signal2_prima_q = signal2_prima[:-1]


    #calculation of IASD
    iasd = np.sum(np.abs(signal_prima_1 - signal_prima_q))
    l_iasd.append(iasd)

    iasd2 = np.sum(np.abs(signal2_prima_1 - signal2_prima_q))
    l_iasd2.append(iasd2)


    #calculation of IE
    ie = np.sum(np.exp(signal))
    l_ie.append(ie)

    ie2 = np.sum(np.exp(signal2))
    l_ie2.append(ie2)

  
  return l_mav, l_max_val, l_min_val, l_rms, l_var, l_damv, l_dvarv, l_iasd, l_ie, l_mav2, l_max_val2, l_min_val2, l_rms2, l_var2, l_damv2, l_dvarv2, l_iasd2, l_ie2
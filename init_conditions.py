
import numpy as np
import globals
from io_continua import *
import os.path
from os import path

def mydistspace(start,stop,n,lmin):
    lmax=(stop-start)/2.0
    lmin=lmin/2.0
    x1=2.0            # use log curve from x1 to x2
    x2=5.0
    logx1=np.log10(x1)
    logx2=np.log10(x2)
    c1=(lmax-lmin)/(x2-x1)
    c2=(lmax*x1-lmin*x2)/(x1-x2)
    xf=c1*np.logspace(logx1, logx2, num=int(n/2), endpoint=True)+c2
    xb=-xf[::-1]    # reverse
    x=np.concatenate((xb,xf), axis=0)+lmax+start
    return x

def myinterpolation(x):
    len1,len2=np.shape(x)                               # setup original indices
    lin1=np.linspace(0, 1, len1)
    lin2=np.linspace(0, 1, len2)
    x=interpolate.interp2d(lin2, lin1, x, kind='cubic') # interpolation function | forgot why indices are swapped
    lin1=np.linspace(0, 1, N1+2)                        # setup new indices
    lin2=np.linspace(0, 1, N2+2)
    x=x(lin2,lin1)                                      # interpolate | forgot why indices are swapped
    return  x

def read_previous():
    N1=globals.N1
    N2=globals.N2
    x,y,z,ly,lz=read_continua()
    if np.shape(x)!=(N1+2,N2+2):
        len1,len2=np.shape(x)
        print('Interpolating continua data from %ix%i to %ix%i' % (len1,len2,N1+2,N2+2))
        x=myinterpolation(x)
        y=myinterpolation(y)
        z=myinterpolation(z)
        ly=myinterpolation(ly)
        lz=myinterpolation(lz)
    else:
        print('Continua data have the same shape')
    return x,y,z,ly,lz

def create_positions():
    N1=globals.N1
    N2=globals.N2
    netY=globals.netY
    netZ=globals.netZ
    print('Using default initial conditions...')
    x=np.zeros((N1+2,N2+2))
    #lin1=(netY/N1)*mydistspace(0, N1+1, N1+2,0.005)
    #lin2=(netZ/N2)*mydistspace(0, N2+1, N2+2,0.001)
    lin1=(netY/N1)*np.linspace(0, N1+1, N1+2)
    lin2=(netZ/N2)*np.linspace(0, N2+1, N2+2)
    z,y=np.meshgrid(lin2,lin1)
    ly,lz=y[1:,:]-y[:-1,:],z[:,1:]-z[:,:-1]
    return x,y,z,ly,lz

def set_positions():
    tmp=path.exists('continua_x.out')
    if tmp: x,y,z,ly,lz=read_previous()
    else:   x,y,z,ly,lz=create_positions()
    return x,y,z,ly,lz

def set_velocities():
    N1=globals.N1
    N2=globals.N2
    vx=np.zeros((N1+2,N2+2))
    vy=np.zeros((N1+2,N2+2))
    vz=np.zeros((N1+2,N2+2))
    vx[10:12,10:12]=5.0
    return vx,vy,vz
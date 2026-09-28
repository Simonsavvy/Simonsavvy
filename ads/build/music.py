# Original royalty-free background loop: warm pad chords + soft kick + shaker, ~96 BPM.
import numpy as np, sys, wave
sr=44100; dur=float(sys.argv[1]); out=sys.argv[2]
n=int(sr*dur); t=np.arange(n)/sr; bpm=96; beat=60/bpm
def note(f): return 440*2**((f-69)/12)
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
mix=np.zeros(n)
bar=beat*4
for i in range(int(dur/bar)+1):
    s=int(i*bar*sr); e=min(n,int((i+1)*bar*sr))
    if s>=n: break
    tt=np.arange(e-s)/sr; env=np.minimum(1,tt/0.4)*np.minimum(1,(bar-tt)/0.4)
    for m in chords[i%4]:
        f=note(m); mix[s:e]+=0.06*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt))
    f=note(chords[i%4][0]-12); mix[s:e]+=0.08*env*np.sin(2*np.pi*f*tt)
for k in range(int(dur/beat)+1):
    s=int(k*beat*sr)
    if s>=n: break
    L=min(int(0.25*sr),n-s); tt=np.arange(L)/sr
    mix[s:s+L]+=0.35*np.sin(2*np.pi*(55+60*np.exp(-tt*30))*tt)*np.exp(-tt*12)   # kick
    for off in (0.5,):  # off-beat shaker
        s2=int((k+off)*beat*sr)
        if s2<n:
            L2=min(int(0.06*sr),n-s2); mix[s2:s2+L2]+=0.05*np.random.randn(L2)*np.exp(-np.arange(L2)/sr*60)
fade=int(0.8*sr); mix[-fade:]*=np.linspace(1,0,fade); mix[:int(0.3*sr)]*=np.linspace(0,1,int(0.3*sr))
mix=mix/np.max(np.abs(mix))*0.8
st=np.stack([mix,mix],1); d=(st*32767).astype(np.int16)
w=wave.open(out,"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes()); w.close()

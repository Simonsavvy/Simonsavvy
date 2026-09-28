import subprocess, wave
from tiktok import *
from rhvoice_wrapper import TTS
tts=TTS(threads=1,quiet=True)
def say(text,path):
    open(path,"wb").write(tts.get(text,voice="slt",format_="wav"))
    raw=path+".tmp.wav"; import os; os.replace(path,raw)
    subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-ar","44100",path],check=True)
    w=wave.open(path); d=w.getnframes()/w.getframerate(); w.close(); return d
def ad_vo(name,hsrc,hcrop,hst,hook,segs,end,lines):
    """segs: (kind,a,b,cap,yoff,weight). Video timing follows the voiceover."""
    d1=say(lines[0],"vo/l1.wav"); d2=say(lines[1],"vo/l2.wav"); d3=say(lines[2],"vo/l3.wav")
    hd=max(2.8,d1+0.35); dd=d2+0.4; ed=d3+1.0; total=hd+dd+ed
    boxes(hook,"hk.png",620,62,ai=True); endcard(*end,"end.png")
    ins=["-ss",str(hst),"-t",f"{hd:.2f}","-i",hsrc,"-loop","1","-i","hk.png"]
    fc=f"[0:v]{hookf(hsrc,hcrop)},tpad=stop_mode=clone:stop_duration=5,trim=duration={hd:.2f}[h0];[h0][1:v]overlay=shortest=1,{N}[h];"; lst="[h]"; n=2
    wsum=sum(s[5] for s in segs)
    for k,(kind,a,b,cap,yoff,wt) in enumerate(segs):
        sd=dd*wt/wsum
        if kind=="S":
            subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",APP,"-frames:v","1",f"st{k}.png"],check=True)
            ins+=["-loop","1","-t",f"{sd:.2f}","-i",f"st{k}.png"]
        else: ins+=["-ss",str(a),"-t",str(round(b-a,2)),"-i",APP]
        boxes(cap,f"cap{k}.png",270,50,bg=(20,96,58),fg="white"); ins+=["-loop","1","-i",f"cap{k}.png"]
        fc+=(f"[{n}:v]crop=720:1280:0:{yoff},scale=w='1080*(1+0.025*t)':h=-2:eval=frame,crop=1080:1920,{N},"
             f"tpad=stop_mode=clone:stop_duration=10,trim=duration={sd:.2f},setpts=PTS-STARTPTS[s{k}];"
             f"[s{k}][{n+1}:v]overlay=shortest=1,{N}[d{k}];"); lst+=f"[d{k}]"; n+=2
    ins+=["-loop","1","-t",f"{ed:.2f}","-i","end.png"]
    fc+=f"[{n}:v]scale=w='1080*(1+0.02*t)':h=-2:eval=frame,crop=1080:1920,{N}[e];{lst}[e]concat=n={len(segs)+2}:v=1:a=0[v];"
    subprocess.run(["python3","music.py",f"{total:.2f}","vo/music.wav"],check=True)
    a0=n+1
    ins+=["-i","vo/l1.wav","-i","vo/l2.wav","-i","vo/l3.wav","-i","vo/music.wav"]
    t1,t2,t3=150,int((hd+0.1)*1000),int((hd+dd+0.2)*1000)
    vox="highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aresample=44100,aformat=channel_layouts=stereo"
    fc+=(f"[{a0}:a]{vox},adelay={t1}|{t1}[a1];[{a0+1}:a]{vox},adelay={t2}|{t2}[a2];[{a0+2}:a]{vox},adelay={t3}|{t3}[a3];"
         f"[a1][a2][a3]amix=inputs=3:normalize=0,volume=1.6,asplit=2[vsc][voice];[{a0+3}:a]volume=0.16[mus];"
         f"[mus][vsc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[duck];"
         f"[duck][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,atrim=duration={total:.2f}[a]")
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[v]","-map","[a]",
        "-c:v","libx264","-profile:v","high","-crf","18","-preset","medium","-c:a","aac","-b:a","192k","-ar","44100",
        "-movflags","+faststart",f"../{name}"],check=True); print("ok",name,round(total,1),"s")
ad_vo("simovet_ad1_farmers_licensed.mp4",V3,C3,0,"how do you know your vet is actually licensed?",
   [("S",3.5,0,"every vet's KVB licence is checked by a person",120,1.2),
    ("V",4.0,5.0,"book and pay with m-pesa",120,0.8),
    ("V",32.8,34.9,"verified vets near you, nearest first",170,1.0)],
   ("Book a KVB-verified vet. Pay by M-Pesa.","Every vet's licence is checked by a person."),
   ["How do you know your vet is really licensed?",
    "On SimoVet, every vet's K V B licence is checked by a person. Find a verified vet near you, and pay by M-Pesa.",
    "Visit simonetvetcare dot co dot ke."])
ad_vo("simovet_ad2_vets_paid_first.mp4",V4,C4,3,"the farmer pays before you even see the request",
   [("V",4.0,5.0,"farmers pay by m-pesa when they book",120,0.8),
    ("S",8.9,0,"85% paid to your m-pesa after each confirmed visit",170,1.4)],
   ("Vets: free to join.","Set your own prices, hours and service area."),
   ["Vets, listen. The farmer pays before you even see the request.",
    "Farmers pay by M-Pesa when they book. You keep eighty five percent, paid to your M-Pesa after each confirmed visit.",
    "Free to join. simonetvetcare dot co dot ke."])
ad_vo("simovet_ad3_farmers_prices.mp4",V3,C3,4,"vet prices shown before you book. finally.",
   [("V",39.5,44.8,"every vet card shows services + prices",170,1.0)],
   ("See each vet's services and prices before you book.","Pay by M-Pesa. Get a full visit record."),
   ["No more guessing vet prices.",
    "On SimoVet, every vet card shows their services and prices before you book. Pay by M-Pesa, and get a full visit record.",
    "simonetvetcare dot co dot ke."])
import os; tts.join(); os._exit(0)

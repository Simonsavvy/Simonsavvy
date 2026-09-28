import sherpa_onnx, soundfile as sf, sys
M="/tmp/claude-0/-home-user-Simonsavvy/85553a0d-6a9c-5531-9d67-65ea6d12bafa/scratchpad/npm/package/kokoro-int8-en-v0_19"
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=M+"/model.int8.onnx",voices=M+"/voices.bin",tokens=M+"/tokens.txt",data_dir=M+"/espeak-ng-data"),
    num_threads=4))
tts=sherpa_onnx.OfflineTts(cfg)
def say(text,path,sid=1,speed=1.05):
    a=tts.generate(text,sid=sid,speed=speed); sf.write(path,a.samples,a.sample_rate); return len(a.samples)/a.sample_rate
if __name__=="__main__":
    print(tts.num_speakers)
    for sid in (1,3,7): print(sid, round(say("How do you know your vet is really licensed? On SimoVet, every vet's K V B licence is checked by a person.",f"vo/k{sid}.wav",sid),2))

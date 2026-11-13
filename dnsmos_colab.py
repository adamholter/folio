"""DNSMOS P.835 (SIG, BAK, OVRL) for 48 kHz WAVs; follows Microsoft DNS-Challenge dnsmos_local.py."""
import sys,os,subprocess,glob,json,urllib.request
try:
    import onnxruntime as ort
except ImportError:
    subprocess.run([sys.executable,'-m','pip','-q','install','onnxruntime'],check=True)
    import onnxruntime as ort
import numpy as np,soundfile as sf
from scipy import signal
MODEL='/tmp/sig_bak_ovr.onnx'
if not os.path.exists(MODEL):
    urllib.request.urlretrieve('https://github.com/microsoft/DNS-Challenge/raw/master/DNSMOS/DNSMOS/sig_bak_ovr.onnx',MODEL)
FS=16000;LEN=int(9.01*FS)
sess=ort.InferenceSession(MODEL,providers=['CPUExecutionProvider'])
p_ovr=np.poly1d([-0.06766283,1.11546468,0.04602535]);p_sig=np.poly1d([-0.08397278,1.22083953,0.0052439]);p_bak=np.poly1d([-0.13166888,1.60915514,-0.39604546])
def score(path):
    x,sr=sf.read(path,dtype='float64')
    if sr!=FS:x=signal.resample_poly(x,FS,sr)
    rows=[]
    for i in range(int(np.floor(len(x)/FS)-9.01)+1):
        seg=x[i*FS:i*FS+LEN]
        s,b,o=sess.run(None,{'input_1':seg.astype('float32')[None,:]})[0][0]
        rows.append((p_sig(s),p_bak(b),p_ovr(o)))
    return [round(float(v),3) for v in np.mean(rows,axis=0)]
out={}
for pattern in sys.argv[1:]:
    for path in sorted(glob.glob(pattern)):
        out[path]=dict(zip(('SIG','BAK','OVRL'),score(path)));print('DNSMOS',path,out[path],flush=True)
print('DNSMOS_JSON',json.dumps(out))

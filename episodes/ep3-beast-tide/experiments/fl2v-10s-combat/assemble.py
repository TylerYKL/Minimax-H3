"""Assemble three H3 renders into a mute 10s rough cut; not final action editing.
python assemble.py shot01.mp4 shot02.mp4 shot03.mp4 --output rough-10s.mp4
Requires ffmpeg and ffprobe on PATH. Preserves the endpoints of each clip.
"""
import argparse,json,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('clips',nargs=3,type=Path);p.add_argument('--output',type=Path,default=Path('rough-10s.mp4'));a=p.parse_args()
if a.output.exists():p.error('Output already exists; choose a new --output path.')
def probe(f):
 q=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(f)]))
 return q['streams'][0]
def run(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
enc=['-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']
with tempfile.TemporaryDirectory(prefix='ep3-fl2v-') as tmp:
 files=[]
 for i,(src,target) in enumerate(zip(a.clips,[72,72,96])):
  info=probe(src);n=int(info['nb_read_frames'])
  if info['r_frame_rate']!='24/1' or n<target:raise SystemExit(f'{src}: need 24fps and at least {target} frames; got {info}')
  indices=[round(j*(n-1)/(target-1)) for j in range(target)]
  assert len(set(indices))==target
  select='+'.join(f'eq(n,{j})' for j in indices)
  vf=f"select='{select}',setpts=N/(24*TB),scale=864:480:force_original_aspect_ratio=decrease,pad=864:480:(ow-iw)/2:(oh-ih)/2,setsar=1"
  out=Path(tmp)/f'{i}.mp4';files.append(out)
  run(['-i',str(src),'-vf',vf,'-r','24']+enc+[str(out)])
 args=[]
 for f in files:args+=['-i',str(f)]
 run(args+['-filter_complex','[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]','-map','[v]']+enc+[str(a.output)])
 assert int(probe(a.output)['nb_read_frames'])==240
print(f'Created {a.output}: 240 frames / 24fps = 10.000s. Rough cut only; inspect contact timing before final edit.')

"""Conform the three-shot 253-frame output to 240 frames, preserving shot endpoints.
python conform_10s.py ALL-output.mp4 --output support-10s.mp4
Requires ffmpeg/ffprobe. Rejects unexpected input length rather than guessing cuts.
"""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path);p.add_argument('--output',type=Path,default=Path('support-10s.mp4'));a=p.parse_args()
if a.output.exists():p.error('Output already exists; choose a new filename.')
def inspect(f):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames,r_frame_rate,duration','-of','json',str(f)]))['streams'][0]
s=inspect(a.video)
if s['r_frame_rate']!='24/1' or int(s['nb_read_frames'])!=253:raise SystemExit(f'Expected 253 frames at 24fps, got {s}. Inspect group boundaries first.')
indices=[];cursor=0
for source_count,target in [(73,72),(107,96),(73,72)]:
 indices += [cursor+round(j*(source_count-1)/(target-1)) for j in range(target)]
 cursor+=source_count
assert len(indices)==len(set(indices))==240
vf="select='"+'+'.join(f'eq(n,{i})' for i in indices)+"',setpts=N/(24*TB)"
subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-vf',vf,'-r','24','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)],check=True)
s=inspect(a.output);assert int(s['nb_read_frames'])==240 and abs(float(s['duration'])-10)<.001
print('Verified 240 frames / 24fps / 10.000 seconds. Inspect repair and impact timing; this is only a rough duration conform.')

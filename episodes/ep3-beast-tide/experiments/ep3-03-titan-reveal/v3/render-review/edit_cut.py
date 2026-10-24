"""Build a 5.5-second silent editorial review from four user-rendered V3 clips.
Usage: python edit_cut.py FOOT SCALE LAUNCH FOLLOW --output review.mp4
"""
import argparse,subprocess,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('clips',nargs=4,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
if a.output.exists():p.error('Choose a new output filename.')
plan=[(56,36,24),(39,30,30),(73,48,42),(73,48,36)]
filters=[]
for i,(file,(expected,source,target)) in enumerate(zip(a.clips,plan)):
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(file)]))['streams'][0]
 assert int(info['nb_read_frames'])==expected and info['r_frame_rate']=='24/1',info
 keep={round(j*(source-1)/(target-1)) for j in range(target)}
 drop=[n for n in range(source) if n not in keep]
 select="select='not("+'+'.join(f'eq(n,{n})' for n in drop)+")'," if drop else ''
 filters.append(f'[{i}:v]trim=start_frame=0:end_frame={source},{select}setpts=N/(24*TB),setsar=1[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(4))+'concat=n=4:v=1:a=0[out]')
cmd=['ffmpeg','-v','error']
for f in a.clips:cmd+=['-i',str(f)]
cmd+=['-filter_complex',';'.join(filters),'-map','[out]','-an','-r','24','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)]
subprocess.run(cmd,check=True)
print('Created',a.output)

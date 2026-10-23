"""Rebuild the 240-frame multi-angle edit from committed H3 renders."""
from pathlib import Path
import subprocess,json,tempfile
ROOT=Path(__file__).resolve().parent
sources={'main':ROOT.parent/'fl2v-single-10s/render-review/source-243f.mp4'}
for k in 'ABCD':sources[k]=ROOT.parent/f'fl2v-camera-angles/render-review/sources/{k}.mp4'
# Source frames are zero based; end is exclusive. No repeated source ranges.
shots=[('main',0,9,'侧面：扑进'),('A',6,33,'第一人称：撞盾与反弹'),('main',36,86,'侧面：落地、再扑与收盾'),('B',0,14,'怪兽肩后：挥刀命中'),('main',123,145,'侧面：命中后的击飞'),('C',4,31,'贴地：撞路障与落地'),('main',177,218,'侧面：恢复与换盾'),('D',0,25,'俯拍：交代位置'),('main',218,243,'侧面：收尾')]
assert sum(b-a for _,a,b,_ in shots)==240
enc=['-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']
def run(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
manifest=[];cursor=0
with tempfile.TemporaryDirectory(prefix='ep3-multiview-') as td:
 clips=[]
 for i,(src,a,b,note) in enumerate(shots):
  f=Path(td)/f'{i}.mp4';clips.append(f)
  run(['-i',str(sources[src]),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS','-r','24']+enc+[str(f)])
  manifest.append(dict(source=src,source_file=str(sources[src].relative_to(ROOT.parent)),source_start_frame=a,source_end_exclusive=b,output_start_frame=cursor,output_end_exclusive=cursor+b-a,description=note));cursor+=b-a
 args=[]
 for f in clips:args+=['-i',str(f)]
 graph=''.join(f'[{i}:v]' for i in range(len(clips)))+f'concat=n={len(clips)}:v=1:a=0[v]'
 output=ROOT/'EP3-multiview-10s.mp4'
 run(args+['-filter_complex',graph,'-map','[v]']+enc+[str(output)])
 q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]));s=q['streams'][0]
 assert len(q['streams'])==1 and int(s['nb_read_frames'])==240 and s['r_frame_rate']=='24/1' and abs(float(s['duration'])-10)<.001
(ROOT/'edit-map.json').write_text(json.dumps(dict(fps=24,frames=240,duration=10,retimed=False,audio=False,shots=manifest),ensure_ascii=False,indent=2)+'\n')
print('Verified: 240 frames, 24fps, 10.000 seconds, 9 shots, mute.')

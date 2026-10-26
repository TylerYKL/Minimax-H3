"""Trim the expected243-frame24fps output to240frames, keeping the first10seconds."""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
if a.output.exists():p.error('Choose a new output filename.')
def probe(f):return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames,r_frame_rate,duration','-of','json',str(f)]))['streams'][0]
s=probe(a.video)
if int(s['nb_read_frames'])!=243 or s['r_frame_rate']!='24/1':p.error(f'Expected243frames/24fps; received{s}')
subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-vf','trim=end_frame=240,setpts=N/(24*TB)','-an','-r','24','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)],check=True)
s=probe(a.output);assert int(s['nb_read_frames'])==240 and abs(float(s['duration'])-10)<.001
print('Verified240frames/24fps/10seconds; inspect actual cut timing before adding HUD.')

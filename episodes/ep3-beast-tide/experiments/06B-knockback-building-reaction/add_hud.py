"""Overlay a readable teammate-telemetry panel on the Nyx render.
python add_hud.py NYX.mp4 --output NYX-hud.mp4 --damage 78
Use --font /path/to/font.ttf when automatic font discovery is unavailable.
"""
import argparse,json,subprocess,os
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--damage',type=int,default=78);p.add_argument('--font',type=Path);a=p.parse_args()
if not 0<=a.damage<=100:p.error('Damage must be0–100.')
if a.output.exists():p.error('Choose a new output filename.')
fonts=[a.font,Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'),Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/consola.ttf',Path('/System/Library/Fonts/Menlo.ttc')]
font=next((f for f in fonts if f and f.is_file()),None)
if not font:p.error('Pass --font with an existing TrueType font.')
font=str(font.resolve()).replace('\\','/').replace(':','\\:').replace("'","\\'")
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(a.video)]))['streams'][0]
if (info['width'],info['height'])!=(864,480):p.error('Expected864x480; resize the video before this overlay.')
f=['drawbox=x=540:y=72:w=304:h=238:color=0x071019@0.86:t=fill','drawbox=x=540:y=72:w=304:h=238:color=0xa76bff@0.9:t=2','drawbox=x=558:y=235:w=262:h=12:color=0x35232d:t=fill']
if a.damage:f.append(f'drawbox=x=558:y=235:w={round(262*a.damage/100)}:h=12:color=0xff654f:t=fill')
for txt,x,y,size,color in [('SQUAD TELEMETRY',558,88,16,'0xcfaaff'),('AEGIS',558,118,27,'white'),('ARMOR DAMAGE',558,160,17,'0xe2dce9'),(str(a.damage)+'%',558,180,40,'0xff765e'),('DAMAGE ALERT',558,263,18,'0xff765e')]:
 f.append(f"drawtext=fontfile='{font}':text='{txt}':expansion=none:x={x}:y={y}:fontsize={size}:fontcolor={color}")
subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-vf',','.join(f),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)],check=True)
print('HUD applied. Damage is a configurable fictional armor-status value:',a.damage)

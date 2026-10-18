"""Encode 10-second previews, 243-frame H3 sources and RV2V templates.
python export.py --frames /path/to/frames --output exports
Frames directory contains 01/0000.png..0242.png and 02/0000.png..0242.png.
"""
import argparse,copy,hashlib,json,subprocess,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--frames',required=True);p.add_argument('--output',default=str(ROOT/'exports'));a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
base=json.loads((ROOT/'../../experiments/06A-rv2v-impact-separation/workflow-rv2v-template.json').resolve().read_text())
refs=[dict(index=i,imageFile=f,fileName='',type='input',subfolder='') for i,f in enumerate(['沈烈Aegis三视图_去背景-resize.png','nyx-aim.png','lyra-skill.png','A-team.png','aegis-airborne-shield.png','C-blade-contact.png'])]
enc=['-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']
def ff(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
def inspect(path,frames):
    q=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-count_frames','-of','json',str(path)]));s=q['streams'][0]
    assert len(q['streams'])==1 and int(s['nb_read_frames'])==frames and s['r_frame_rate']=='24/1'
    return dict(file=path.name,frames=frames,fps=24,duration_seconds=frames/24,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
assets=[];previews=[]
for seg in ['01','02']:
    frames=Path(a.frames)/seg;assert all((frames/f'{i:04d}.png').exists() for i in range(243))
    source=out/f'EP3-{seg}-H3-source-243f.mp4';preview=out/f'EP3-{seg}-preview-10s.mp4'
    ff(['-framerate','24','-i',str(frames/'%04d.png'),'-frames:v','243']+enc+[str(source)])
    ff(['-i',str(source),'-frames:v','240']+enc+[str(preview)])
    assets.extend([inspect(source,243),inspect(preview,240)]);previews.append(preview)
    prompt=(ROOT/'prompts_common.txt').read_text().replace('{SHOTS}',(ROOT/f'shots-{seg}.txt').read_text().strip())
    (out/f'EP3-{seg}-prompt.txt').write_text(prompt)
    w=copy.deepcopy(base);w['id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'EP3-ten-second-'+seg));w['revision']=0
    d=next(n for n in w['nodes'] if n['type']=='MiniMaxH3Director');v=d['widgets_values_named'];t=json.loads(v['timeline_data'])
    t['global']['prompt']=prompt;t['global']['refs']=refs;t['totalFrames']=243;t['gen']['defaultFrameCount']=243
    t['segments']=[dict(id='EP3-'+seg,start=0,length=243,frameCount=243,durationSec=243/24,prompt='',taskType='',refs=[],refVideos=[],refAudios=[],continuityFromPrev=False)]
    v['global_prompt']=prompt;v['timeline_data']=json.dumps(t,ensure_ascii=False);v['total_frames']=243;d['widgets_values']=list(v.values())
    for n in w['nodes']:
        if n['type']=='SaveVideo':
            n['widgets_values'][0]='video/EP3_10s_'+seg;n['widgets_values_named']['filename_prefix']=n['widgets_values'][0]
        if n['id']==13:
            note=f'EP3 第{seg}段。上传 {source.name} 到 RV2V 源视频时间轴，保留单个243帧片段。生成后裁取前240帧得到10秒，不改播放速度。图片1=Aegis三视图，2=Nyx持炮，3=Lyra技能，4=城市，5=盾，6=刀。CreateVideo audio不接线。十秒多镜头尚未实机验证。'
            n['widgets_values']=[note];n['widgets_values_named']={'text':note}
    (out/f'EP3-{seg}-workflow.json').write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n')
    chosen=[0,24,48,72,96,120,144,168,192,216,228,239]
    filt="scale=360:203,drawtext=text='Frame %{n}':x=6:y=6:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,select='"+'+'.join(f'eq(n,{n})' for n in chosen)+"',tile=4x3"
    ff(['-i',str(preview),'-vf',filt,'-frames:v','1',str(out/f'EP3-{seg}-keyframes.jpg')])
master=out/'EP3-first-20s-preview.mp4'
ff(['-i',str(previews[0]),'-i',str(previews[1]),'-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]','-map','[v]']+enc+[str(master)])
assets.append(inspect(master,480))
manifest=dict(previs_rendered=True,h3_rendered=False,workflow_tested_in_comfyui=False,preview_frames_per_segment=240,h3_frames_per_segment=243,fps=24,alignment='H3 17k+5: 240 rounds up to 243; trim last 3 frames, do not retime',reference_slots=refs,assets=assets,episode_plan='../episode-plan.json',audio_export_connected=False)
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
plan=json.loads((ROOT/'episode-plan.json').read_text())
for item in plan['segments'][:2]:item['status']='previs_rendered_h3_unverified'
(ROOT/'episode-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('Verified: two exact 10s previews, two 243f H3 sources, one exact 20s master.')

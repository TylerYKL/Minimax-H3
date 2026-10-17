"""Encode the master edit and per-shot sources; generate matching H3 prompts/templates.
python export.py --frames /path/to/frames
Requires ffmpeg/ffprobe and the repository's existing RV2V template.
"""
import argparse, copy, hashlib, json, subprocess, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--frames',required=True);p.add_argument('--config',default=str(ROOT/'timeline.json'));args=p.parse_args()
cfg=json.loads(Path(args.config).read_text());fps=cfg['fps'];events=cfg['events']
OUT=ROOT/'exports';OUT.mkdir(exist_ok=True)
base=json.loads((ROOT/'../../experiments/06A-rv2v-impact-separation/workflow-rv2v-template.json').resolve().read_text())
shared=next(n for n in base['nodes'] if n['type']=='MiniMaxH3Director')['widgets_values_named']
refs=json.loads(shared['timeline_data'])['global']['refs']
enc=['-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']
def ff(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
def probe(path,count):
    q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(path)]));s=q['streams'][0]
    assert len(q['streams'])==1 and int(s['nb_read_frames'])==count and s['r_frame_rate']==f'{fps}/1'
    return dict(file=str(path.relative_to(ROOT)),frames=count,fps=fps,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def prompt_for(shot):
    def sec(event):return f"{(events[event]-shot['world_start'])/fps:.3f}"
    if shot['camera']=='side':
        action=f'''Keep the single fixed side view. Initially Aegis hovers facing screen right, with his back toward the incoming claw. Foot exhaust supports his hover; the shield is absent. At approximately {sec('claw_entry')} seconds the giant claw suddenly enters behind him from screen left. At {sec('chill_start')} seconds replace the brief cyan back guides with a fleeting cold rim-light glint on his back armor. This is a reaction cue, not extra equipment. Do not add a close-up or cut.
At {sec('turn_start')} seconds he starts the source's rapid four-frame turn to face the claw, finishing by {sec('turn_end')} seconds. The right-forearm shield begins opening at {sec('shield_start')} seconds and is full-sized by {sec('shield_full')} seconds. At {sec('shield_contact')} seconds the claw strikes it. Replace the white marker with a one-frame white-gold peak flare followed by a fading refractive shockwave. Foot jets shut off on contact.
On the following frame Aegis and his attached shield already separate from the palm. Preserve the abrupt rightward displacement and backward torso tilt. A thin white streak tracks the moving body; no duplicate remains behind. Continue his forced flight out of the right edge. Keep the camera fixed on the claw's brief follow-through through the end. Do not prolong contact into a push, replay the strike or switch to another shot.'''
    else:
        action=f'''Keep the fixed high overhead view: the full thirty-meter giant at left, tiny Aegis in flight near center, and the forty-meter tower at right. Cars and building floors establish scale. The shot begins during knockback; do not replay the attack or introduce a hover. His back leads rightward, his shield stays on his right forearm, and foot jets are dark. Preserve the short white displacement streak without turning it into a separate projectile.
At approximately {sec('wall_contact')} seconds Aegis penetrates the target facade near its third floor. Replace the orange marker with a compact orange-white contact burst. On the next frame the source wall panels break outward; Aegis and his shield remain concealed inside the breach. Turn the proxy fragments into rubble and glass following their existing trajectories.
Continue the source's local support failure, upper-floor descent by roughly one floor, falling fragments and growing dust through the final frame. Keep the lower building standing. Replace faceted dust blobs with fine concrete dust while retaining a readable breach and descending roofline. The giant stays in place with its striking arm extended, without a second attack. No camera orbit, cut or recovery.'''
    return f'''subject_definitions:
<Video 1> is {shot['id']}-source.mp4, a {shot['source_frames']}-frame source at {fps} fps, lasting {shot['source_frames']/fps:.3f} seconds. Preserve its single camera, body scale, action order and rapid trajectories; replace the simplified geometry and effect guides.
<Subject 1> is the one Aegis shown in the multiple views of <Picture 1>: a 1.88-meter fighter wearing heavy worn gunmetal armor, orange-gold accents, a cyan visor and an orange hexagonal chest core. <Picture 2> supplies his attached RIGHT-forearm golden honeycomb shield appearance. No sword is active in this sequence.
<Subject 2> is the ruined-city environment from <Picture 3>, with weathered concrete, dark glazing, red-moon rim light and cool shadows. Transfer only the environment, not the other characters pictured there.
<Subject 3> is the thirty-meter titan from <Picture 4>: charcoal volcanic armor, red molten fissures, red eyes, horns, an intact red chest core and a tail rooted behind the pelvis with a stone hammer at its end. Both hands are empty. Maintain source anatomy and the sixteen-to-one height ratio.

summary:
[video editing + reference generation] The target video is an edited version of <Video 1>. Transfer finished cinematic 3D CG appearances while retaining the source's rapid combat timing and spatial continuity.

retention_analysis:
<Video 1> (entire shot): partially_preserved - retain duration, camera, layout, scale, motion and contacts; replace proxy surfaces and effect markers.
<Subject 1> (where visible): attribute_transfer - transfer consistent armor and attached shield onto the small fighter; preserve source poses rather than reference display poses.
<Subject 2> (entire shot): attribute_transfer - finish the city surfaces without changing the source layout or damage trajectory.
<Subject 3> (visible body or striking limb): attribute_transfer - transfer rock appearance without changing scale, limb count or action.

detailed_description:
Render finished cinematic 3D CG on all visible surfaces from the first frame. Preserve source camera and action timing. Treat thin lines, white flashes and coarse dust volumes as temporary effect guides, not final objects. Do not add slow motion, captions or watermarks.
{action}

overall_soundscape:
N/A

non_diegetic_music:
N/A
'''

# Adjacent edit ranges must refer to contiguous world time.
for a,b in zip(cfg['shots'],cfg['shots'][1:]):
    assert a['world_start']+a['edit_out']==b['world_start']+b['edit_in'], 'Discontinuous world-time edit'
assets=[];sources=[]
for shot in cfg['shots']:
    assert 0<=shot['edit_in']<shot['edit_out']<=shot['source_frames']
    folder=Path(args.frames)/shot['id']
    assert all((folder/f'{n:04d}.png').exists() for n in range(shot['source_frames']))
    source=OUT/(shot['id']+'-source.mp4');sources.append(source)
    ff(['-framerate',str(fps),'-i',str(folder/'%04d.png'),'-frames:v',str(shot['source_frames'])]+enc+[str(source)])
    assets.append(probe(source,shot['source_frames']))
    prompt=prompt_for(shot);(OUT/(shot['id']+'-prompt.txt')).write_text(prompt)
    w=copy.deepcopy(base);w['id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'ep3/combat-template-v1/'+shot['id']));w['revision']=0
    d=next(n for n in w['nodes'] if n['type']=='MiniMaxH3Director');v=d['widgets_values_named'];t=json.loads(v['timeline_data'])
    t['global']['prompt']=prompt;t['totalFrames']=shot['source_frames'];t['frameRate']=fps
    t['gen']['defaultFrameCount']=shot['source_frames']
    t['segments']=[dict(id=shot['id'],start=0,length=shot['source_frames'],frameCount=shot['source_frames'],durationSec=shot['source_frames']/fps,prompt='',taskType='',refs=[],refVideos=[],refAudios=[],continuityFromPrev=False)]
    v['global_prompt']=prompt;v['timeline_data']=json.dumps(t,ensure_ascii=False);v['total_frames']=shot['source_frames'];v['frame_rate']=fps
    d['widgets_values']=list(v.values())
    for n in w['nodes']:
        if n['type']=='SaveVideo':
            n['widgets_values'][0]='video/EP3_template_'+shot['id'];n['widgets_values_named']['filename_prefix']=n['widgets_values'][0]
        if n['id']==13:
            note=f"本镜上传 {source.name} 到 RV2V 源视频时间轴。参考槽：1 Aegis、2 盾、3 城市、4 巨兽。CreateVideo audio 不接线；Director audio_vae 保留。先看完整灰模，再决定生成。H3 实际切点需按输出调整。"
            n['widgets_values']=[note];n['widgets_values_named']={'text':note}
    (OUT/(shot['id']+'-workflow.json')).write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n')
# Master edit is assembled from exact frame ranges; source handles do not slow the action.
inputs=[];filters=[];labels=[];total=0
for i,(shot,source) in enumerate(zip(cfg['shots'],sources)):
    inputs+=['-i',str(source)]
    filters.append(f"[{i}:v]trim=start_frame={shot['edit_in']}:end_frame={shot['edit_out']},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    labels.append(f'[v{i}]');total+=shot['edit_out']-shot['edit_in']
filters.append(''.join(labels)+f'concat=n={len(sources)}:v=1:a=0[out]')
master=OUT/'combat-master.mp4'
ff(inputs+['-filter_complex',';'.join(filters),'-map','[out]','-r',str(fps)]+enc+[str(master)])
assets.append(probe(master,total))
selected=[0,28,29,32,34,36,37,38,41,48,64,total-1]
filt="scale=432:243,drawtext=text='Master frame %{n}':x=8:y=8:fontsize=17:fontcolor=white:box=1:boxcolor=black@0.6,select='"+'+'.join(f'eq(n,{n})' for n in selected)+"',tile=4x3"
ff(['-i',str(master),'-vf',filt,'-frames:v','1',str(OUT/'keyframes.jpg')])
manifest=dict(previs_rendered=True,h3_rendered=False,workflow_tested_in_comfyui=False,fps=fps,master_frames=total,master_seconds=total/fps,assets=assets,shots=cfg['shots'],events=events,source_upload_required=True,export_audio_connected=False,reference_slots=refs,world_scale_meters=dict(aegis=1.88,titan=30,target_tower=40))
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Exported master, per-shot sources, prompts, templates and manifest:',total,'master frames')

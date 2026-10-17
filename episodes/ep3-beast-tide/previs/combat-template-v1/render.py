"""Blender: shared scene and frame-driven reusable combat actions.
blender -b -t 4 --python render.py -- --output /path/to/frames
Optional --shot 01-ambush --frames 0,29,35,36,37,38
"""
import argparse, json, math, runpy, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
p.add_argument('--config',default=str(ROOT/'timeline.json'))
p.add_argument('--shot')
p.add_argument('--frames')
opts=p.parse_args(args)
cfg=json.loads(Path(opts.config).read_text())
e=cfg['events'];m=cfg['motion']
assert e['claw_entry']<e['turn_start']<=e['shield_start']<e['shield_contact']<e['wall_contact']
assert len(m['flight_x'])==e['wall_contact']-e['shield_contact']+1
s=runpy.run_path(str(ROOT/'scene.py'))
scene=s['scene'];hero=s['hero'];scene.render.fps=cfg['fps']
scene.render.resolution_x,scene.render.resolution_y=cfg['resolution']
# Both views use the same world; only the camera changes.
s['cam_a'].location=(-4,-15,13)
s['cam_a'].rotation_euler=(s['Vector']((-1,0,10.8))-s['cam_a'].location).to_track_quat('-Z','Y').to_euler()
s['cam_a'].data.ortho_scale=9
s['cam_b'].location=(-4,-39,55)
s['cam_b'].rotation_euler=(s['Vector']((0,0,22))-s['cam_b'].location).to_track_quat('-Z','Y').to_euler()
s['cam_b'].data.ortho_scale=72

def hover_turn_guard(n):
    """Rear awareness, four-frame turn, right-arm shield activation."""
    turn=max(0,min(1,(n-e['turn_start']+1)/(e['turn_end']-e['turn_start']+1)))
    hero.location=(0,0,10)
    hero.rotation_euler=(0,0,math.pi*(1-turn))
    hidden=n>e['wall_contact']
    for o in hero.children_recursive:o.hide_render=hidden
    for o in s['coldparts']:o.hide_render=not(e['chill_start']<=n<e['chill_end'])
    for o in s['shieldparts']:o.hide_render=n<e['shield_start'] or hidden
    size=.45 if e['shield_start']<=n<e['shield_full'] else 1
    s['shieldroot'].scale=(1,size,size)
    for o in s['jets']:o.hide_render=n>=e['shield_contact']

def claw_strike(n):
    """Single rear entry and strike, with a small follow-through."""
    if n<e['claw_entry']:x=m['claw_rest_x']
    elif n<=e['shield_contact']:
        a=(n-e['claw_entry'])/(e['shield_contact']-e['claw_entry'])
        x=m['claw_entry_x']+(m['claw_contact_x']-m['claw_entry_x'])*a
    else:x=m['claw_contact_x']+min(.25,(n-e['shield_contact'])*.05)
    s['palmroot'].location=(x,0,11.3)
    s['move_rod'](s['fore'],(-8,2.3,15),(x-.7,0,11.3))
    hit=n-e['shield_contact']
    s['flash'].hide_render=hit not in (0,1)
    s['flash'].scale=(.35,.65,.65) if hit==0 else (.16,.35,.35)
    s['shock'].hide_render=hit not in (0,1)
    s['shock'].scale=(1,.65,.65) if hit==0 else (1,1.65,1.65)
    for o in s['airwaves']:o.hide_render=True

def forced_flight(n):
    """Explicit displacement samples guarantee fast motion in the source."""
    k=n-e['shield_contact']
    if k>=0:
        x=m['flight_x'][min(k,len(m['flight_x'])-1)]
        hero.location=(x,0,10)
        hero.rotation_euler=(0,min(.65,k*.18),0)
    s['trail'].hide_render=not(e['shield_contact']<n<=e['wall_contact'])
    if not s['trail'].hide_render:
        x=hero.location.x;points=s['trail'].data.splines[0].points
        points[0].co=(max(.5,x-3),0,11,1);points[1].co=(x,0,11,1)

def facade_impact_collapse(n):
    """Contact flash, breach, ballistic rubble, local floor collapse."""
    k=n-e['wall_contact'];dt=max(0,k/cfg['fps'])
    s['wallflash'].hide_render=k not in (0,1)
    for o in s['breach']:o.hide_render=k>=1
    for i,level in enumerate(s['tower']):
        level.location=(0,0,0);level.rotation_euler=(0,0,0)
        if k>=1 and i>=2:
            a=max(0,dt-max(0,i-3)*.018)
            level.location=(-min(.35,.2*a),0,-min(m['max_floor_drop'],4.9*a*a+a))
            level.rotation_euler.y=-min(.018,.01*a)
            if i in (2,3):
                level.location.x=-min(.8,.7*a);level.rotation_euler.y=-min(.1,.08*a)
    for o,v,delay in s['chunks']:
        a=max(0,dt-delay);o.hide_render=k<1 or dt<delay
        o.location=s['Vector']((11.8,0,11))+v*a+s['Vector']((0,0,-4.9*a*a))
        o.rotation_euler=(a*2,a*3,a)
    for o,v in s['dust']:
        o.hide_render=k<4;o.location=s['Vector']((11.8,0,10))+v*dt
        a=max(.01,dt*.7);o.scale=(a,a,a)

def animate(world_frame,camera):
    hover_turn_guard(world_frame)
    claw_strike(world_frame)
    forced_flight(world_frame)
    facade_impact_collapse(world_frame)
    scene.camera=s['cam_a'] if camera=='side' else s['cam_b']

for shot in cfg['shots']:
    if opts.shot and shot['id']!=opts.shot:continue
    out=Path(opts.output)/shot['id'];out.mkdir(parents=True,exist_ok=True)
    frames=[int(x) for x in opts.frames.split(',')] if opts.frames else range(shot['source_frames'])
    for frame in frames:
        assert 0<=frame<shot['source_frames']
        animate(shot['world_start']+frame,shot['camera'])
        scene.render.filepath=str(out/('%04d.png'%frame))
        s['bpy'].ops.render.render(write_still=True)
    print('Rendered',shot['id'])

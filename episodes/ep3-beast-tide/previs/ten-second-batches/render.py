"""Shared meter-scale proxy scene, loaded by render.py through runpy.
No render loop or command-line entry here. Animation is driven by render.py;
reusable action timing lives in timeline.json. Blender 4.3.2.
"""
import argparse
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

rng = random.Random(888)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.fps = 24
scene.render.film_transparent = False
sh = scene.display.shading
sh.light = 'STUDIO'
sh.studiolight_rotate_z = 0.4
sh.color_type = 'MATERIAL'
sh.show_shadows = True
sh.show_cavity = True
sh.cavity_type = 'BOTH'
sh.curvature_ridge_factor = 1.3
sh.curvature_valley_factor = 1.1
sh.show_specular_highlight = True
sh.background_type = 'WORLD'
scene.world.color = (0.12, 0.15, 0.19)
scene.view_settings.view_transform = 'Standard'

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    return m

rock = material('Titan dark rock proxy', (0.19, .21, .24))
rock_light = material('Titan shoulder plates', (.27, .29, .32))
red = material('Titan red identity markers', (.75, .05, .025))
armor = material('Aegis gunmetal proxy', (.12, .19, .25))
gold = material('Aegis orange markers', (1, .40, .035))
shieldmat = material('Shield gold timing proxy', (1, .66, .08))
cyan = material('Aegis visor', (.05, .85, 1))
white = material('Impact and displacement', (1, 1, 1))
airmat = material('Air compression guide', (.58, .78, .84))
concrete = material('Concrete', (.44, .48, .52))
slabmat = material('Slabs', (.32, .36, .40))
windows = material('Window voids', (.07, .11, .14))
groundmat = material('Street', (.18, .22, .26))
dustmat = material('Dust proxy', (.43, .40, .36))

def finish(obj, name, mat, parent=None):
    obj.name = name
    obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj

def empty(name):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    return o

def box(name, loc, dims, mat, parent=None, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = finish(bpy.context.object, name, mat, parent)
    o.scale = dims
    if bevel:
        mod = o.modifiers.new('Soft edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 1
    return o

def ball(name, loc, dims, mat, parent=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=loc)
    o = finish(bpy.context.object, name, mat, parent)
    o.scale = dims
    return o

def rod(name, a, b, radius, mat, parent=None, end_radius=None):
    a, b = Vector(a), Vector(b)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=radius,
                                  radius2=radius if end_radius is None else end_radius,
                                  depth=1, location=(a+b)/2)
    o = finish(bpy.context.object, name, mat, parent)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = (b-a).to_track_quat('Z', 'Y')
    o.scale.z = (b-a).length
    return o

def move_rod(o, a, b):
    a, b = Vector(a), Vector(b)
    o.location = (a+b)/2
    o.rotation_quaternion = (b-a).to_track_quat('Z', 'Y')
    o.scale.z = (b-a).length

def curve(name, pts, radius, mat, parent=None):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = radius
    data.bevel_resolution = 1
    poly = data.splines.new('POLY')
    poly.points.add(len(pts)-1)
    for p, xyz in zip(poly.points, pts):
        p.co = (*xyz, 1)
    o = bpy.data.objects.new(name, data)
    scene.collection.objects.link(o)
    return finish(o, name, mat, parent)


def camera(name, loc, target, width):
    bpy.ops.object.camera_add(location=loc)
    o=bpy.context.object
    o.name=name
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='ORTHO'
    o.data.ortho_scale=width
    return o


# EP3 first twenty seconds: north=-X, south=+X, west=-Y.
scene.display.render_aa='8'
scene.world.color=(.085,.095,.12)
box('Avenue',(0,0,-.2),(85,72,.4),groundmat)
for y in [-7,7]:box('Curb',(0,y,.1),(80,.2,.2),concrete)
for x in range(-36,35,5):box('Lane marker',(x,0,.015),(2,.12,.03),white)
for x in [-29,-17,-5,7,19,31]:
    for y in [-28,28]:
        h=rng.uniform(36,52)
        tower=box('Tower',(x,y,h/2),(7,7,h),slabmat);tower.hide_render=y<0
        for z in range(2,int(h),4):
            for dx in [0]:
                pane=box('Window',(x+dx,y+(3.51 if y<0 else -3.51),z),(5.3,.04,2),windows);pane.hide_render=y<0
box('Intact elevated bridge',(-14,0,11.6),(3.5,36,.8),concrete)
for y in [-8,8]:box('Bridge support',(-14,y,5.5),(1,1.3,11),slabmat)
for x,y in [(-20,5),(-9,-5),(12,-5),(16,5)]:
    box('Abandoned car',(x,y,.6),(3.8,1.7,1.2),rock)
    box('Car cabin',(x+.1,y,1.25),(1.6,1.5,.5),windows)
ball('Red moon',(-48,4,39),(7,7,7),red)
box('West firing platform',(1,-7,1),(6,4,2),concrete)
for x,z in [(4,.25),(3.5,.65),(3,1.1),(2.5,1.6)]:box('Platform step',(x,-5,z/2),(1,1,z),concrete)
for x,y in [(9,4),(11,1.8)]:box('South medical cover',(x,y,.65),(2.3,.5,1.3),concrete)
# Aegis model: local feet at z=0; head top at z=1.88.
hero=empty('Aegis_1.88m')
for y in [-.18,.18]:
    box('Aegis boot',(-.06,y,.06),(.42,.20,.12),armor,hero)
    rod('Aegis shin',(0,y,.16),(.03,y,.50),.11,armor,hero)
    ball('Aegis knee',(-.04,y,.53),(.12,.13,.12),gold,hero)
    rod('Aegis thigh',(.03,y,.58),(0,y,.95),.14,armor,hero)
box('Aegis pelvis',(0,0,.98),(.32,.43,.25),armor,hero,bevel=.08)
box('Aegis torso',(0,0,1.30),(.36,.58,.52),armor,hero,bevel=.10)
ball('Aegis furnace',(-.20,0,1.34),(.045,.105,.105),gold,hero)
ball('Aegis helmet',(0,0,1.73),(.16,.17,.15),armor,hero)
box('Aegis cyan visor',(-.15,0,1.76),(.035,.28,.055),cyan,hero)
for y in [-.39,.39]:
    ball('Aegis shoulder',(0,y,1.49),(.22,.21,.19),armor,hero)
rod('Aegis left upper arm',(0,-.39,1.45),(.18,-.55,1.15),.10,armor,hero)
rod('Aegis left forearm',(.18,-.55,1.15),(.12,-.65,.94),.085,armor,hero)
rod('Aegis right upper arm',(0,.39,1.45),(.04,.53,1.15),.11,armor,hero)
rod('Aegis right forearm',(.04,.53,1.15),(-.38,.49,1.28),.11,armor,hero)
box('Right forearm emitter',(-.30,.49,1.28),(.24,.22,.24),gold,hero)
jets=[]
for y in [-.18,.18]:
    jets.append(rod('Foot jet',(0,y,-1.15),(0,y,-.03),.025,white,hero,end_radius=.12))
shieldroot=empty('Right forearm shield')
shieldroot.parent=hero
shieldroot.location=(-.47,.45,1.30)
points=[(0,.78*math.cos(i*math.pi/3),.92*math.sin(i*math.pi/3)) for i in range(7)]
shieldparts=[curve('Shield outline',points,.055,shieldmat,shieldroot)]
for i in range(6):
    shieldparts.append(curve('Shield spoke',[(0,0,0),points[i]],.018,gold,shieldroot))
for y,z in [(-.30,0),(0,.35),(0,-.35),(.30,0)]:
    hp=[(0,y+.19*math.cos(i*math.pi/3),z+.19*math.sin(i*math.pi/3)) for i in range(7)]
    shieldparts.append(curve('Shield honeycomb',hp,.018,shieldmat,shieldroot))

for j in jets:j.hide_render=True
purple=material('Nyx purple',(.20,.09,.30));magenta=material('Nyx energy',(.90,.08,.9))
teal=material('Lyra teal',(.045,.27,.26));green=material('Repair green',(.12,1,.5))
friendmat=material('Wounded ally blue gray',(.25,.33,.42))

def clone_actor(name,bodymat,energymat,scale):
    root=empty(name);mapping={hero:root}
    for old in hero.children_recursive:
        if old in jets or old==shieldroot or old in shieldroot.children_recursive:continue
        new=old.copy()
        if old.data:new.data=old.data.copy()
        scene.collection.objects.link(new);new.name=name+' '+old.name
        new.parent=mapping.get(old.parent,root);mapping[old]=new
        if getattr(new,'data',None) and hasattr(new.data,'materials'):
            for i,mat in enumerate(new.data.materials):
                new.data.materials[i]=energymat if mat in (gold,cyan,shieldmat) else bodymat
    root.scale=scale
    return root
nyx=clone_actor('Nyx',purple,magenta,(.80,.80,.96))
lyra=clone_actor('Lyra',teal,green,(.76,.76,.94))
wounded=clone_actor('Wounded ally',friendmat,cyan,(.9,.9,.96))
rod('Nyx helmet crest',(0,0,1.85),(.08,0,2.25),.045,purple,nyx,end_radius=.01)
box('Lyra armored hood',(.04,0,1.75),(.40,.43,.40),teal,lyra,bevel=.07)
box('Lyra hood visor',(-.18,0,1.76),(.035,.27,.12),green,lyra)
for y in [-.38,.38]:box('Lyra long skirt',(.12,y,.68),(.22,.12,.65),teal,lyra)
barrel=rod('Nyx cannon barrel',(0,0,0),(-1,0,0),.14,purple)
beam=rod('Nyx beam',(0,0,0),(-1,0,0),.035,magenta)
heal=[]
for i in range(3):heal.append(curve('Repair filament',[(0,0,0),(1,0,0),(2,0,0)],.013,green))
bladepivot=empty('Right arm energy dao');bladepivot.parent=hero;bladepivot.location=(-.38,.49,1.28)
verts=[(0,-.05,0),(-1.55,-.05,-.11),(-1.8,-.05,.08),(-.3,-.05,.22),(0,.05,0),(-1.55,.05,-.11),(-1.8,.05,.08),(-.3,.05,.22)]
mesh=bpy.data.meshes.new('Broad dao mesh');mesh.from_pydata(verts,[],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]);mesh.update()
blade=bpy.data.objects.new('Energy dao blade',mesh);scene.collection.objects.link(blade);finish(blade,blade.name,shieldmat,bladepivot)
impact=ball('Shield contact proxy',(-.8,0,1),(.18,.35,.35),white)
slashflash=ball('Dao contact proxy',(-1,0,.9),(.2,.3,.3),gold)

beasts=[]
for i in range(18):
    b=empty('Small beast %02d'%i)
    ball('Beast torso',(0,0,.7),(.72,.36,.4),rock,b)
    ball('Beast head',(.7,0,.85),(.32,.28,.3),rock_light,b)
    for y in [-.18,.18]:
        ball('Beast red eye',(.97,y,.95),(.04,.06,.05),red,b)
        rod('Beast horn',(.65,y,1.04),(.35,y,1.42),.08,rock,b,end_radius=.01)
    rod('Beast tail',(-.6,0,.8),(-1.25,0,.9),.10,rock,b,end_radius=.01)
    legs=[]
    for x in [-.45,.4]:
        for y in [-.3,.3]:
            leg=rod('Beast leg',(x,y,.7),(x+.12,y,.1),.085,rock,b);legs.append((leg,x,y))
    beasts.append((b,legs))
puddle=ball('Puddle',(-2,0,.015),(2,1,.015),windows)
ripples=[]
for i in range(3):ripples.append(curve('Ground ripple',[(math.cos(j*math.pi/24),math.sin(j*math.pi/24),0) for j in range(49)],.012,cyan))
stones=[]
for i in range(14):
    loc=(rng.uniform(-5,0),rng.uniform(-2,2),.08);o=ball('Loose fragment',loc,(.12,.09,.08),concrete);stones.append((o,loc))
cam=camera('Timeline camera',(12,-18,10),(-8,0,3),34)

def clamp(x,a=0,b=1):return max(a,min(b,x))
def look(loc,target,width):
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=width;scene.camera=cam

def animate(t,segment):
    hero.location=(.45*clamp((t-7)*5),0,0)
    hero.rotation_euler=(0,-.12*max(0,1-abs(t-7.1)*5),0)
    if 13.05<t<13.5:hero.rotation_euler.z=.3*math.sin((t-13.05)/.45*math.pi)
    shield_on=5.2<=t<12.4
    for o in shieldparts:o.hide_render=not shield_on
    v=max(.03,clamp((t-5.2)/.2));shieldroot.scale=(1,v,v)
    blade.hide_render=t<12.6
    bladepivot.rotation_euler.y=-.6
    if 13.15<t<13.4:bladepivot.rotation_euler.y=-1.05+clamp((t-13.15)/.25)*2.1
    elif t>=13.4:bladepivot.rotation_euler.y=.8
    for o in jets:o.hide_render=True
    u=clamp((t-8.5)/1.5)
    nyx.location=(1,-2-5*u,2*u);nyx.rotation_euler.z=-.45*u
    lyra.location=(4+4*clamp((t-8.5)/3.5)+max(0,t-17.2)*.25,2,0);lyra.rotation_euler.z=math.pi
    wounded.location=(9+max(0,t-17.2)*.25,3,-.45);wounded.rotation_euler.y=.18
    impact.hide_render=not(7<=t<7.125)
    impact.location=(-.55+hero.location.x,.45,1.2)
    slashflash.hide_render=not(13.30<=t<13.425)
    slashflash.location=(-1.05,.15,1)
    # Run cycles and contact responses are explicit source motions.
    for i,(b,legs) in enumerate(beasts):
        arrival=7+(i//3)*.45+(i%3)*.1
        x=-1.35-(i//3)*2.6-4*max(0,arrival-t)
        if t>=arrival:x=-1.35-(i//3)*2.6-min(2,(t-arrival)*10)
        y=[.45,-1.5,2.4][i%3]+(i//3)*.10
        b.location=(x,y,0);b.rotation_euler=(0,0,0)
        for leg,lx,ly in legs:
            phase=t*14+(0 if lx*ly>0 else math.pi)
            move_rod(leg,(lx,ly,.7),(lx+.25*math.sin(phase),ly,.12+.1*max(0,math.cos(phase))))
        if i in [4,7,10]:
            hit={4:10.5,7:11.1,10:11.7}[i]
            if t>hit:
                a=clamp((t-hit)/.18);b.location.x-=2*a;b.location.z=.15;b.rotation_euler.y=a*.8
        if i==0 and t>=12.4:
            b.location.x=-3.35+2*clamp((t-12.4)/.9)
            if t>=13.3:
                a=clamp((t-13.3)/.22);b.location.x-=3*a;b.rotation_euler.y=a*1.2;b.location.z=.1
        if t>=18.2 and i not in [0,4,7,10]:
            a=clamp((t-18.2)/1.8);b.location.y+=(-1 if i%2 else 1)*4*a;b.rotation_euler.z=(-1 if i%2 else 1)*.7*a
    muzzle_base=Vector(nyx.location)+Vector((-.25,.35,1.35))
    hit_times=[10.5,11.1,11.7,16.2]
    h=min(hit_times,key=lambda x:abs(t-x));idx={10.5:4,11.1:7,11.7:10,16.2:13}[h]
    target=Vector(beasts[idx][0].location)+Vector((.5,0,.8))
    end=muzzle_base+(target-muzzle_base).normalized()*1.5
    move_rod(barrel,muzzle_base,end);move_rod(beam,end,target);beam.hide_render=not(0<=t-h<.0834)
    for i,o in enumerate(heal):
        o.hide_render=not(14.8<=t<17.8)
        a=Vector(lyra.location)+Vector((.35,.2+i*.1,1.15));b=Vector(wounded.location)+Vector((-.1,-.35,1.45))
        pts=o.data.splines[0].points
        for j,v in enumerate([a,(a+b)/2+Vector((0,(i-1)*.15,.15)),b]):pts[j].co=(*v,1)
    for i,o in enumerate(ripples):
        o.hide_render=t<18.2;o.location=(-2,0,.04)
        radius=.2+((max(0,t-18.2)*1.6+i*.55)%1.8);o.scale=(radius,radius*.65,1)
    for i,(o,loc) in enumerate(stones):
        o.location=loc
        if t>18.2:o.location.z+=.04*abs(math.sin(t*30+i))
    # Five shots per ten-second source; fixed axes and persistent world state.
    local=t-(segment-1)*10
    if segment==1:
        if local<2:look((13,-22,15),(-11,0,5),42-2*local)
        elif local<4:
            lead=beasts[0][0].location
            look((lead.x+4,-3,.9),(lead.x+.5,0,.65),5.5)
        elif local<6.5:look((-5,-7,3),(1,0,1.1),10)
        elif local<8.5:look((-4,-5,2.4),(0,0,1),5.4)
        else:look((11,-16,10),(1,-1,1.8),25)
    else:
        if local<2.4:look((-4,-12,4.8),(0,-6.5,3.1),8)
        elif local<5:look((-4,-5,2.5),(-.5,0,1),6.5)
        elif local<7.5:look((12,-3,3.7),(8,2.5,1),8.5)
        elif local<8.7:look((1,-3,1),(-2,0,.15),5.5)
        else:look((10,-18,11),(-7,0,2.5),32)

import argparse
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--segment',type=int,choices=[1,2],required=True);p.add_argument('--frames');opts=p.parse_args(args)
out=Path(opts.output);out.mkdir(parents=True,exist_ok=True)
frames=[int(x) for x in opts.frames.split(',')] if opts.frames else range(243)
for n in frames:
    animate((n+(opts.segment-1)*240)/24,opts.segment)
    scene.render.filepath=str(out/f'{n:04d}.png');bpy.ops.render.render(write_still=True)
print('Rendered segment',opts.segment,'frames',len(frames))

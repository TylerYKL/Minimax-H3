"""Blender 4.3+: procedural combat blocking, meters, 24 fps, 56 frames.
Run: blender -b -t 4 --python build_previs.py -- --output /path/frames
Optional: --frames 0,23,26,28,32,47,55
No downloaded assets; this is an animated timing/layout reference, not an H3 render.
"""
import argparse
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--frames', default='all')
opts = parser.parse_args(args)
out = Path(opts.output)
out.mkdir(parents=True, exist_ok=True)
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

box('Street ground', (0, 0, -.35), (90, 60, .7), groundmat)
for y in (-7, 7):
    box('Street edge', (0, y, .03), (70, .12, .06), concrete)
for x in range(-25, 29, 5):
    box('Road dash', (x, 0, .05), (2, .12, .05), concrete)
for x, y in [(-5, 4), (4, -4), (8, 4), (-17, -5)]:
    box('Four meter car', (x, y, .65), (4, 1.8, 1.3), slabmat, bevel=.08)
    box('Car cabin', (x+.15, y, 1.45), (1.8, 1.6, .55), windows)
for x, y, h in [(-30, 22, 35), (-22, 24, 43), (28, 25, 48), (36, 24, 32)]:
    box('Distant city block', (x, y, h/2), (9, 9, h), slabmat)
    for z in range(3, h, 4):
        box('Distant floor band', (x, y+4.55, z), (8, .08, .15), concrete)
box('Intact highway deck 12m', (-7, 14, 11.65), (40, 4, .7), concrete)
for x in [-24, -12, 0, 12]:
    box('Highway pillar', (x, 14, 5.6), (.8, 1.2, 11.2), slabmat)

# The creature's horn tips reach exactly 30m above ground.
for y in [-2, 2]:
    box('Titan foot', (-11.7, y, .75), (4, 2.5, 1.5), rock, bevel=.10)
    rod('Titan shin', (-12, y, 1.5), (-13, y, 6.3), 1.25, rock)
    ball('Titan knee plate', (-11.7, y, 6.3), (1.2, 1.4, 1.4), rock_light)
    rod('Titan thigh', (-13, y, 6.3), (-12.6, y*.7, 11), 1.7, rock)
ball('Titan pelvis', (-12.6, 0, 11), (2.6, 3, 2.5), rock)
ball('Titan torso', (-12.4, 0, 17.6), (3.0, 4.0, 6.6), rock)
ball('Titan chest core', (-9.55, 0, 18.3), (.18, 1.0, 1.0), red)
for y in [-3.4, 3.4]:
    ball('Titan shoulder', (-12.4, y, 22), (2.7, 2.4, 2.2), rock_light)
ball('Titan head', (-11.7, 0, 26.2), (1.9, 2, 2), rock)
for y in [-1.1, 1.1]:
    rod('Titan horn', (-11.9, y, 27.4), (-12.5, y*1.6, 30), .55, rock, end_radius=0)
    ball('Titan eye', (-9.9, y, 26.8), (.10, .28, .18), red)
for z in range(12, 24, 2):
    rod('Spinal plate', (-14.6, 0, z), (-16, 0, z+.5), .8, rock_light, end_radius=0)
tailpoints=[(-14, 0, 11),(-17, 0, 8),(-20, 0, 4),(-23, 0, 2)]
for i in range(3):
    rod('Tail rooted behind pelvis', tailpoints[i], tailpoints[i+1], 1.3-i*.3, rock)
ball('Tail stone hammer', (-23, 0, 2), (1.6, 1.5, 1.5), rock_light)
rod('Resting upper arm', (-12,-3.8,22),(-9,-5,16),1.4,rock)
rod('Resting forearm', (-9,-5,16),(-8,-5,12),1.3,rock)
ball('Resting empty hand', (-8,-5,11.3),(1.1,1.2,1.3),rock)
upper=rod('Striking upper arm',(-12.4,3.4,22),(-8,2.3,15),1.5,rock)
fore=rod('Striking forearm',(-8,2.3,15),(-5,0,11.3),1.25,rock)
palmroot=empty('Animated claw')
ball('Claw palm',(0,0,0),(.9,1.35,1.4),rock,parent=palmroot)
for i,y in enumerate([-.95,-.32,.32,.95]):
    rod('Claw finger',(.25,y,.6),(1.15,y,.4),.32,rock,parent=palmroot)
    rod('Claw curved tip',(1.15,y,.4),(1.5,y,-.15),.23,rock,parent=palmroot,end_radius=.025)
rod('Claw thumb',(-.1,1.1,-.35),(.9,1.65,-.65),.4,rock,parent=palmroot,end_radius=.08)
curve('Forearm red seam',[(0,-.6,.95),(.25,-.15,1.22),(.5,.3,.9)],.055,red,palmroot)

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
airwaves=[]
for radius in [1.45,1.65]:
    pts=[(0,radius*math.cos(i*math.pi/25),radius*math.sin(i*math.pi/25)) for i in range(51)]
    airwaves.append(curve('Air compression timing ring',pts,.018,airmat))

# Breakable 40m ten-floor tower; upper levels are separate rigid proxies.
tower=[]
breach=[]
for floor in range(10):
    group=empty('Tower level %02d'%floor)
    tower.append(group)
    z=floor*4
    box('Floor slab',(16,0,z+.2),(8,10,.4),slabmat,group)
    for x in [12.25,19.75]:
        for y in [-4.75,4.75]:
            box('Column',(x,y,z+2),(.5,.5,4),concrete,group)
    # Window grid and panels, on the face toward the moving hero.
    for y in [-4,-2,0,2,4]:
        pane=box('Window',(12.08,y,z+2),(.10,1.55,2.45),windows,group)
        if floor==2 and abs(y)<=2: breach.append(pane)
        mullion=box('Window mullion',(11.96,y-.90,z+2),(.22,.20,3.6),concrete,group)
        if floor==2 and abs(y)<=2: breach.append(mullion)
        sill=box('Facade sill',(11.95,y,z+.65),(.30,1.8,.7),concrete,group)
        if floor==2 and abs(y)<=2: breach.append(sill)
    box('Side wall',(16,-5,z+2),(8,.3,3.6),concrete,group)
    box('Red vertical landmark',(12.0,4.95,z+2),(.18,.20,3.6),red,group)
box('Flat rooftop',(16,0,40),(8.1,10.1,.35),concrete,tower[-1])
chunks=[]
for i in range(45):
    size=rng.uniform(.12,.65)
    o=box('Impact fragment',(12,0,11),(size,size*.8,size*.6),concrete)
    chunks.append((o,Vector((rng.uniform(-5,-1),rng.uniform(-5,5),rng.uniform(-1,5))),rng.uniform(0,.15)))
dust=[]
for i in range(12):
    o=ball('Dust volume proxy',(12,0,10),(1,1,1),dustmat)
    dust.append((o,Vector((rng.uniform(-1.5,.4),rng.uniform(-2,2),rng.uniform(-1,2)))))
flash=ball('Shield impact flash',(-.40,-.45,11.3),(.25,.45,.45),white)
wallflash=ball('Wall impact flash',(11.75,0,11),(.25,.5,.5),gold)
trail=curve('White displacement trail',[(0,0,11),(1,0,11)],.08,white)

def camera(name, loc, target, width):
    bpy.ops.object.camera_add(location=loc)
    o=bpy.context.object
    o.name=name
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='ORTHO'
    o.data.ortho_scale=width
    return o

cam_a=camera('A_side_contact',(-7,-20,13.6),(-1.8,0,11.2),13)
cam_b=camera('B_overhead_fixed',(-4,-39,55),(0,0,22),72)

def animate(n):
    t=n/24
    # Fast entry in first four frames, then close the remaining gap slowly.
    if n<4: px=-6+1.9*n/4
    elif n<26: px=-4.1+2.05*((n-4)/22)**.72
    else: px=-2.05+min(.25,(n-26)*.025)
    palmroot.location=(px,0,11.3)
    move_rod(fore,(-8,2.3,15),(px-.7,0,11.3))
    hero.rotation_euler=(0,0,0)
    hero.location=(0,0,10)
    if n>=26:
        if n==26: x=.10
        elif n==27: x=.70
        elif n<32: x=1.5+(n-28)*3.2
        else: x=12.6
        hero.location=(x,0,10)
        hero.rotation_euler.y=min(.65,(n-26)*.15)
    for child in hero.children_recursive:
        child.hide_render=n>=33
    for j in jets:j.hide_render=n>=26
    for s in shieldparts:s.hide_render=n<24 or n>=33
    shieldroot.scale=(1,1 if n!=24 else .5,1 if n!=24 else .5)
    flash.hide_render=n not in (26,27)
    flash.scale=(.20,.45,.45) if n==26 else (.12,.30,.30)
    wallflash.hide_render=n not in (32,33)
    for k,a in enumerate(airwaves):
        a.hide_render=not(5<=n<25)
        a.location=(px+1.65+k*.2,0,11.3)
        a.scale=(1,1+.03*math.sin(n),1+.03*math.sin(n))
    trail.hide_render=not(28<=n<=32)
    if not trail.hide_render:
        end=hero.location.x
        p=trail.data.splines[0].points
        p[0].co=(max(.8,end-5),0,11,1)
        p[1].co=(end,0,11,1)
    dt=max(0,(n-32)/24)
    for part in breach: part.hide_render=n>=33
    for i,level in enumerate(tower):
        level.location=(0,0,0);level.rotation_euler=(0,0,0)
        if n>=33 and i>=2:
            # Lower damaged levels buckle first; upper levels descend visibly.
            fall=max(0,dt-max(0,i-3)*.018)
            level.location=(-.20*fall,0,-(4.9*fall*fall+1.0*fall))
            level.rotation_euler.y=-.010*fall
            if i in (2,3):
                level.location.x=-.7*fall
                level.rotation_euler.y=-.08*fall
    for o,v,delay in chunks:
        a=max(0,dt-delay)
        o.hide_render=n<33 or dt<delay
        o.location=Vector((11.8,0,11))+v*a+Vector((0,0,-4.9*a*a))
        o.rotation_euler=(a*2,a*3,a)
    for o,v in dust:
        o.hide_render=n<36
        o.location=Vector((11.8,0,10))+v*dt
        s=max(.01,dt*.7)
        o.scale=(s,s,s)
    scene.camera=cam_a if n<28 else cam_b
    # Subtle one-frame jolt, never a long shake or camera chase.
    cam_a.location.z=13.6+(.08 if n==26 else 0)

frames=range(56) if opts.frames=='all' else [int(x) for x in opts.frames.split(',')]
for n in frames:
    animate(n)
    scene.render.filepath=str(out/('%04d.png'%n))
    bpy.ops.render.render(write_still=True)
print('Rendered frames:',len(frames),'Output:',out)

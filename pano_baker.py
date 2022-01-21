import bpy
import time
import os
from math import pi


def e2d(float_value):
    fac = 180/pi
    return (float_value/fac)


def setup_panorender():
    context = bpy.context
    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 1
    scene.cycles.max_bounces = 1
    scene.cycles.bake_type = 'DIFFUSE'
    scene.render.bake.use_pass_color = True
    scene.render.bake.use_pass_direct = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.use_selected_to_active = False
    scene.render.bake.use_cage = False
    #scene.render.bake.cage_extrusion = 0.1
    scene.render.bake.use_clear = True
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.resolution_x = 8192
    scene.render.resolution_y = scene.render.resolution_x/2
    scene.render.resolution_percentage = 100
    scene.render.use_overwrite = False


def render_pano(pano_index):
    #ob = pano_ob_in_list
    context = bpy.context
    scene = context.scene
    pano_list = scene.pano_list
    camera_ob = bpy.data.objects["CAM_"+pano_list[pano_index].name]
    camera_ob.rotation_euler[0] = e2d(90)
    camera_ob.rotation_euler[1] = e2d(0)
    camera_ob.rotation_euler[2] = e2d(0)

    scene.camera = camera_ob
    #bpy.ops.view_pano(group_un_idx = pano_index)
    #bpy.ops.render.render(use_viewport = True)

    pano_name = pano_list[pano_index].name

    previous_alpha = bpy.data.objects[pano_name].material_slots[
        0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value
    bpy.data.objects[pano_name].material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.0

    basepath = "D:\QSYNC\SegniProject\Immagini360\Attuale\8k\ "
    if not os.path.exists(os.path.join(basepath+pano_name+".jpg")):
        scene.render.filepath = os.path.join(basepath+pano_name+".jpg")
        bpy.ops.render.render(write_still=1)
    #bpy.data.objects[pano_name].material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value = previous_alpha
    bpy.data.objects[pano_name].material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.68

    #bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, use_selected_to_active=False, use_clear=True, save_mode='INTERNAL')


setup_panorender()
tot_time = 0
start_time = time.time()
pano_index = 0
pano_list = bpy.context.scene.pano_list
ob_counter = 1
tot_pano = len(pano_list)

while pano_index < tot_pano:

    print('start baking "'+pano_list[pano_index].name +
          '" (object '+str(ob_counter)+'/'+str(tot_pano)+')')

    render_pano(pano_index)

    ob_counter += 1
    pano_index += 1
    print("--- %s seconds ---" % (time.time() - start_time))

tot_time += (time.time() - start_time)
print("--- JOB complete in %s seconds ---" % tot_time)

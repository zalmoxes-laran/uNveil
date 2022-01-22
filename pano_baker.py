import bpy
import time
import os
from math import pi
from bpy.types import Panel
from bpy.types import Operator
from bpy.props import (BoolProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty,
                       IntProperty
                       )

from .functions import e2d

#def e2d(float_value):
#    fac = 180/pi
#    return (float_value/fac)

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
    scene.render.resolution_x = scene.bake_res_out
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

    #basepath = "D:\QSYNC\SegniProject\Immagini360\Attuale\8k\ "
    basepath = scene.unveil_dir_bake_output
    pano_name_with_res = pano_name+"-" + str(scene.bake_res_out)[:1] + "k-m"
    if not os.path.exists(os.path.join(basepath+pano_name_with_res+".jpg")) or scene.bake_overwrite:
        scene.render.filepath = os.path.join(
            basepath+pano_name_with_res+".jpg")
        bpy.ops.render.render(write_still=1)
    #bpy.data.objects[pano_name].material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value = previous_alpha
    bpy.data.objects[pano_name].material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.68

    #bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, use_selected_to_active=False, use_clear=True, save_mode='INTERNAL')

class OT_render_pano_operator(bpy.types.Operator):
    """Bake to disk active panorama list"""
    bl_idname = "render.pano"
    bl_label = "Bake panorama"
    bl_description = "Bake to disk active panorama list"
    bl_options = {'REGISTER', 'UNDO'}

    group_un_idx: IntProperty()

    def execute(self, context):
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
            if pano_list[pano_index].publish_item:
                render_pano(pano_index)

            ob_counter += 1
            pano_index += 1
            print("--- %s seconds ---" % (time.time() - start_time))

        tot_time += (time.time() - start_time)
        print("--- JOB complete in %s seconds ---" % tot_time)

        return {'FINISHED'}

class pano_bakerToolsPanel:
    bl_label = "Pano Baker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        #obj = context.active_object
        #resolution_pano = scene.RES_pano

        row = layout.row()
        row.operator("render.pano", icon="TEXTURE_DATA",
                             text='Bake to disk')
        row.prop(context.scene, 'bake_res_out', toggle=True)
        row.prop(scene, 'bake_overwrite', text="Overwrite")
        row = layout.row()

        row.prop(context.scene, 'unveil_dir_bake_output', toggle=True, text="")
        

        #if scene.pano_list_index >= 0 and len(scene.pano_list) > 0:

        #    row = layout.row()
        #    row.label(text="Name:")
        #    row = layout.row()
        #    row.prop(item, "name", text="")


class VIEW3D_PT_pano_baker_SetupPanel(Panel, pano_bakerToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_pano_baker_SetupPanel"
    #bl_context = "objectmode"


classes = [
    OT_render_pano_operator,
    VIEW3D_PT_pano_baker_SetupPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.Scene.epoch_list = CollectionProperty(type=EPOCHListItem)
    #bpy.types.Scene.epoch_list_index = IntProperty(
    #    name="Index for my_list", default=0)
    bpy.types.Scene.unveil_dir_bake_output = StringProperty(
        name="Path to baked panoramas",
        default="",
        description="Define the path to the directory to export the baked pano",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.bake_res_out = IntProperty(
        name="Resolution for bake", default=0)

    bpy.types.Scene.bake_overwrite = BoolProperty(
        name="Bake",
        default=False,
        description="Overwrite files with bake"
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    #del bpy.types.Scene.epoch_list
    #del bpy.types.Scene.epoch_list_index
    del bpy.types.Scene.unveil_dir_bake_output
    del bpy.types.Scene.bake_res_out
    del bpy.types.Scene.bake_overwrite

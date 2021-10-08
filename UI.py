import bpy
import mathutils

from bpy.types import Panel
from bpy.types import Operator
from bpy.types import PropertyGroup
from bpy.types import Menu, UIList

from .functions import *
#from . import report_data
from . import addon_updater_ops

import os
from bpy_extras.io_utils import ImportHelper, axis_conversion

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

# class ToolsPanelImport:
#     bl_label = "Import"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'

#     def draw(self, context):
#         layout = self.layout
#         obj = context.object

#         row = layout.row()
#         self.layout.operator("import_panorami.txt", icon="STICKY_UVS_DISABLE", text='import pano(s)')

        #self.layout.operator("import_cam.agixml", icon="DUPLICATE", text='Agisoft xml cams')

# class ToolsPanelExport:
#     bl_label = "Exporters"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout
#         obj = context.object
#         row = layout.row()
#         if obj is not None:
#             self.layout.operator("export.coordname", icon="STICKY_UVS_DISABLE", text='Coordinates')
#             row = layout.row()

#             box = layout.box()
#             row = box.row()
#             row.label(text= "Export object(s) in one file:")
#             row = box.row()
#             row.operator("export.object", icon="OBJECT_DATA", text='obj')
#             #row = box.row()
#             row.operator("fbx.exp", icon="OBJECT_DATA", text='fbx')
#             row = box.row()
#             row.label(text= "-> "+obj.name + ".obj/.fbx")

#             box = layout.box()
#             row = box.row()
#             row.label(text= "Export objects in several files:")
#             row = box.row()
#             row.operator("obj.exportbatch", icon="DUPLICATE", text='obj')
#             row.operator("fbx.exportbatch", icon="DUPLICATE", text='fbx')
#             row.operator("gltf.exportbatch", icon="DUPLICATE", text='gltf')
#             row.operator("glb.exportbatch", icon="DUPLICATE", text='glb')
#             row = box.row()
#             if not bpy.context.scene.FBX_export_dir:
#                 row.label(text= "-> /objectname.obj")
#                 row = box.row()
#                 row.label(text= "-> /FBX/objectname.fbx")
#             row = box.row()
#             row.prop(context.scene, 'FBX_export_dir', toggle = True, text='Export to')
#         else:
#             row.label(text="Select object(s) to see tools here.")
#             row = layout.row()

class ToolsPanelSHIFT:
    bl_label = "Shifting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        #addon_updater_ops.check_for_update_background()
        layout = self.layout
        scene = context.scene
        obj = context.object

        row = layout.row()
        row.label(text="Shift values:")
        row.operator("shiftval_from.txtfile", icon="STICKY_UVS_DISABLE", text='import')
        row = layout.row()
        row.prop(context.scene, 'BL_x_shift', toggle = True)
        row = layout.row()
        row.prop(context.scene, 'BL_y_shift', toggle = True)
        row = layout.row()
        row.prop(context.scene, 'BL_z_shift', toggle = True)
        row = layout.row()
        row.prop(context.scene, 'BL_epsg', toggle = True)
        row = layout.row()        

        # if scene['crs x'] is not None and scene['crs y'] is not None:
        #     if scene['crs x'] > 0 or scene['crs y'] > 0:
        #         self.layout.operator("shift_from.blendergis", icon="PASTEDOWN", text='from Bender GIS')

        addon_updater_ops.update_notice_box_ui(self, context)

# class VIEW3D_PT_un_Import_ToolBar(Panel, ToolsPanelImport):
#     bl_category = "uNveil"
#     bl_idname = "VIEW3D_PT_un_Import_ToolBar"
#     bl_context = "objectmode"

# class VIEW3D_PT_un_Export_ToolBar(Panel, ToolsPanelExport):
#     bl_category = "uNveil"
#     bl_idname = "VIEW3D_PT_un_Export_ToolBar"
#     bl_context = "objectmode"

class VIEW3D_PT_un_Shift_ToolBar(Panel, ToolsPanelSHIFT):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_un_Shift_ToolBar"
    bl_context = "objectmode"

class Res_menu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_Res_menu"

    def draw(self, context):
        res_list = context.scene.resolution_list
        idx = 0
        layout = self.layout
        while idx < len(res_list):
            op = layout.operator(
                    "set.pano_res", text=str(res_list[idx].res_num), emboss=False, icon="RIGHTARROW")
            op.res_number = str(res_list[idx].res_num)
            idx +=1

class PANOToolsPanel:
    bl_label = "Panorama suite"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        resolution_pano = scene.RES_pano

        row = layout.row()
        row.label(text="POV")
        row.operator("import_panorami.txt", icon="STICKY_UVS_DISABLE", text='import')
        row = layout.row()
        row.prop(context.scene, 'PANO_file', toggle = True)
        row = layout.row()
        row.prop(context.scene, 'PANO_dir', toggle = True)
        row = layout.row()
        self.layout.operator("import.pano", icon="GROUP_UVS", text='Read/Refresh PANO file')

        if context.active_object:
            if obj.type not in ['MESH']:
                select_a_mesh(layout)
            else:
                row = layout.row()
                split = layout.split()
                col = split.column()
                col.operator("ubermat_create.pano", icon="MATERIAL", text='')
                col = split.column()
                col.operator("ubermat_update.pano", icon="MATERIAL", text='')
                row = layout.row()

                #split = layout.split()
                #col = split.column()

                if len(scene.resolution_list) > 0:
                    row = layout.row()
                    row.menu(Res_menu.bl_idname, text=str(resolution_pano), icon='COLOR')

                #col.prop(context.scene, 'RES_pano', toggle = True)
                #col = split.column()
                #col.operator("set.panores", icon="NODE_COMPOSITING", text='')
                row = layout.row()

                row = layout.row(align=True)
                split = row.split()
                col = split.column()
                col.label(text="Display mode")
                col = split.column(align=True)

                #col.menu(Res_mode_menu.bl_idname, text=str(context.scene.RES_pano), icon='COLOR')

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("PANO_UL_List", "PANO nodes", scene, "pano_list", scene, "pano_list_index")

        if scene.pano_list_index >= 0 and len(scene.pano_list) > 0:
            current_pano = scene.pano_list[scene.pano_list_index].name
            item = scene.pano_list[scene.pano_list_index]
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")

        if context.active_object:
            if obj.type in ['MESH']:
                if obj.material_slots:
                    if obj.material_slots[0].material.name.endswith('uberpano'):
                        row = layout.row()
                        node = get_cc_node_pano(obj, current_pano)
                        row.label(text=node.name)# + nodegroupname)
                        layout.context_pointer_set("node", node)
                        node.draw_buttons_ext(context, layout)

        row = layout.row()
        self.layout.operator("view.pano", icon="ZOOM_PREVIOUS", text='Inside the Pano')
        row = layout.row()
        self.layout.operator("remove.pano", icon="ERROR", text='Remove the Pano')
        row = layout.row()
        self.layout.operator("align.quad", icon="OUTLINER_OB_FORCE_FIELD", text='Align quad')
        row = layout.row()
        split = layout.split()
        # First column
        col = split.column()
        col.label(text="Lens:")
        col.prop(context.scene, 'PANO_cam_lens', toggle = True)
        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Apply")
        col.operator("set.lens", icon="FILE_TICK", text='SL')

class VIEW3D_PT_un_SetupPanel(Panel, PANOToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_un_SetupPanel"
    #bl_context = "objectmode"

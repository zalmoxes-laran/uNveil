import bpy
import mathutils

from bpy.types import Panel
from bpy.types import Operator
from bpy.types import PropertyGroup
from bpy.types import Menu, UIList

from .functions import *
#from . import report_data
from . import addon_updater_ops
from .external_modules_install import *

import os
from bpy_extras.io_utils import ImportHelper, axis_conversion

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

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
        row.operator("export.coordshift", icon="STICKY_UVS_DISABLE", text='export')
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

class VIEW3D_PT_un_Shift_ToolBar(Panel, ToolsPanelSHIFT):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_un_Shift_ToolBar"
    bl_context = "objectmode"

class Res_menu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_Res_menu"

    def draw(self, context):
        res_list = context.scene.resolution_list
        layout = self.layout
        idx = 0
        while idx < len(res_list):
            op = layout.operator(
                    "set.panorama_res", text=str(res_list[idx].res_num), emboss=False, icon="RIGHTARROW")
            op.res_number = str(res_list[idx].res_num)
            op.index_number = res_list[idx].res_num
            idx +=1
            
class PANOToolsPanel:
    bl_label = "POV manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        resolution_pano = scene.RES_pano

        row = layout.row()
        row.label(text="Import")
        row.operator("import_panorami.txt", icon="STICKY_UVS_DISABLE", text='')
        row = layout.row()
        #row.prop(context.scene, 'PANO_file', toggle = True)
        #row = layout.row()
        #row.prop(context.scene, 'PANO_dir', toggle = True)
        #row = layout.row()
        #self.layout.operator("import.pano", icon="GROUP_UVS", text='Read/Refresh PANO file')

        if context.active_object:
            if obj.type not in ['MESH']:
                select_a_mesh(layout)
            else:
                row = layout.row()
                
                ## PORZIONE DI CODICE DISATTIVATA TEMPORANEAMENTE PER TESTING. LO REINSERISCO PIU' AVANTI
                #split = layout.split()
                #col = split.column()
                #col.operator("ubermat_create.pano", icon="MATERIAL", text='')
                #col = split.column()
                #col.operator("ubermat_update.pano", icon="MATERIAL", text='')
                ## FINE PORZIONE DI TESTO DISATTIVATA

                row = layout.row()

                #split = layout.split()
                #col = split.column()

                if len(scene.resolution_list) > 0:
                    row = layout.row()
                    row.label(text="Set pano res:")
                    row.menu(Res_menu.bl_idname, text=str(resolution_pano)+"k", icon='COLOR')
                    row.prop(scene, 'RES_propagato_su_tutto', text="All")

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
            op = row.operator("set.panoname", icon="DISC", text="")
            
            op.index_number = scene.pano_list_index
            #row = layout.row()
            #row.prop(context.scene, 'BL_x_shift', toggle = True)

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
 
class ToolsPanelMetadata:
    bl_label = "Metadata manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        #resolution_pano = scene.RES_pano

        row = layout.row()
        row.label(text="Activate service")
        #row.operator("activate.spreadsheetservice", icon="STICKY_UVS_DISABLE", text='')
        row = layout.row()
        row.label(text="Update modules")
        row.operator("install_missing.modules", icon="STICKY_UVS_DISABLE", text='')

class VIEW3D_PT_metadata(Panel, ToolsPanelMetadata):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_metadata"
    #bl_context = "objectmode"





import bpy
import mathutils

from bpy.types import Panel
from bpy.types import Operator
from bpy.types import PropertyGroup

from .functions import *

import os
from bpy_extras.io_utils import ImportHelper, axis_conversion

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

import json
import os
import shutil

import logging
log = logging.getLogger(__name__)

class UN_properties_belonging_ob(bpy.types.PropertyGroup):

    nu: prop.StringProperty(
           name="nu",
           description="Narrative unit",
           default="Untitled")

    pov: prop.StringProperty(
           name="pov",
           description="Point of view",
           default="Untitled")

    epoch: prop.StringProperty(
           name="epoch",
           description="Epoch",
           default="Untitled")

class UN_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, resol_un, index):
        #scene = context.scene
        layout.label(text = item.identificativo, icon = item.icon)

class UNListItem(PropertyGroup):
    """ Group of properties representing an item in the list """

    identificativo : StringProperty(
            name="Identificativo",
            description="An id for this item",
            default="Untitled")

    nome: StringProperty(
        name="Nome",
        description="A name for this item (ITA)",
        default="Untitled")

    icon : StringProperty(
            name="code for icon",
            description="",
            default="GROUP_UVS")

    descrizione: StringProperty(
            name="Descrizione",
            description="A description for this item (ITA)",
            default="Untitled")

    media : StringProperty(
            name="Media",
            description="A media list for this item",
            default="Untitled")

    audio : StringProperty(
            name="Audio",
            description="An audio list for this item",
            default="Untitled")

    time : StringProperty(
            name="Time",
            description="A time list for this item",
            default="Untitled")

    context : StringProperty(
            name="Context",
            description="A list context for this item",
            default="Untitled")

def unlistitem_to_obj(item_in_list):
    obj = bpy.data.objects[item_in_list.name]
    return obj

class UN_import_metadata(bpy.types.Operator):
    '''Narative units are retrieved from a standardized Google Spreadsheet. If the button is grayed out, fill the fields in the Google Spreadsheet setup section'''
    bl_idname = "import.un_metadata"
    bl_label = "Import from Gogle Spreadsheet"
    bl_options = {"REGISTER", "UNDO"}

    
    @classmethod
    def poll(cls, context):
        is_active_button = False
        prefs = context.preferences.addons.get(__package__, None)
        if len(context.scene.g_spreadsheet_id) == 44 and len(context.scene.g_spreadsheet_sheet) > 0 and prefs.preferences.is_google_module:
            is_active_button = True
        return is_active_button
    
    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        clear_list(context, scene.un_list, scene.un_list_index) 
        un_list_index_counter = 0
        # qui inserisco lettore tabella
        from .spreadsheet import init_spreadsheet_service
        values = init_spreadsheet_service(context)
        #print(values)
        # Parse the array:
        for p in values:
            is_record = False
            try:
                code = p[0]
                if p[0].startswith("UN"):
                    is_record = True
                    print(p[0])

            except IndexError:
                pass
            if is_record:
                scene.un_list.add()
                scene.un_list[un_list_index_counter].identificativo = p[0]
                #scene.un_list[un_list_index_counter].context = p[3]
                #scene.un_list[un_list_index_counter].time = p[2]
                try:
                    scene.un_list[un_list_index_counter].nome = p[1]
                except IndexError:
                    scene.un_list[un_list_index_counter].nome = ""
                try:
                    scene.un_list[un_list_index_counter].descrizione = p[4]
                except IndexError:
                    scene.un_list[un_list_index_counter].descrizione = ""
                try:
                    scene.un_list[un_list_index_counter].media = p[5]
                except IndexError:
                    scene.un_list[un_list_index_counter].media = ""
                try:    
                    scene.un_list[un_list_index_counter].audio = p[6]
                except IndexError:
                    scene.un_list[un_list_index_counter].audio = ""

                un_list_index_counter += 1

        return {'FINISHED'}

class REMOVE_un(bpy.types.Operator):
    bl_idname = "remove.un"
    bl_label = "Remove selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        if scene.un_list[scene.un_list_index].name == "Untitled":
            scene.un_list.remove(scene.un_list_index)
            scene.un_list_index = scene.un_list_index - 1            
        else:
            try:
                ob_un = data.objects[scene.un_list[scene.un_list_index].name]
                data.objects.remove(ob_un)
            except:
                pass
            try:
                cam_un = data.objects['CAM_'+scene.un_list[scene.un_list_index].name]
                data.objects.remove(cam_un)
            except:
                pass
            scene.un_list.remove(scene.un_list_index)
            scene.un_list_index = scene.un_list_index - 1
        return {'FINISHED'}

class VIEW_un(bpy.types.Operator):
    bl_idname = "view.un"
    bl_label = "View from the inside of selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        un_list_index = scene.un_list_index
        current_camera_name = 'CAM_'+scene.un_list[un_list_index].name
        current_camera_obj = data.objects[current_camera_name]
        scene.camera = current_camera_obj
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        current_un = data.objects[scene.un_list[un_list_index].name]
        context.view_layer.objects.active = current_un
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

def set_res_mat(mat,res_number ):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == "TEX_IMAGE":
            percorso_e_file = os.path.split(node.image.filepath)
            print(percorso_e_file)
            all_unres_base_directory = os.path.dirname(percorso_e_file[0])
            current_unres_foldername = str(res_number)+"k"
            minimum_sChildPath = os.path.join(all_unres_base_directory,current_unres_foldername,percorso_e_file[1])
            #print(minimum_sChildPath)
            node.image.filepath = minimum_sChildPath

class SETunNAME(bpy.types.Operator):

    bl_idname = "set.unname"
    bl_label = "set the name of the unrama"
    bl_options = {"REGISTER", "UNDO"}

    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        nome_oggetto_da_rinominare = scene.un_list[self.index_number].previous_name
        nuovo_nome_oggetto = scene.un_list[self.index_number].name
        nome_camera_da_rinominare = "CAM_"+nome_oggetto_da_rinominare
        nuovo_nome_camera = "CAM_"+nuovo_nome_oggetto
        
        bpy.data.objects[nome_oggetto_da_rinominare].name = nuovo_nome_oggetto
        bpy.data.objects[nome_camera_da_rinominare].name = nuovo_nome_camera

        # update "previous name"
        scene.un_list[self.index_number].previous_name = scene.un_list[self.index_number].name

        return {'FINISHED'}
            
class UNToolsPanel:
    bl_label = "UN manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        resolution_un = scene.RES_un

        row = layout.row()
        row.label(text="Import")
        row.operator("import.un_metadata", icon="STICKY_UVS_DISABLE", text='')
        row = layout.row()
        '''
        if context.active_object:
            if obj.type not in ['MESH']:
                select_a_mesh(layout)
            else:
                
                row = layout.row()

                row = layout.row(align=True)
                split = row.split()
                col = split.column()
                col.label(text="Display mode")
                col = split.column(align=True)

                #col.menu(Res_mode_menu.bl_idname, text=str(context.scene.RES_un), icon='COLOR')
        '''

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("UN_UL_List", "UN nodes", scene, "un_list", scene, "un_list_index")

        if scene.un_list_index >= 0 and len(scene.un_list) > 0:
            current_un = scene.un_list[scene.un_list_index].name
            item = scene.un_list[scene.un_list_index]
            row = layout.row()
            row.label(text="Id:")
            row = layout.row()
            row.prop(item, "identificativo", text="")
            row = layout.row()
            row.label(text="Nome:")
            row = layout.row()
            row.prop(item, "nome", text="")
            row = layout.row()
            row.label(text="Descrizione:")
            row = layout.row()
            row.prop(item, "descrizione", text="")
            row = layout.row()
            row.label(text="Media:")
            row = layout.row()
            row.prop(item, "media", text="")
            row = layout.row()
            row.label(text="Audio file:")
            row = layout.row()
            row.prop(item, "audio", text="")
            #op = row.operator("set.unname", icon="DISC", text="")
            #op.index_number = scene.un_list_index
    
        #row = layout.row()
        #self.layout.operator("remove.un", icon="ERROR", text='Remove the Pano')
        
class VIEW3D_PT_un_SetupPanel(Panel, UNToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_un_SetupPanel"
    #bl_context = "objectmode"

classes = [
    UNListItem,
    UN_UL_List,
    REMOVE_un,
    VIEW_un,
    UN_import_metadata,
    SETunNAME,
    VIEW3D_PT_un_SetupPanel,
    UN_properties_belonging_ob,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.un_list = CollectionProperty(type = UNListItem)
    bpy.types.Scene.un_list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.resolution_list_index = IntProperty(name = "Index for my_list", default = 0)

    bpy.types.Object.UN_prop_belong_ob = CollectionProperty(type=UN_properties_belonging_ob)
    bpy.types.Object.UN_prop_belong_ob_index = IntProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.UN_prop_belong_ob
    del bpy.types.Object.UN_prop_belong_ob_index
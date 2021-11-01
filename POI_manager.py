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

from .spreadsheet import *

class POI_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, resol_poi, index):
        #scene = context.scene
        layout.label(text = item.identificativo, icon = item.icon)

class POIListItem(PropertyGroup):
    """ Group of properties representing an item in the list """

    identificativo : StringProperty(
            name="Identificativo",
            description="An id for this item",
            default="Untitled")

    icon : StringProperty(
            name="code for icon",
            description="",
            default="GROUP_UVS")

    description : StringProperty(
            name="Description",
            description="A description for this item",
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

def poilistitem_to_obj(item_in_list):
    obj = bpy.data.objects[item_in_list.name]
    return obj

def export_poiscene(scene, export_folder, EMviq, nodes, format_file, edges):
    #EM_list_clear(bpy.context, "emviq_error_list")
    edges["."] = []
    for poi in scene.poi_list:
        exec(poi.name+'_node = {}')
        exec(poilistitem_to_obj(poi).location[0])
        exec("nodes['"+poi.name+"'] = "+ poi.name + '_node')
        poi.name
 
        if len(ob.EM_ep_belong_ob) >= 2:
            for ob_tagged in ob.EM_ep_belong_ob:
                for epoch in scene.epoch_list:
                    if ob_tagged.epoch == epoch.name:
                        epochname1_var = epoch.name.replace(" ", "_")
                        epochname_var = epochname1_var.replace(".", "")

                        if EMviq:
                            try:
                                exec(epochname_var+'_node')
                            except NameError:
                                print("well, it WASN'T defined after all!")
                                exec(epochname_var + '_node' + ' = {}')
                                exec(epochname_var + '_urls = []')
                                exec(epochname_var + "_node['urls'] = "+ epochname_var +"_urls")
                                exec("nodes['"+epoch.name+"'] = "+ epochname_var + '_node')

                                edges["."].append(epoch.name)

                            else:
                                print("sure, it was defined.")

                            exec(epochname_var + '_urls.append("'+utente_aton+'/models/'+progetto_aton+'/shared/'+ ob.name + '.gltf")')

                        ob.select_set(False)
    return nodes, edges

def json_writer(base_dir):
    
    poi_scene = {}
    scenegraph = {}
    nodes = {}
    edges = {}
    
    poi_scene['scenegraph'] = scenegraph
    nodes, edges = export_poiscene(scene, base_dir, True, nodes, self.em_export_format, edges)

    scenegraph['nodes'] = nodes

    # encode dict as JSON 
    data = json.dumps(poi_scene, indent=4, ensure_ascii=True)

    #'/users/emanueldemetrescu/Desktop/'
    file_name = os.path.join(base_dir, "config.json")

    # write JSON file
    with open(file_name, 'w') as outfile:
        outfile.write(data + '\n')

    em_file_4_emviq = os.path.join(export_folder, "em.graphml")

    em_file_fixed_path = bpy.path.abspath(scene.EM_file)
    shutil.copyfile(em_file_fixed_path, em_file_4_emviq)


    return

class POI_import_metadata(bpy.types.Operator):
    '''Narative units are retrieved from a standardized Google Spreadsheet. If the button is grayed out, fill the fields in the Google Spreadsheet setup section'''
    bl_idname = "import.poi_metadata"
    bl_label = "Import from Gogle Spreadsheet"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        is_active_button = False
        if len(context.scene.g_spreadsheet_id) == 44 and len(context.scene.g_spreadsheet_sheet) > 0 and context.preferences.addons['uNveil'].preferences.is_google_module:
            is_active_button = True
        return is_active_button

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        clear_list(context, scene.poi_list, scene.poi_list_index) 
        poi_list_index_counter = 0
        # qui inserisco lettore tabella

        values = init_spreadsheet_service(context)

        # Parse the array:
        for p in values:
            is_record = False
            try:
                code = p[0]
                if p[0].startswith("POI"):
                    is_record = True

            except IndexError:
                pass
            if is_record:
                scene.poi_list.add()
                scene.poi_list[poi_list_index_counter].identificativo = p[0]
                #scene.poi_list[poi_list_index_counter].context = p[3]
                #scene.poi_list[poi_list_index_counter].time = p[2]
                try:
                    scene.poi_list[poi_list_index_counter].name = p[1]
                except IndexError:
                    scene.poi_list[poi_list_index_counter].name = ""
                try:
                    scene.poi_list[poi_list_index_counter].description = p[4]
                except IndexError:
                    scene.poi_list[poi_list_index_counter].description = ""
                try:
                    scene.poi_list[poi_list_index_counter].media = p[5]
                except IndexError:
                    scene.poi_list[poi_list_index_counter].media = ""
                try:    
                    scene.poi_list[poi_list_index_counter].audio = p[6]
                except IndexError:
                    scene.poi_list[poi_list_index_counter].audio = ""
                poi_list_index_counter += 1

        return {'FINISHED'}

class REMOVE_poi(bpy.types.Operator):
    bl_idname = "remove.poi"
    bl_label = "Remove selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        if scene.poi_list[scene.poi_list_index].name == "Untitled":
            scene.poi_list.remove(scene.poi_list_index)
            scene.poi_list_index = scene.poi_list_index - 1            
        else:
            try:
                ob_poi = data.objects[scene.poi_list[scene.poi_list_index].name]
                data.objects.remove(ob_poi)
            except:
                pass
            try:
                cam_poi = data.objects['CAM_'+scene.poi_list[scene.poi_list_index].name]
                data.objects.remove(cam_poi)
            except:
                pass
            scene.poi_list.remove(scene.poi_list_index)
            scene.poi_list_index = scene.poi_list_index - 1
        return {'FINISHED'}

class VIEW_poi(bpy.types.Operator):
    bl_idname = "view.poi"
    bl_label = "View from the inside of selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        poi_list_index = scene.poi_list_index
        current_camera_name = 'CAM_'+scene.poi_list[poi_list_index].name
        current_camera_obj = data.objects[current_camera_name]
        scene.camera = current_camera_obj
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        current_poi = data.objects[scene.poi_list[poi_list_index].name]
        context.view_layer.objects.active = current_poi
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

def set_res_mat(mat,res_number ):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == "TEX_IMAGE":
            percorso_e_file = os.path.split(node.image.filepath)
            print(percorso_e_file)
            all_poires_base_directory = os.path.dirname(percorso_e_file[0])
            current_poires_foldername = str(res_number)+"k"
            minimum_sChildPath = os.path.join(all_poires_base_directory,current_poires_foldername,percorso_e_file[1])
            #print(minimum_sChildPath)
            node.image.filepath = minimum_sChildPath

class SETpoiNAME(bpy.types.Operator):

    bl_idname = "set.poiname"
    bl_label = "set the name of the poirama"
    bl_options = {"REGISTER", "UNDO"}

    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        nome_oggetto_da_rinominare = scene.poi_list[self.index_number].previous_name
        nuovo_nome_oggetto = scene.poi_list[self.index_number].name
        nome_camera_da_rinominare = "CAM_"+nome_oggetto_da_rinominare
        nuovo_nome_camera = "CAM_"+nuovo_nome_oggetto
        
        bpy.data.objects[nome_oggetto_da_rinominare].name = nuovo_nome_oggetto
        bpy.data.objects[nome_camera_da_rinominare].name = nuovo_nome_camera

        # update "previous name"
        scene.poi_list[self.index_number].previous_name = scene.poi_list[self.index_number].name

        return {'FINISHED'}
            
class POIToolsPanel:
    bl_label = "POI manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        resolution_poi = scene.RES_poi

        row = layout.row()
        row.label(text="Import")
        row.operator("import.poi_metadata", icon="STICKY_UVS_DISABLE", text='')
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

                #col.menu(Res_mode_menu.bl_idname, text=str(context.scene.RES_poi), icon='COLOR')
        '''

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("POI_UL_List", "POI nodes", scene, "poi_list", scene, "poi_list_index")

        if scene.poi_list_index >= 0 and len(scene.poi_list) > 0:
            current_poi = scene.poi_list[scene.poi_list_index].name
            item = scene.poi_list[scene.poi_list_index]
            row = layout.row()
            row.label(text="Id:")
            row = layout.row()
            row.prop(item, "identificativo", text="")
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")
            row = layout.row()
            row.label(text="Description:")
            row = layout.row()
            row.prop(item, "description", text="")
            row = layout.row()
            row.label(text="Media:")
            row = layout.row()
            row.prop(item, "media", text="")
            row = layout.row()
            row.label(text="Audio file:")
            row = layout.row()
            row.prop(item, "audio", text="")

            op = row.operator("set.poiname", icon="DISC", text="")
            
            op.index_number = scene.poi_list_index
    
        #row = layout.row()
        #self.layout.operator("remove.poi", icon="ERROR", text='Remove the Pano')
        
class VIEW3D_PT_poi_SetupPanel(Panel, POIToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_poi_SetupPanel"
    #bl_context = "objectmode"

classes = [
    POIListItem,
    POI_UL_List,
    REMOVE_poi,
    VIEW_poi,
    POI_import_metadata,
    SETpoiNAME,
    VIEW3D_PT_poi_SetupPanel
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.poi_list = CollectionProperty(type = POIListItem)
    bpy.types.Scene.poi_list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.resolution_list_index = IntProperty(name = "Index for my_list", default = 0)
    
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
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

class POI_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, resol_poi, index):
        #scene = context.scene
        layout.label(text = item.name, icon = item.icon)

class POIListItem(PropertyGroup):
    """ Group of properties representing an item in the list """

    name : StringProperty(
            name="Name",
            description="A name for this item",
            default="Untitled")

    previous_name : StringProperty(
            name="Name",
            description="Previous name for this item",
            default="Empty")

    original_name : StringProperty(
            name="Name",
            description="Original name for this item",
            default="Empty")

    icon : StringProperty(
            name="code for icon",
            description="",
            default="GROUP_UVS")

    resol_poi : IntProperty(
            name = "Res",
            default = 1,
            description = "Resolution of Panoramic image for this bubble")


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

def clear_poilist():
    data = bpy.data
    context = bpy.context
    scene = context.scene
    #POI_list_clear(context)
    poi_list_index_counter = 0    
    return

class POI_import(bpy.types.Operator):
    bl_idname = "import.poi"
    bl_label = "Import Panoramas from file"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        #minimum_sChildPath, folder_list = read_poi_dir(context)
        read_poi_dir(context)
        lines_in_file = readfile(scene.POI_file)
        # POI_list_clear(context)
        # poi_list_index_counter = 0
        
        # Parse the array:
        for p in lines_in_file:
            #p0 = p.split('\t')  # use space as separator
            p0 = p.split(' ')  # use space as separator
            print(p0[0])
            ItemName = p0[0]
            pos_x = float(p0[1])-scene.BL_x_shift
            pos_y = float(p0[2])-scene.BL_y_shift
            pos_z = (float(p0[3]))-scene.BL_z_shift
            omega = float(p0[4])
            phi = float(p0[5])
            kappa = float(p0[6])

            for model in data.objects:
                if model.name == remove_extension(ItemName) or model.name == "CAM_"+remove_extension(ItemName):
                    data.objects.remove(model)
            sph = bpy.ops.mesh.primitive_uv_sphere_add(calc_uvs=True, radius=0.2, location=(pos_x,pos_y,pos_z))
            just_created_obj = context.active_object
            just_created_obj.name = remove_extension(ItemName)
            
            just_created_obj.rotation_euler[2] = e2d(-90.0)
            bpy.ops.object.transform_apply(rotation = True, location = False)

            #print(f"Il poirama {just_created_obj.name} ha rotazione z: {e2d(180.0+phi)}")
            #just_created_obj.rotation_euler[0] = e2d(-(omega-90.0))
            #just_created_obj.rotation_euler[1] = e2d(kappa)
            #just_created_obj.rotation_euler[2] = e2d(180.0+phi)

            if omega>0:
                just_created_obj.rotation_euler[1] = e2d((omega-90.0))
            else:
                just_created_obj.rotation_euler[1] = e2d(-(omega-90.0))
            just_created_obj.rotation_euler[0] = e2d(-kappa)
            if omega>0:
                just_created_obj.rotation_euler[2] = e2d(180.0+phi)
            else:
                just_created_obj.rotation_euler[2] = e2d(180-phi)

            uvMapName = 'UVMap'
            obj, uvMap = GetObjectAndUVMap( just_created_obj.name, uvMapName )
            scale = Vector( (-1, 1) )
            pivot = Vector( (0.5, 0.5) )
            ScaleUV( uvMap, scale, pivot )

            #ItemName_res = (remove_extension(ItemName)+"-"+str(scene.RES_poi)+"k.jpg")
            ItemName_res = (remove_extension(ItemName)+".jpg")
            current_poires_foldername = str(scene.RES_poi)+"k"
            
            minimum_sChildPath = os.path.join(scene.POI_dir,current_poires_foldername)

            diffTex, img = create_tex_from_file(ItemName_res,minimum_sChildPath)
            mat = create_mat(just_created_obj)
            setup_mat_poirama_3DSC(mat.name, img)
           
            scene.poi_list.add()
            scene.poi_list[poi_list_index_counter].name = just_created_obj.name
            
            flipnormals()
            create_cam(just_created_obj.name,pos_x,pos_y,pos_z)
            poi_list_index_counter += 1
        #scene.update()
        return {'FINISHED'}

class ubermat_create(bpy.types.Operator):
    bl_idname = "ubermat_create.poi"
    bl_label = "Create ubermaterial from poiramas"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        create_poi_ubermat(True)

        return {'FINISHED'}

class ubermat_update(bpy.types.Operator):
    bl_idname = "ubermat_update.poi"
    bl_label = "Update ubermaterial from poiramas"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        create_poi_ubermat(False)
        
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

class VIEW_alignquad(bpy.types.Operator):
    bl_idname = "align.quad"
    bl_label = "align the quad inside the active Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        poi_list_index = scene.poi_list_index
        current_camera_name = 'CAM_'+scene.poi_list[poi_list_index].name
        current_camera_obj = data.objects[current_camera_name]
        #scene.camera = current_camera_obj
        current_poi = data.objects[scene.poi_list[poi_list_index].name]
        object = context.active_object



        set_rotation_to_bubble(context,object,current_camera_obj)

        return {'FINISHED'}

class VIEW_setlens(bpy.types.Operator):
    bl_idname = "set.lens"
    bl_label = "set the lens of the camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        poi_list_index = scene.poi_list_index
        current_camera_name = 'CAM_'+scene.poi_list[poi_list_index].name

        current_camera_obj = data.objects[current_camera_name]
        current_camera_obj.data.lens = scene.POI_cam_lens
        #        scene.camera = current_camera_obj
        #        current_poi = data.objects[scene.poi_list[poi_list_index].name]
        #        object = context.active_object


        #        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        #        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        #
        #        scene.objects.active = current_poi
        #        bpy.ops.object.select_all(action='DESELECT')
        #        current_poi.select = True
        #        set_rotation_to_bubble(context,object,current_camera_obj)

        return {'FINISHED'}

def set_res_mat(mat,res_number ):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == "TEX_IMAGE":
            percorso_e_file = os.path.split(node.image.filepath)
            print(percorso_e_file)
            all_poires_base_directory = os.path.dirname(percorso_e_file[0])
            current_poires_foldername = str(res_number)+"k"
            #ItemName_res = (nodename+"-"+str(self.res_number)+"k.jpg")
            minimum_sChildPath = os.path.join(all_poires_base_directory,current_poires_foldername,percorso_e_file[1])
            #print(minimum_sChildPath)
            node.image.filepath = minimum_sChildPath

class SETpoiRES(bpy.types.Operator):
    bl_idname = "set.poirama_res"
    bl_label = "set the res of the poirama"
    bl_options = {"REGISTER", "UNDO"}

    res_number : StringProperty()
    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        context.scene.RES_poi = self.index_number
        if scene.RES_propagato_su_tutto:
            for poirama_unit in scene.poi_list:
                poirama_unit.name
                mat = bpy.data.objects[poirama_unit.name].material_slots[0].material
                set_res_mat(mat,self.res_number)
        else:
            active_obj = bpy.context.active_object
            mat = active_obj.material_slots[0].material
            set_res_mat(mat,self.res_number)
        return {'FINISHED'}

class RESETpoiNAME(bpy.types.Operator):
    bl_idname = "reset.poiname"
    bl_label = "reset the name of the poirama"
    bl_options = {"REGISTER", "UNDO"}

    res_number : StringProperty()
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


class Res_menu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_Res_menu"

    def draw(self, context):
        res_list = context.scene.resolution_list
        layout = self.layout
        idx = 0
        while idx < len(res_list):
            op = layout.operator(
                    "set.poirama_res", text=str(res_list[idx].res_num), emboss=False, icon="RIGHTARROW")
            op.res_number = str(res_list[idx].res_num)
            op.index_number = res_list[idx].res_num
            idx +=1
            
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
        row.operator("import_poirami.txt", icon="STICKY_UVS_DISABLE", text='')
        row = layout.row()
        #row.prop(context.scene, 'POI_file', toggle = True)
        #row = layout.row()
        #row.prop(context.scene, 'POI_dir', toggle = True)
        #row = layout.row()
        #self.layout.operator("import.poi", icon="GROUP_UVS", text='Read/Refresh POI file')

        if context.active_object:
            if obj.type not in ['MESH']:
                select_a_mesh(layout)
            else:
                row = layout.row()
                
                ## PORZIONE DI CODICE DISATTIVATA TEMPORANEAMENTE PER TESTING. LO REINSERISCO PIU' AVANTI
                split = layout.split()
                col = split.column()
                col.operator("ubermat_create.poi", icon="MATERIAL", text='')
                col = split.column()
                col.operator("ubermat_update.poi", icon="MATERIAL", text='')
                ## FINE PORZIONE DI TESTO DISATTIVATA

                row = layout.row()

                split = layout.split()
                col = split.column()

                if len(scene.resolution_list) > 0:
                    row = layout.row()
                    row.label(text="Set poi res:")
                    row.menu(Res_menu.bl_idname, text=str(resolution_poi)+"k", icon='COLOR')
                    row.prop(scene, 'RES_propagato_su_tutto', text="All")

                #col.prop(context.scene, 'RES_poi', toggle = True)
                #col = split.column()
                #col.operator("set.poires", icon="NODE_COMPOSITING", text='')
                row = layout.row()

                row = layout.row(align=True)
                split = row.split()
                col = split.column()
                col.label(text="Display mode")
                col = split.column(align=True)

                #col.menu(Res_mode_menu.bl_idname, text=str(context.scene.RES_poi), icon='COLOR')

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("POI_UL_List", "POI nodes", scene, "poi_list", scene, "poi_list_index")

        if scene.poi_list_index >= 0 and len(scene.poi_list) > 0:
            current_poi = scene.poi_list[scene.poi_list_index].name
            item = scene.poi_list[scene.poi_list_index]
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")
            op = row.operator("set.poiname", icon="DISC", text="")
            
            op.index_number = scene.poi_list_index
            #row = layout.row()
            #row.prop(context.scene, 'BL_x_shift', toggle = True)

        # if context.active_object:
        #     if obj.type in ['MESH']:
        #         if obj.material_slots:
        #             if obj.material_slots[0].material.name.endswith('uberpoi'):
        #                 row = layout.row()
        #                 node = get_cc_node_poi(obj, current_poi)
        #                 row.label(text=node.name)# + nodegroupname)
        #                 layout.context_pointer_set("node", node)
        #                 node.draw_buttons_ext(context, layout)

        row = layout.row()
        self.layout.operator("view.poi", icon="ZOOM_PREVIOUS", text='Inside the Pano')
        row = layout.row()
        self.layout.operator("remove.poi", icon="ERROR", text='Remove the Pano')
        row = layout.row()
        self.layout.operator("align.quad", icon="OUTLINER_OB_FORCE_FIELD", text='Align quad')
        row = layout.row()
        split = layout.split()
        # First column
        col = split.column()
        col.label(text="Lens:")
        col.prop(context.scene, 'POI_cam_lens', toggle = True)
        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Apply")
        col.operator("set.lens", icon="FILE_TICK", text='SL')

class VIEW3D_PT_poi_SetupPanel(Panel, POIToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_poi_SetupPanel"
    #bl_context = "objectmode"

classes = [
    POIListItem,
    POI_UL_List,
    REMOVE_poi,
    VIEW_poi,
    #VIEW_alignquad,
    #VIEW_setlens,
    #POI_import,
    #ubermat_create,
    #ubermat_update,
    SETpoiRES,
    SETpoiNAME,
    #Res_menu,
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
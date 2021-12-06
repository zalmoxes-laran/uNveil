import bpy

from bpy.types import Panel
from bpy.types import Operator
from bpy.types import PropertyGroup
from bpy.types import UIList

from .functions import *

import os
from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

import json
import os
import shutil

import logging
log = logging.getLogger(__name__)


class UN_contained_in_pov(PropertyGroup):
    """ List of UN """

    un_item: StringProperty(
        name="Name",
        description="name of the UN",
        default="Untitled")


class UN_OT_remove_UN(bpy.types.Operator):
    """Remove UN from POV"""
    bl_idname = "un_models.remove"
    bl_label = "Remove UN from POV"
    bl_description = "Remove UN from POV"
    bl_options = {'REGISTER', 'UNDO'}


    group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        sel_pano = scene.pano_list[scene.pano_list_index]

        sel_pano.un_list.remove(self.group_un_idx)
        #print(f"Ho rimosso il {sel_un.identificativo}")

        return {'FINISHED'}


class UN_OT_add_remove_UN_models(bpy.types.Operator):
    """Add and remove UN to/from POV"""
    bl_idname = "un_models.add_remove"
    bl_label = "Add and remove UN to/from POV"
    bl_description = "Add and remove UN to/from POV"
    bl_options = {'REGISTER', 'UNDO'}

    rm_add : BoolProperty()
    group_un_idx : IntProperty()

    def execute(self, context):
        scene = context.scene
        sel_pano = scene.pano_list[scene.pano_list_index]
        sel_un = scene.un_list[scene.un_list_index]

        #print(sel_pano.un_list.un_item)
        #if len(sel_pano.un_list) > 0:
        if self.rm_add:
            un_ancora_non_presente = True

            for list_item in sel_pano.un_list:
                if sel_un.identificativo == list_item.un_item:
                    un_ancora_non_presente = False

            if un_ancora_non_presente:
                sel_pano.un_list.add()
                print(len(sel_pano.un_list)-1)
                sel_pano.un_list[len(sel_pano.un_list)-1].un_item = sel_un.identificativo
                print(f"Added {sel_un.identificativo} to {sel_pano.name}") #{sel_pano.un_list[len(sel_pano.un_list)-1].un_item}")
        
        else:
            counter = 0
            while counter < len(sel_pano.un_list):
                if sel_un.identificativo == sel_pano.un_list[counter].un_item:
                    sel_pano.un_list.remove(counter)
                    print(f"Ho rimosso il {sel_un.identificativo}")
                counter +=1
            
        '''
        selected_objects = context.selected_objects

        for ob in selected_objects:
            if len(ob.EM_ep_belong_ob) >= 0:
                if self.rm_add:
                    if not self.rm_pov in ob.EM_ep_belong_ob:
                        local_counter = len(ob.EM_ep_belong_ob)
                        ob.EM_ep_belong_ob.add()
                        ob.EM_ep_belong_ob[local_counter].epoch = self.rm_pov
                else:
                    counter = 0
                    for ob_list in ob.EM_ep_belong_ob:
                        if ob_list.epoch == self.rm_pov:
                            ob.EM_ep_belong_ob.remove(counter)  
                        counter +=1
            else:
                ob.EM_ep_belong_ob.add()
                ob.EM_ep_belong_ob[0].epoch = self.rm_pov    
        '''               
        return {'FINISHED'}

class OBJECT_OT_PANORAMI(Operator):
    """Import points as empty objects from a txt file"""
    bl_idname = "import_panorami.txt"
    bl_label = "ImportPanorami"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.import_file.pano_data('INVOKE_DEFAULT')

        return {'FINISHED'}

def namefile_from_path(filepath):
        o_filepath_abs = bpy.path.abspath(filepath)
        o_imagedir, o_filename = os.path.split(o_filepath_abs)
        filename = os.path.splitext(o_filename)[0]
        return filename

def create_new_col_from_file_name(filename):
        newcol = bpy.data.collections.new(filename)
        bpy.context.collection.children.link(newcol)
        return newcol

def is_collection(name_col):
        there_is = False
        for coll in bpy.data.collections:
                if coll.name == name_col:
                        there_is = True
        return there_is

def item_panolist_from_ob_name(obname):
    context = bpy.context
    counter = 0
    found = False
    real_name = "None"
    while counter < len(context.scene.pano_list):
        if context.scene.pano_list[counter].original_name == obname:
            found = True
            real_name = context.scene.pano_list[counter].name
            return found, real_name
        counter +=1
    return found, real_name

def read_pano_data(self,context, filepath, shift, name_col, x_col, y_col, z_col, omega_col, phi_col, kappa_col, separator, clear_list):
        data = bpy.data
        scene = context.scene
        #minimum_sChildPath, folder_list = read_pano_dir(context)
        folder_pano_txt_file, file_name_txt = os.path.split(filepath)
        img_pano_folder = read_pano_dir(folder_pano_txt_file)
        lines_in_file = readfile(filepath)
        if clear_list:
            clear_pano_list(context)
        #pano_list_index_counter = 0
        counter = 0
        # Parse the array:
        for p in lines_in_file:                      
                p0 = p.split(separator)  # use separator                         
                ItemName = p0[name_col]
                # check if the separator works
                try:
                        pos_x = float(p0[x_col])-scene.BL_x_shift
                except IndexError:
                        self.report({'ERROR'}, "Uncorrect field separator ?")
                        #print("")
                        return {'FINISHED'}
                pos_y = float(p0[y_col])-scene.BL_y_shift
                pos_z = (float(p0[z_col]))-scene.BL_z_shift
                omega = float(p0[omega_col])
                phi = float(p0[phi_col])
                kappa = float(p0[kappa_col])

                existing_pano = False    
                actual_name = remove_extension(ItemName)
                if not clear_list:
                    for pano in scene.pano_list:
                        if pano.original_name == remove_extension(ItemName):
                            existing_pano = True
                            actual_name = pano.name
                            print(f"{ItemName} esiste già nella lista")
                existing_model = False
                for model in data.objects:
                    if model.name == actual_name or model.name == "CAM_"+actual_name:
                        existing_model = True
                        if clear_list:
                            data.objects.remove(model)

                collection_name = namefile_from_path(filepath) 
                if is_collection(collection_name):
                        if bpy.data.collections[collection_name].users < 0:
                                context.collection.children.link(collection_name)
                else:
                        newcol = create_new_col_from_file_name(collection_name)
                             
                context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[collection_name]
                if not existing_model:
                    sph = bpy.ops.mesh.primitive_uv_sphere_add(calc_uvs=True, radius=0.2, location=(pos_x,pos_y,pos_z))
                    just_created_obj = context.active_object
                    just_created_obj.name = actual_name
                    #context.view_layer.active_layer_collection.collection.objects.unlink(just_created_obj)
                
                    just_created_obj.rotation_euler[2] = e2d(-90.0)
                    bpy.ops.object.transform_apply(rotation = True, location = False)

                    #print(f"Il panorama {just_created_obj.name} ha rotazione z: {e2d(180.0+phi)}")
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
                    
                    context.view_layer.objects.active = just_created_obj
                    
                    uvMapName = 'UVMap'
                    obj, uvMap = GetObjectAndUVMap( just_created_obj.name, uvMapName )
                    scale = Vector( (-1, 1) )
                    pivot = Vector( (0.5, 0.5) )
                    ScaleUV( uvMap, scale, pivot )

                    ItemName_res = (remove_extension(ItemName)+".jpg")
                    current_panores_foldername = str(img_pano_folder)
                    
                    minimum_sChildPath = os.path.join(folder_pano_txt_file,current_panores_foldername)

                    diffTex, img = create_tex_from_file(ItemName_res,minimum_sChildPath)
                    mat = create_mat(just_created_obj)
                    setup_mat_panorama_3DSC(mat.name, img)
                    
                    if not existing_pano:
                        scene.pano_list.add()
                        last_record_index = len(scene.pano_list)-1
                        scene.pano_list[last_record_index].name = scene.pano_list[last_record_index].previous_name = scene.pano_list[
                            last_record_index].original_name = just_created_obj.name
                        scene.pano_list[last_record_index].group_file = collection_name

                    
                    flipnormals(context)
                    create_pano_cam(just_created_obj.name,pos_x,pos_y,pos_z,bpy.data.collections[collection_name])

                #pano_list_index_counter += 1

        return {'FINISHED'}
'''
def read_point_data(context, filepath, shift, name_col, x_col, y_col, z_col, omega_col, phi_col, kappa_col, separator):
    print("running read point file...")
    f = open(filepath, 'r', encoding='utf-8')
    arr=f.readlines()  # store the entire file in a variable
    f.close()
    
    counter = 0

    for p in arr:
        p0 = p.split(separator)  # use separator variable as separator
        ItemName = p0[int(name_col)]
        print(str(ItemName))
        print(str(p0[1]))
        x_coor = float(p0[1])
        y_coor = float(p0[int(y_col)])
        z_coor = float(p0[int(z_col)])
         
        if shift == True:
            shift_x = context.scene.BL_x_shift
            shift_y = context.scene.BL_y_shift
            shift_z = context.scene.BL_z_shift
            x_coor = x_coor-shift_x
            y_coor = y_coor-shift_y
            z_coor = z_coor-shift_z  

        # Generate object at x = lon and y = lat (and z = 0 )
        o = bpy.data.objects.new( ItemName, None )
        if counter == 0:
                newcol = create_new_col_from_file_name(namefile_from_path(filepath))
                counter += 1

        newcol.objects.link(o)
        o.location.x = x_coor
        o.location.y = y_coor
        o.location.z = z_coor
        o.show_name = True

    return {'FINISHED'}
    '''

class ImportCoorPanorami(Operator, ImportHelper):
    """Tool to import panoramas from a txt file"""
    bl_idname = "import_file.pano_data"  # important since its how bpy.ops.import_file.pano_data is constructed
    bl_label = "Import positions"

    # ImportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob: StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    shift: BoolProperty(
            name="Shift world coordinates",
            description="Shift coordinates using the General Shift Value (GSV)",
            default=True,
            )

    clear_previous: BoolProperty(
            name="Clear previous list",
            description="Clear previous list",
            default=False,
            )

    col_name: EnumProperty(
            name="Name",
            description="Column with the name",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='0',
            )
  
    col_x: EnumProperty(
            name="X",
            description="Column with coordinate X",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='1',
            ) 

    col_y: EnumProperty(
            name="Y",
            description="Column with coordinate X",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='2',
            )

    col_z: EnumProperty(
            name="Z",
            description="Column with coordinate X",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='3',
            )     

    col_Omega: EnumProperty(
            name="Omega",
            description="Column with rotation Omega",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='4',
            )

    col_Phi: EnumProperty(
            name="Phi",
            description="Column with rotation Phi",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='5',
            )

    col_Kappa: EnumProperty(
            name="Kappa",
            description="Column with rotation Kappa",
            items=(('0', "Column 1", "Column 1"),
                   ('1', "Column 2", "Column 2"),
                   ('2', "Column 3", "Column 3"),
                   ('3', "Column 4", "Column 4"),
                   ('4', "Column 5", "Column 5"),
                   ('5', "Column 6", "Column 6"),
                   ('6', "Column 7", "Column 7")),
            default='6',
            )

    separator: EnumProperty(
            name="separator",
            description="Separator type",
            items=((',', "comma", "comma"),
                   (' ', "space", "space"),
                   (';', "semicolon", "semicolon"),
                   ('	', "tab", "tab")),
            default='	',
            )

    def execute(self, context):
        return read_pano_data(self,context, self.filepath, self.shift, int(self.col_name), int(self.col_x), int(self.col_y), int(self.col_z), int(self.col_Omega), int(self.col_Phi), int(self.col_Kappa), self.separator, self.clear_previous)

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportCoorPanorami.bl_idname, text="Coordinate Panoramas Import Operator")

    bpy.ops.import_file.pano_data('INVOKE_DEFAULT')

class PANO_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
    #def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pano_element = item
        #scene = context.scene occhio manca questa variabile: resol_pano
        icons_style = 'OUTLINER'
        #layout.label(text = item.name, icon = item.icon)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.9, align=True)
            layout.prop(pano_element, "name", text="",
                        emboss=False, icon=pano_element.icon)

            #icon = '' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "view.pano", text="", emboss=False, icon='VIS_SEL_11')
            op.group_un_idx = index

            icon = 'RESTRICT_VIEW_OFF' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "pov_manager.toggle_publish", text="", emboss=False, icon=icon)
            op.group_un_idx = index
        #self.layout.prop(context.scene, "test_color", text='Detail Color')

class UN_PANO_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        un_element = item
        #scene = context.scene occhio manca questa variabile: resol_pano
        icons_style = 'OUTLINER'
        #layout.label(text = item.name, icon = item.icon)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.9, align=True)
            layout.prop(un_element, "un_item", text="",
                        emboss=False, icon='VIS_SEL_11')
            
            #icon = '' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "un_models.remove", text="", emboss=False, icon='CANCEL')
            op.group_un_idx = index
            
            '''
            icon = 'RESTRICT_VIEW_OFF' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "pov_manager.toggle_publish", text="", emboss=False, icon=icon)
            op.group_un_idx = index
            '''
        #self.layout.prop(context.scene, "test_color", text='Detail Color')

class OT_toggle_publish(bpy.types.Operator):
    """Define if a POV will be published or not"""
    bl_idname = "pov_manager.toggle_publish"
    bl_label = "Toggle Publish"
    bl_description = "Define if a POV will be published or not"
    bl_options = {'REGISTER', 'UNDO'}

    group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        print(str(scene.pano_list_index))
        if self.group_un_idx < len(scene.pano_list):
            print(f"toggle {self.group_un_idx}")
            scene.pano_list[self.group_un_idx].publish_item = not scene.pano_list[self.group_un_idx].publish_item
            print(scene.pano_list[self.group_un_idx].publish_item)
           
            '''
            scene.pano_list[self.group_un_idx]
            # check_same_ids()  # check scene ids
            current_e_manager = scene.pano_list[self.group_un_idx]
            for pov in scene.pano_list:
                if pov.icon == "RESTRICT_INSTANCED_OFF":
                    if current_e_manager.name == us.epoch:
                        object_to_select = bpy.data.objects[us.name]
                        object_to_select.select_set(True)
            '''
        return {'FINISHED'}

class PANOListItem(PropertyGroup):
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
    
    publish_item: BoolProperty(
            name="code for icon",
            description="",
            default=False)

    resol_pano : IntProperty(
            name = "Res",
            default = 1,
            description = "Resolution of Panoramic image for this bubble")

    group_file: StringProperty(
        name="name of the group",
        description="",
        default="None")

    un_list: CollectionProperty(
        type=UN_contained_in_pov)
    '''
    bpy.types.Object.UN_ep_belong_ob_index = IntProperty()

    bpy.types.Object.UN_pano_belong_ob = CollectionProperty(
        type=UN_panos_belonging_ob)
    bpy.types.Object.UN_pano_belong_ob_index = IntProperty()
    '''

def panolistitem_to_obj(item_in_list):
    obj = bpy.data.objects[item_in_list.name]
    return obj

def export_panoscene(scene, export_folder, EMviq, nodes, format_file, edges):
    #EM_list_clear(bpy.context, "emviq_error_list")
    edges["."] = []
    for pano in scene.pano_list:
        exec(pano.name+'_node = {}')
        exec(panolistitem_to_obj(pano).location[0])
        exec("nodes['"+pano.name+"'] = "+ pano.name + '_node')
        pano.name
 
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
    
    pano_scene = {}
    scenegraph = {}
    nodes = {}
    edges = {}
    
    pano_scene['scenegraph'] = scenegraph
    nodes, edges = export_panoscene(scene, base_dir, True, nodes, self.em_export_format, edges)

    scenegraph['nodes'] = nodes

    # encode dict as JSON 
    data = json.dumps(pano_scene, indent=4, ensure_ascii=True)

    #'/users/emanueldemetrescu/Desktop/'
    file_name = os.path.join(base_dir, "config.json")

    # write JSON file
    with open(file_name, 'w') as outfile:
        outfile.write(data + '\n')

    em_file_4_emviq = os.path.join(export_folder, "em.graphml")

    em_file_fixed_path = bpy.path.abspath(scene.EM_file)
    shutil.copyfile(em_file_fixed_path, em_file_4_emviq)

    return

class PANO_import(bpy.types.Operator):
    bl_idname = "import.pano"
    bl_label = "Import Panoramas from file"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        #minimum_sChildPath, folder_list = read_pano_dir(context)
        read_pano_dir(context)
        lines_in_file = readfile(scene.PANO_file)
        
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

            #print(f"Il panorama {just_created_obj.name} ha rotazione z: {e2d(180.0+phi)}")
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

            #ItemName_res = (remove_extension(ItemName)+"-"+str(scene.RES_pano)+"k.jpg")
            ItemName_res = (remove_extension(ItemName)+".jpg")
            current_panores_foldername = str(scene.RES_pano)+"k"
            
            minimum_sChildPath = os.path.join(scene.PANO_dir,current_panores_foldername)

            diffTex, img = create_tex_from_file(ItemName_res,minimum_sChildPath)
            mat = create_mat(just_created_obj)
            setup_mat_panorama_3DSC(mat.name, img)
           
            scene.pano_list.add()
            scene.pano_list[pano_list_index_counter].name = just_created_obj.name
            #scene.pano_list[pano_list_index_counter].group_file = just_created_obj.name
            
            flipnormals()
            create_cam(just_created_obj.name,pos_x,pos_y,pos_z)
            pano_list_index_counter += 1
        #scene.update()
        return {'FINISHED'}

'''
class ubermat_create(bpy.types.Operator):
    bl_idname = "ubermat_create.pano"
    bl_label = "Create ubermaterial from panoramas"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        create_pano_ubermat(True)

        return {'FINISHED'}

class ubermat_update(bpy.types.Operator):
    bl_idname = "ubermat_update.pano"
    bl_label = "Update ubermaterial from panoramas"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        create_pano_ubermat(False)
        
        return {'FINISHED'}
'''

class REMOVE_pano(bpy.types.Operator):
    bl_idname = "remove.pano"
    bl_label = "Remove selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        if scene.pano_list[scene.pano_list_index].name == "Untitled":
            scene.pano_list.remove(scene.pano_list_index)
            scene.pano_list_index = scene.pano_list_index - 1            
        else:
            try:
                ob_pano = data.objects[scene.pano_list[scene.pano_list_index].name]
                data.objects.remove(ob_pano)
            except:
                pass
            try:
                cam_pano = data.objects['CAM_'+scene.pano_list[scene.pano_list_index].name]
                data.objects.remove(cam_pano)
            except:
                pass
            scene.pano_list.remove(scene.pano_list_index)
            scene.pano_list_index = scene.pano_list_index - 1
        return {'FINISHED'}

class VIEW_pano(bpy.types.Operator):
    bl_idname = "view.pano"
    bl_label = "View from the inside of selected Pano"
    bl_options = {"REGISTER", "UNDO"}

    group_un_idx : IntProperty()
    
    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        pano_list_index = self.group_un_idx#scene.pano_list_index
        current_camera_name = 'CAM_'+scene.pano_list[pano_list_index].name
        current_camera_obj = data.objects[current_camera_name]
        scene.camera = current_camera_obj
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        current_pano = data.objects[scene.pano_list[pano_list_index].name]
        context.view_layer.objects.active = current_pano
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

'''
class VIEW_alignquad(bpy.types.Operator):
    bl_idname = "align.quad"
    bl_label = "align the quad inside the active Pano"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        data = bpy.data
        context = bpy.context
        scene = context.scene
        pano_list_index = scene.pano_list_index
        current_camera_name = 'CAM_'+scene.pano_list[pano_list_index].name
        current_camera_obj = data.objects[current_camera_name]
        #scene.camera = current_camera_obj
        current_pano = data.objects[scene.pano_list[pano_list_index].name]
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
        pano_list_index = scene.pano_list_index
        current_camera_name = 'CAM_'+scene.pano_list[pano_list_index].name

        current_camera_obj = data.objects[current_camera_name]
        current_camera_obj.data.lens = scene.PANO_cam_lens
        #        scene.camera = current_camera_obj
        #        current_pano = data.objects[scene.pano_list[pano_list_index].name]
        #        object = context.active_object


        #        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        #        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        #
        #        scene.objects.active = current_pano
        #        bpy.ops.object.select_all(action='DESELECT')
        #        current_pano.select = True
        #        set_rotation_to_bubble(context,object,current_camera_obj)

        return {'FINISHED'}
'''

def set_res_mat(mat,res_number ):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == "TEX_IMAGE":
            image_filepath_abs = bpy.path.abspath(node.image.filepath)
            #print(image_filepath_abs)
            percorso_e_file = os.path.split(image_filepath_abs)
            #print(percorso_e_file)
            all_panores_base_directory = os.path.dirname(percorso_e_file[0])
            #print(all_panores_base_directory)
            current_panores_foldername = str(res_number)+"k"
            #ItemName_res = (nodename+"-"+str(self.res_number)+"k.jpg")
            minimum_sChildPath = os.path.join(all_panores_base_directory,current_panores_foldername,percorso_e_file[1])
            #print(minimum_sChildPath)
            node.image.filepath = bpy.path.relpath(minimum_sChildPath)

class SETpanoRES(bpy.types.Operator):
    bl_idname = "set.panorama_res"
    bl_label = "set the res of the panorama"
    bl_options = {"REGISTER", "UNDO"}

    res_number : StringProperty()
    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        context.scene.RES_pano = self.index_number
        if scene.RES_propagato_su_tutto:
            for panorama_unit in scene.pano_list:
                #panorama_unit.original_name
                mat = bpy.data.objects[panorama_unit.name].material_slots[0].material
                set_res_mat(mat,self.res_number)
        else:
            active_obj = bpy.context.active_object
            mat = active_obj.material_slots[0].material
            set_res_mat(mat,self.res_number)
        return {'FINISHED'}

class RESETpanoNAME(bpy.types.Operator):
    bl_idname = "reset.panoname"
    bl_label = "reset the name of the panorama"
    bl_options = {"REGISTER", "UNDO"}

    res_number : StringProperty()
    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        nome_oggetto_da_rinominare = scene.pano_list[self.index_number].previous_name
        nuovo_nome_oggetto = scene.pano_list[self.index_number].name
        nome_camera_da_rinominare = "CAM_"+nome_oggetto_da_rinominare
        nuovo_nome_camera = "CAM_"+nuovo_nome_oggetto
        
        bpy.data.objects[nome_oggetto_da_rinominare].name = nuovo_nome_oggetto
        bpy.data.objects[nome_camera_da_rinominare].name = nuovo_nome_camera

        # update "previous name"
        scene.pano_list[self.index_number].previous_name = scene.pano_list[self.index_number].name

        return {'FINISHED'}  

class SETpanoNAME(bpy.types.Operator):

    bl_idname = "set.panoname"
    bl_label = "set the name of the panorama"
    bl_options = {"REGISTER", "UNDO"}

    index_number : IntProperty()

    def execute(self, context):
        scene = bpy.context.scene
        nome_oggetto_da_rinominare = scene.pano_list[self.index_number].previous_name
        nuovo_nome_oggetto = scene.pano_list[self.index_number].name
        nome_camera_da_rinominare = "CAM_"+nome_oggetto_da_rinominare
        nuovo_nome_camera = "CAM_"+nuovo_nome_oggetto
        
        bpy.data.objects[nome_oggetto_da_rinominare].name = nuovo_nome_oggetto
        bpy.data.objects[nome_camera_da_rinominare].name = nuovo_nome_camera

        # update "previous name"
        scene.pano_list[self.index_number].previous_name = scene.pano_list[self.index_number].name

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
        row.operator("remove.pano", icon="ERROR",
                             text='')
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
                '''
                split = layout.split()
                col = split.column()
                col.operator("ubermat_create.pano", icon="MATERIAL", text='')
                col = split.column()
                col.operator("ubermat_update.pano", icon="MATERIAL", text='')
                '''
                ## FINE PORZIONE DI TESTO DISATTIVATA

                row = layout.row()

                split = layout.split()
                col = split.column()

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
        row.template_list("PANO_UL_List", "", scene,
                          "pano_list", scene, "pano_list_index")
        


        if scene.pano_list_index >= 0 and len(scene.pano_list) > 0:
            current_pano = scene.pano_list[scene.pano_list_index].name
            item = scene.pano_list[scene.pano_list_index]
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")
            op = row.operator("set.panoname", icon="DISC", text="")
            op.index_number = scene.pano_list_index

            row = layout.row()  
            row.label(text="Group:")
            row = layout.row()
            row.prop(item, "group_file", text="")

            # assign un to pov section

            row = layout.row()
            row.label(text="Assign selected UN to current POV:")
            op = row.operator("un_models.add_remove", text="", emboss=False, icon='ADD')

            op.rm_add = True
            op.group_un_idx = 8000
            op = row.operator("un_models.add_remove", text="", emboss=False, icon='REMOVE')

            op.rm_add = False
            op.group_un_idx = 8000
            # qui comando selettore del un proxy
            #op = row.operator("select_rm.given_epoch", text="", emboss=False, icon='SELECT_SET')
            #op.rm_epoch = scene.epoch_list[scene.epoch_list_index].name


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
        '''
        row = layout.row()
        
        op = self.layout.operator("view.pano", icon="ZOOM_PREVIOUS", text='Inside the Pano')
        op.group_un_idx = scene.pano_list_index         
        row = layout.row()
        '''
        
        '''
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
        '''

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("UN_PANO_UL_List", "", scene.pano_list[scene.pano_list_index],
                          "un_list", scene, "un_inpano_list_index", rows=2)

class VIEW3D_PT_pov_SetupPanel(Panel, PANOToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_pov_SetupPanel"
    #bl_context = "objectmode"

classes = [
    UN_OT_remove_UN,
    UN_contained_in_pov,
    PANOListItem,
    PANO_UL_List,
    UN_PANO_UL_List,
    REMOVE_pano,
    VIEW_pano,
    #VIEW_alignquad,
    #VIEW_setlens,
    PANO_import,
    #ubermat_create,
    #ubermat_update,
    SETpanoRES,
    SETpanoNAME,
    Res_menu,
    VIEW3D_PT_pov_SetupPanel,
    ImportCoorPanorami,
    OBJECT_OT_PANORAMI,
    UN_OT_add_remove_UN_models,
    OT_toggle_publish,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pano_list = CollectionProperty(type = PANOListItem)
    bpy.types.Scene.pano_list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.resolution_list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.un_inpano_list_index = IntProperty(name="Index for my_list", default=0)

    bpy.types.Scene.RES_propagato_su_tutto = BoolProperty(
        name="Res",
        default=False,
        description="Change resolution of all panoramic image for bubbles"
    )

    bpy.types.Scene.PANO_file = StringProperty(
        name="TXT",
        default="",
        description="Define the path to the PANO file",
        subtype='FILE_PATH'
    )

    bpy.types.Scene.PANO_dir = StringProperty(
        name="DIR",
        default="",
        description="Define the path to the PANO file",
        subtype='DIR_PATH'
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)        
    del bpy.types.Scene.pano_list
    del bpy.types.Scene.pano_list_index
    del bpy.types.Scene.resolution_list_index
    del bpy.types.Scene.RES_propagato_su_tutto
    del bpy.types.Scene.PANO_file
    del bpy.types.Scene.PANO_dir

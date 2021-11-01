import bpy
import os

from bpy.types import Operator

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       StringProperty,
                       EnumProperty
                       )

from .functions import *

# import points section ----------------------------------------------------------

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

def read_pano_data(self,context, filepath, shift, name_col, x_col, y_col, z_col, omega_col, phi_col, kappa_col, separator, clear_list):
        data = bpy.data
        scene = context.scene
        #minimum_sChildPath, folder_list = read_pano_dir(context)
        folder_pano_txt_file, file_name_txt = os.path.split(filepath)
        img_pano_folder = read_pano_dir(folder_pano_txt_file)
        lines_in_file = readfile(filepath)
        if clear_list:
                PANO_list_clear(context)
        pano_list_index_counter = 0
        counter = 0
        # Parse the array:
        for p in lines_in_file:                      
                p0 = p.split(separator)  # use separator                         
                ItemName = p0[name_col]
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

                for model in data.objects:
                        if model.name == remove_extension(ItemName) or model.name == "CAM_"+remove_extension(ItemName):
                                data.objects.remove(model)

                collection_name = namefile_from_path(filepath) 
                if is_collection(collection_name):
                        if bpy.data.collections[collection_name].users < 0:
                                context.collection.children.link(collection_name)
                else:
                        newcol = create_new_col_from_file_name(collection_name)
                             
                context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[collection_name]
                
                sph = bpy.ops.mesh.primitive_uv_sphere_add(calc_uvs=True, radius=0.2, location=(pos_x,pos_y,pos_z))
                just_created_obj = context.active_object
                just_created_obj.name = remove_extension(ItemName)
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
                
                scene.pano_list.add()
                scene.pano_list[pano_list_index_counter].name = scene.pano_list[pano_list_index_counter].previous_name = scene.pano_list[pano_list_index_counter].original_name = just_created_obj.name
                
                flipnormals(context)
                create_pano_cam(just_created_obj.name,pos_x,pos_y,pos_z,bpy.data.collections[collection_name])

                pano_list_index_counter += 1

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

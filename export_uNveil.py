import bpy
import os
from .functions import *

import bpy
import math

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


############## from here operators to export text ########################


class OBJECT_OT_ExportShiftFile(bpy.types.Operator):
    bl_idname = "export.coordshift"
    bl_label = "Export coord name"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.export_shift.file_data('INVOKE_DEFAULT')
            
        return {'FINISHED'}

def write_gsv_data(context, filepath, shift, rot, cam, nam, aton):
    print("running write some data...")
    
    selection = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')

    f = open(filepath, 'w', encoding='utf-8')
        
    #file = open(fn + ".txt", 'w')

    # write selected objects coordinate
    for obj in selection:
        obj.select_set(True)

        x_coor = obj.location[0]
        y_coor = obj.location[1]
        z_coor = obj.location[2]

        if shift == True:
            shift_x = context.scene.BL_x_shift
            shift_y = context.scene.BL_y_shift
            shift_z = context.scene.BL_z_shift
            x_coor = x_coor+shift_x
            y_coor = y_coor+shift_y
            z_coor = z_coor+shift_z

        if aton:
            pass

        else:
            if rot == True or cam == True:
                rotation_grad_x = math.degrees(obj.rotation_euler[0])
                rotation_grad_y = math.degrees(obj.rotation_euler[1])
                rotation_grad_z = math.degrees(obj.rotation_euler[2])

            # Generate UV sphere at x = lon and y = lat (and z = 0 )

            if rot == True:
                if nam == True:
                    f.write("%s %s %s %s %s %s %s\n" % (obj.name, x_coor, y_coor, z_coor, rotation_grad_x, rotation_grad_y, rotation_grad_z))
                else:    
                    f.write("%s %s %s %s %s %s\n" % (x_coor, y_coor, z_coor, rotation_grad_x, rotation_grad_y, rotation_grad_z))
            if cam == True:
                if obj.type == 'CAMERA':
                    f.write("%s %s %s %s %s %s %s %s\n" % (obj.name, x_coor, y_coor, z_coor, rotation_grad_x, rotation_grad_y, rotation_grad_z, obj.data.lens))        
            if rot == False and cam == False:
                if nam == True:
                    f.write("%s %s %s %s\n" % (obj.name, x_coor, y_coor, z_coor))
                else:
                    f.write("%s %s %s\n" % (x_coor, y_coor, z_coor))
            
    f.close()
    return {'FINISHED'}

class ExportEpsgShift(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_shift.file_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Coordinate shift file"

    # ExportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob: StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    nam: BoolProperty(
            name="Add names of objects",
            description="This tool includes name",
            default=True,
            )

    rot: BoolProperty(
            name="Add coordinates of rotation",
            description="This tool includes name, position and rotation",
            default=False,
            )

    cam: BoolProperty(
            name="Export only cams",
            description="This tool includes name, position, rotation and focal lenght",
            default=False,
            )

    shift: BoolProperty(
            name="World shift coordinates",
            description="Shift coordinates using the General Shift Value (GSV)",
            default=False,
            )

    aton: BoolProperty(
            name="Export json for Aton3",
            description="Export a json file compatible with Aton3 framework",
            default=True,
            )

    def execute(self, context):
        return write_gsv_data(context, self.filepath, self.shift, self.rot, self.cam, self.nam, self.aton)

# Only needed if you want to add into a dynamic menu
#def menu_func_export(self, context):
#    self.layout.operator(ExportCoordinates.bl_idname, text="Text Export Operator")

############## from here operators to export geometry ########################

#_______________________________________________________________________________________________________________

def createfolder(basedir, foldername):
    if not os.path.exists(os.path.join(basedir, foldername)):
        os.mkdir(os.path.join(basedir, foldername))
        print('There is no '+ foldername +' folder. Creating one...')
    else:
        print('Found previously created FBX folder. I will use it')
    if not basedir:
        raise Exception("Save the blend file before to export")


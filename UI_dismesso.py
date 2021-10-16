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

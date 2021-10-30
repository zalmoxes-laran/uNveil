'''
CC-BY-NC 2018 EMANUEL DEMETRESCU
emanuel.demetrescu@gmail.com

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "uNveil per Blender",
    "author": "Emanuel Demetrescu",
    "version": (0,9,10),
    "blender": (2, 93, 5),
    "location": "3D View > Toolbox",
    "description": "Multitemporal storytelling",
    "warning": "alpha",
    #"wiki_url": "",
    #"tracker_url": "",
    "category": "Tools"
    }

# if "bpy" in locals():
#     import importlib
#     importlib.reload(import_uNveil)
 
# else:
import math
import bpy

# import sys, os
# sys.path.append(os.path.dirname(__file__)) 

import bpy.props as prop

from bpy.props import (
            StringProperty,
            BoolProperty,
            FloatProperty,
            EnumProperty,
            IntProperty,
            PointerProperty,
            CollectionProperty,
            )
from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    )

from .blender_pip import Pip
Pip._ensure_user_site_package()

from . import (
    import_uNveil,
    export_uNveil,
    functions,
    shift,
    POV_manager,
    POI_manager,
    addon_updater_ops,
    external_modules_install,
    google_credentials,
    spreadsheet
    )

@addon_updater_ops.make_annotations
class DemPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    # addon updater preferences
    auto_check_update : bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False
                )
    updater_intrval_months : bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
                )
    updater_intrval_days : bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
                )
    updater_intrval_hours : bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
                )
    updater_intrval_minutes : bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
                )
    def draw(self, context):
        layout = self.layout
        mainrow = layout.row()
        col = mainrow.column()
        addon_updater_ops.update_settings_ui(self, context)

class RES_list(PropertyGroup):
    """ List of resolutions """

    res_num : IntProperty(
            name="Resolution",
            description="Resolution number",
            default=1)

class CAMTypeList(PropertyGroup):
    """ List of cameras """

    name_cam : StringProperty(
            name="Name",
            description="A name for this item",
            default="Untitled")

classes = (
    #import_uNveil.OBJECT_OT_PANORAMI,
    import_uNveil.ImportCoorPanorami,
    export_uNveil.ExportEpsgShift,
    export_uNveil.OBJECT_OT_ExportShiftFile,
    export_uNveil.POSListItem,
    functions.OBJECT_OT_createcyclesmat,
    functions.OBJECT_OT_savepaintcam,
    CAMTypeList,
    RES_list,
    DemPreferences
    )

def register():

    # addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.BL_x_shift = FloatProperty(
      name = "X shift",
      default = 0.0,
      description = "Define the shift on the x axis",
      )

    bpy.types.Scene.BL_y_shift = FloatProperty(
      name = "Y shift",
      default = 0.0,
      description = "Define the shift on the y axis",
      )

    bpy.types.Scene.BL_z_shift = FloatProperty(
        name = "Z shift",
        default = 0.0,
        description = "Define the shift on the z axis",
        )

    bpy.types.Scene.RES_pano = IntProperty(
        name = "Res",
        default = 1,
        description = "Resolution of Panoramic image for bubbles"
        )

    bpy.types.Scene.RES_poi = IntProperty(
        name = "Res",
        default = 1,
        description = "Resolution of Panoramic image for bubbles"
        )

    bpy.types.Scene.RES_propagato_su_tutto = BoolProperty(
        name = "Res",
        default = False,
        description = "Change resolution of all panoramic image for bubbles"
        )

    bpy.types.Scene.camera_type = StringProperty(
        name = "Camera type",
        default = "Not set",
        description = "Current camera type"
        )

    bpy.types.Scene.BL_epsg = StringProperty(
        name = "EPSG",
        default = "Not set",
        description = "Epsg code"
        )

    bpy.types.Scene.camera_lens = IntProperty(
        name = "Camera Lens",
        default = 35,
        description = "Lens camera",
        )

    bpy.types.Scene.info_log = []

    # panoramic
    bpy.types.Scene.camera_list = CollectionProperty(type = CAMTypeList)
    bpy.types.Scene.resolution_list = CollectionProperty(type = RES_list)

    bpy.types.Scene.PANO_file = StringProperty(
    name = "TXT",
    default = "",
    description = "Define the path to the PANO file",
    subtype = 'FILE_PATH'
    )

    bpy.types.Scene.PANO_dir = StringProperty(
    name = "DIR",
    default = "",
    description = "Define the path to the PANO file",
    subtype = 'DIR_PATH'
    )

    bpy.types.Scene.PANO_cam_lens = IntProperty(
    name = "Cam Lens",
    default = 21,
    description = "Define the lens of the cameras",
    )
    shift.register()
    POV_manager.register()
    external_modules_install.register()
    POI_manager.register()
    google_credentials.register()

def unregister():

    # addon_updater_ops.unregister(bl_info)
    for cls in classes:
        try:
                bpy.utils.unregister_class(cls)
        except RuntimeError:
                pass

    del bpy.types.Scene.BL_x_shift
    del bpy.types.Scene.BL_y_shift
    del bpy.types.Scene.BL_z_shift
    del bpy.types.Scene.RES_pano
    del bpy.types.Scene.camera_type
    del bpy.types.Scene.camera_lens

    del bpy.types.Scene.BL_epsg
    del bpy.types.Scene.RES_propagato_su_tutto


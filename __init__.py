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
    "version": (0,9,11),
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
            IntProperty,
            CollectionProperty,
            )
from bpy.types import (
    PropertyGroup,
    )

from .blender_pip import Pip
Pip._ensure_user_site_package()

from .google_credentials import *

from . import (
    export_uNveil,
    functions,
    shift,
    POV_manager,
    addon_updater_ops,
    # da qui moduli per google
    external_modules_install,
    google_credentials,
    #spreadsheet,
    export_aton,
    UN_manager,
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

    export_uNveil.Export_OT_EpsgShift,
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



    bpy.types.Scene.RES_pano = IntProperty(
        name = "Res",
        default = 1,
        description = "Resolution of Panoramic image for bubbles"
        )

    bpy.types.Scene.RES_un = IntProperty(
        name = "Res",
        default = 1,
        description = "Resolution of Panoramic image for bubbles"
        )

    bpy.types.Scene.camera_type = StringProperty(
        name = "Camera type",
        default = "Not set",
        description = "Current camera type"
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


    bpy.types.Scene.PANO_cam_lens = IntProperty(
    name = "Cam Lens",
    default = 21,
    description = "Define the lens of the cameras",
    )



    shift.register()
    POV_manager.register()
    external_modules_install.register()
    UN_manager.register()
    google_credentials.register()
    export_aton.register()
    check_google_modules()

def unregister():

    # addon_updater_ops.unregister(bl_info)
    for cls in classes:
        try:
                bpy.utils.unregister_class(cls)
        except RuntimeError:
                pass

    shift.unregister()
    POV_manager.unregister()
    external_modules_install.unregister()
    UN_manager.unregister()
    google_credentials.unregister()
    export_aton.unregister()

    del bpy.types.Scene.RES_pano
    del bpy.types.Scene.camera_type
    del bpy.types.Scene.camera_lens

    del bpy.types.Scene.PANO_cam_lens

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


class EPOCH_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
    #def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        epoch_element = item
        #scene = context.scene occhio manca questa variabile: resol_pano
        icons_style = 'OUTLINER'
        #layout.label(text = item.name, icon = item.icon)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.7, align=True)
            layout.prop(epoch_element, "name", text="",
                        emboss=False, icon=epoch_element.icon)


class EPOCHListItem(PropertyGroup):
    """ Group of properties representing an item in the list """

    name : StringProperty(
            name="Name",
            description="A name for this item",
            default="Untitled")

    icon : StringProperty(
            name="code for icon",
            description="",
            default="GROUP_UVS")
    
    resol_pano : IntProperty(
            name = "Res",
            default = 1,
            description = "Resolution of Panoramic image for this bubble")

    root_path: StringProperty(
            name="Epoch folder",
            default="",
            description="Define the path to a given epoch",
            subtype='DIR_PATH')

class EPOCHToolsPanel:
    bl_label = "EPOCH manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        resolution_pano = scene.RES_pano

        #row = layout.row()
        #row.operator("remove.pano", icon="ERROR",
        #                     text='')
        #row = layout.row()

        row = layout.row()
        layout.alignment = 'LEFT'
        row.template_list("EPOCH_UL_List", "", scene,
                          "epoch_list", scene, "epoch_list_index")
        
        if scene.epoch_list_index >= 0 and len(scene.epoch_list) > 0:
            current_pano = scene.epoch_list[scene.epoch_list_index].name
            item = scene.epoch_list[scene.epoch_list_index]
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")

class VIEW3D_PT_epoch_SetupPanel(Panel, EPOCHToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_epoch_SetupPanel"
    #bl_context = "objectmode"

classes = [
    EPOCH_UL_List,
    EPOCHListItem,
    #EPOCHToolsPanel,
    VIEW3D_PT_epoch_SetupPanel
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.epoch_list = CollectionProperty(type = EPOCHListItem)
    bpy.types.Scene.epoch_list_index = IntProperty(name = "Index for my_list", default = 0)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)        
    del bpy.types.Scene.epoch_list
    del bpy.types.Scene.epoch_list_index


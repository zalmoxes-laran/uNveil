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

class UN_contained_in_epoch(PropertyGroup):
    """ List of UN """

    un_item: StringProperty(
        name="Name",
        description="name of the UN",
        default="Untitled")

class EPOCH_remove(Operator):
    """Remove EPOCH"""
    bl_idname = "un_models.rm"
    bl_label = "Remove EPOCH"
    bl_description = "Remove EPOCH"
    bl_options = {'REGISTER', 'UNDO'}

    group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.epoch_list.remove(self.group_un_idx)

        return {'FINISHED'}


class EPOCH_add(Operator):
    """Add EPOCH"""
    bl_idname = "un_models.add"
    bl_label = "Add EPOCH"
    bl_description = "Add EPOCH"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.epoch_list.add()
        scene.epoch_list_index = len(scene.epoch_list) - 1
        return {'FINISHED'}


class UN_Epoch_remove_UN(Operator):
    """Remove UN from EPOCH"""
    bl_idname = "un_models.remove_epoch"
    bl_label = "Remove EPOCH"
    bl_description = "Remove EPOCH"
    bl_options = {'REGISTER', 'UNDO'}

    group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        sel_epoch = scene.epoch_list[scene.epoch_list_index]
        sel_epoch.un_list_epoch.remove(self.group_un_idx)

        return {'FINISHED'}


class UN_Epoch_add_remove_UN_models(Operator):
    """Add and remove UN to/from EPOCH"""
    bl_idname = "un_models.add_remove_epoch"
    bl_label = "Add and remove UN to/from EPOCH"
    bl_description = "Add and remove UN to/from EPOCH"
    bl_options = {'REGISTER', 'UNDO'}

    rm_add: BoolProperty()
    group_un_idx: IntProperty()

    def execute(self, context_epoch):
        scene = context_epoch.scene
        sel_epoch = scene.epoch_list[scene.epoch_list_index]
        sel_un = scene.un_list[scene.un_list_index]

        if self.rm_add:
            un_ancora_non_presente = True

            for list_item in sel_epoch.un_list_epoch:
                if sel_un.identificativo == list_item.un_item:
                    un_ancora_non_presente = False

            if un_ancora_non_presente:
                sel_epoch.un_list_epoch.add()
                print(len(sel_epoch.un_list_epoch)-1)
                sel_epoch.un_list_epoch[len(
                    sel_epoch.un_list_epoch)-1].un_item = sel_un.identificativo
                print(f"Added {sel_un.identificativo} to {sel_epoch.name}")

        else:
            counter = 0
            while counter < len(sel_epoch.un_list_epoch):
                if sel_un.identificativo == sel_epoch.un_list_epoch[counter].un_item:
                    sel_epoch.un_list_epoch.remove(counter)
                    print(f"Ho rimosso il {sel_un.identificativo}")
                counter += 1
        return {'FINISHED'}

class EPOCH_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        epoch_element = item
        icons_style = 'OUTLINER'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.7, align=True)
            layout.prop(epoch_element, "name", text="",
                        emboss=False, icon=epoch_element.icon)

            op = layout.operator(
                "un_models.rm", text="", emboss=False, icon='CANCEL')
            op.group_un_idx = index

class UN_EPOCH_UL_List(UIList):
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
                "un_models.remove_epoch", text="", emboss=False, icon='CANCEL')
            op.group_un_idx = index
            op.rm_add = True
            op.group_un_idx = 8000
            

class UN_EPOCH_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        un_element = item
        icons_style = 'OUTLINER'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.9, align=True)
            layout.prop(un_element, "un_item", text="",
                        emboss=False, icon='VIS_SEL_11')

            op = layout.operator(
                "un_models.remove_epoch", text="", emboss=False, icon='CANCEL')
            op.group_un_idx = index
            

class EPOCHListItem(PropertyGroup):
    """ Group of properties representing an item in the list """

    name: StringProperty(
        name="Name",
        description="A name for this item",
        default="Untitled")

    icon: StringProperty(
        name="code for icon",
        description="",
        default="GROUP_UVS")

    resol_pano: IntProperty(
        name="Res",
        default=1,
        description="Resolution of Panoramic image for this bubble")

    un_list_epoch: CollectionProperty(
        type=UN_contained_in_epoch)
    
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
        row_epoch = layout.row()
        layout.alignment = 'LEFT'
        row_epoch.template_list("EPOCH_UL_List", "", scene,
                          "epoch_list", scene, "epoch_list_index")
        row2 = layout.row()
        row2.label(text="ADD EPOCH:")
        op_epoch = row2.operator("un_models.add", text="", emboss=False, icon='ADD')

        if scene.epoch_list_index >= 0 and len(scene.epoch_list) > 0:
            item = scene.epoch_list[scene.epoch_list_index]        
            row = layout.row()
            row.label(text="Name:")
            row = layout.row()
            row.prop(item, "name", text="")
        
            row1 = layout.row()
            layout.alignment = 'LEFT'
            row1 = layout.row()
            row1.label(text="List of related Narrative Units (UN):")
            row1 = layout.row()
            row1.template_list("UN_EPOCH_UL_List", "", scene.epoch_list[scene.epoch_list_index],
                            "un_list_epoch", scene, "un_inepoch_list_index", rows=3)
            
            row1 = layout.row()
            row1.label(text="Assign selected UN to current EPOCH:")
            op_epoch = row1.operator("un_models.add_remove_epoch", text="", emboss=False, icon='ADD')

            # row1 = layout.row()
            # layout.alignment = 'LEFT'
            # row1 = layout.row()

            # row1.label(text="List of related Narrative Units (UN):")
            # row1 = layout.row()
            # row1.template_list("UN_EPOCH_UL_List", "", scene.epoch_list[scene.epoch_list_index],
            #                    "un_list_epoch", scene, "un_inepoch_list_index", rows=3)

            # row1 = layout.row()
            # row1.label(text="Assign selected UN to current EPOCH:")
            # op_epoch = row1.operator(
            #     "un_models.add_remove_epoch", text="", emboss=False, icon='ADD')

            op_epoch.rm_add = True
            op_epoch.group_un_idx = 8000
            #op = row1.operator("un_models.add_remove", text="", emboss=False, icon='REMOVE')

            #op.rm_add = False
            #op.group_un_idx = 8000


class VIEW3D_PT_epoch_SetupPanel(Panel, EPOCHToolsPanel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_epoch_SetupPanel"
    #bl_context = "objectmode"


classes = [
    UN_contained_in_epoch,
    EPOCH_remove,
    EPOCH_add,
    UN_Epoch_remove_UN,
    UN_Epoch_add_remove_UN_models,
    EPOCH_UL_List,
    UN_EPOCH_UL_List,
    EPOCHListItem,

    VIEW3D_PT_epoch_SetupPanel,]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.epoch_list = CollectionProperty(type = EPOCHListItem)
    bpy.types.Scene.epoch_list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.un_inepoch_list_index = IntProperty(name="Index for my_list", default=0)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.epoch_list
    del bpy.types.Scene.epoch_list_index
    del bpy.types.Scene.un_inepoch_list_index

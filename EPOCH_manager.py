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

    def execute(self,context):
        scene=context.scene
        #current_epoch = scene.epoch_list[scene.epoch_list_index].name
        #item = scene.epoch_list[self.group_epoch_idx]
        scene.epoch_list.remove(self.group_un_idx)

        return {'FINISHED'}

class EPOCH_add(Operator):
    """Add EPOCH"""
    bl_idname = "un_models.add"
    bl_label = "Add EPOCH"
    bl_description = "Add EPOCH"
    bl_options = {'REGISTER', 'UNDO'}


    #group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        #sel_epoch = scene.epoch_list[scene.epoch_list_index]
        
        scene.epoch_list.add()
        scene.epoch_list_index=len(scene.epoch_list) -1

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

    rm_add : BoolProperty()
    group_un_idx : IntProperty()

    def execute(self, context_epoch):
        scene = context_epoch.scene
        sel_epoch = scene.epoch_list[scene.epoch_list_index]
        sel_un = scene.un_list[scene.un_list_index]

        #print(sel_pano.un_list.un_item)
        #if len(sel_pano.un_list) > 0:
        if self.rm_add:
            un_ancora_non_presente = True

            for list_item in sel_epoch.un_list_epoch:
                if sel_un.identificativo == list_item.un_item:
                    un_ancora_non_presente = False

            if un_ancora_non_presente:
                sel_epoch.un_list_epoch.add()
                print(len(sel_epoch.un_list_epoch)-1)
                sel_epoch.un_list_epoch[len(sel_epoch.un_list_epoch)-1].un_item = sel_un.identificativo
                print(f"Added {sel_un.identificativo} to {sel_epoch.name}") #{sel_pano.un_list[len(sel_pano.un_list)-1].un_item}")
        
        else:
            counter = 0
            while counter < len(sel_epoch.un_list_epoch):
                if sel_un.identificativo == sel_epoch.un_list_epoch[counter].un_item:
                    sel_epoch.un_list_epoch.remove(counter)
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
            #op = layout.menu(Epoch_un_menu.bl_idname,
                            #text=epoch_element.active_un_epoch)#, icon='COLOR')
            #op.pano_index = index

            #icon = '' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "un_models.rm", text="", emboss=False, icon='CANCEL')
            op.group_un_idx = index
            #op.rm_add = True
            #op.group_un_idx = 8000
            
            op = layout.operator(
                "view.epoch", text="", emboss=False, icon='VIS_SEL_11')
            op.group_un_idx = index

            icon = 'RESTRICT_VIEW_OFF' if epoch_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "epoch_manager.toggle_publish", text="", emboss=False, icon=icon)
            op.group_un_idx = index
'''
            op = layout.operator(
                "view.pano", text="", emboss=False, icon='VIS_SEL_11')
            op.group_un_idx = index

            icon = 'RESTRICT_VIEW_OFF' if epoch_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "pov_manager.toggle_publish", text="", emboss=False, icon=icon)
            op.group_un_idx = index
'''
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
            '''
            icon = 'RESTRICT_VIEW_OFF' if pano_element.publish_item else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "pov_manager.toggle_publish", text="", emboss=False, icon=icon)
            op.group_un_idx = index
            '''
        #self.layout.prop(context.scene, "test_color", text='Detail Color')


class OT_EP_toggle_publish(Operator):
    """Define if a EPOCH will be published or not"""
    bl_idname = "epoch_manager.toggle_publish"
    bl_label = "Toggle Publish"
    bl_description = "Define if a EPOCH will be published or not"
    bl_options = {'REGISTER', 'UNDO'}

    group_un_idx: IntProperty()

    def execute(self, context):
        scene = context.scene
        print(str(scene.epoch_list_index))
        if self.group_un_idx < len(scene.epoch_list):
            print(f"toggle {self.group_un_idx}")
            scene.epoch_list[self.group_un_idx].publish_item = not scene.epoch_list[self.group_un_idx].publish_item
            print(scene.epoch_list[self.group_un_idx].publish_item)
           
        return {'FINISHED'}

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
        #obj = context.active_object
        #resolution_pano = scene.RES_pano

        #row = layout.row()
        #row.operator("remove.pano", icon="ERROR",
        #                     text='')
        #row = layout.row()

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
        
        
        #if scene.epoch_list_index >= 0 and len(scene.epoch_list) > 0:
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
    OT_EP_toggle_publish,    
    EPOCHListItem,
    #EPOCHToolsPanel,
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


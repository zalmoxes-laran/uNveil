



import sys, os, bpy
sys.path.append(os.path.dirname(__file__)) 
# #import target_camera
# #from sniper_utils import *

bl_info = {
    "name": "uNveil per Blender",
    "author": "Emanuel Demetrescu",
    "version": (0,9,10),
    "blender": (2, 93, 4),
    "location": "3D View > Toolbox",
    "description": "Multitemporal storytelling",
    "warning": "alpha",
    #"wiki_url": "",
    #"tracker_url": "",
    "category": "Tools"
    }


from bpy.types import (
    AddonPreferences,
    PropertyGroup
    )

from . import (
     UI,
#     import_uNveil,
#     export_uNveil,
#     functions,
#     shift,
#     POV_manager,
#     addon_updater_ops
     )


# interface

class CameraToolsPanel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Animation"
	bl_label = "Sniper"
	bl_context = "objectmode"
	
	def draw(self, context):
		layout = self.layout
		
		col = layout.column(align = True)
		col.operator("sniper.insert_target_camera", icon = "OUTLINER_DATA_CAMERA")
		#if target_camera.targetCameraSetupExists(): col.label(text="Settings are in 'Sniper' tab.", icon = "INFO")
		
		col = layout.column(align = True)
		col.operator("sniper.seperate_text")
		col.operator("sniper.text_to_name")
		
		
# operators
		
class TextToNameOperator(bpy.types.Operator):
	bl_idname = "sniper.text_to_name"
	bl_label = "Text to Name"
	bl_description = "Rename all text objects to their content."
	
	def execute(self, context):
		#textToName()
		return{"FINISHED"}
		
class SeperateTextOperator(bpy.types.Operator):
	bl_idname = "sniper.seperate_text"
	bl_label = "Seperate Text"
	bl_description = "Create new text object for every line in active text object."
	
	def execute(self, context):
		active = getActive()
		#if isTextObject(active):
		#	seperateTextObject(active)
		#	delete(active)
		
		return{"FINISHED"}
			

#registration

classes = (
	CameraToolsPanel,
	TextToNameOperator,
	SeperateTextOperator,
)

def register():
	for c in classes:
		bpy.utils.register_class(c)
	
	#target_camera.register()

def unregister():
	for c in reversed(classes):
		bpy.utils.unregister_class(c)
	
	#target_camera.unregister()

if __name__ == "__main__":
	register()
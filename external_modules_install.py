import subprocess
import sys
import os
import bpy
import site
import pkg_resources
from bpy.types import Panel

from .blender_pip import Pip
Pip._ensure_user_site_package()

import logging
log = logging.getLogger(__name__)

class OBJECT_OT_install_missing_modules(bpy.types.Operator):
    bl_idname = "install_missing.modules"
    bl_label = "missing modules"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #bpy.ops.image.save_dirty()
        install_modules()
        return {'FINISHED'}

def install_modules():
    Pip.upgrade_pip()
    list_of_modules =[
        "google-api-python-client==1.7.9",
        "google-auth-httplib2==0.0.3",
        "google-auth-oauthlib==0.4.0"]
    for module_istall in list_of_modules:
        Pip.install(module_istall)

def old_install_modules():
    
    packages_path = site.getusersitepackages()
    sys.path.insert(0, packages_path )

    is_windows = sys.platform.startswith('win')
    if is_windows:
        print("Il sistema è windows")
        python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
        python_libs = os.path.join(sys.prefix, 'lib', 'site-packages')
        #python_libs = python_libs.replace('\\\ ', '\\')
    is_mac = sys.platform.startswith('darwin')
    if is_mac:
        python_exe = os.path.join(sys.prefix, 'bin', 'python3.9')
        python_exe = python_exe.replace(' ', '\\ ')
        python_libs = os.path.join(sys.prefix, 'lib', 'site-packages')
        python_libs = python_libs.replace(' ', '\\ ')
    is_linux = sys.platform.startswith('linux') # correggere
    print(python_libs)
    sys.path.insert(0, python_libs )
    #print(str(python_exe))

    list_of_modules =["google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib", "googleapiclient"]

    # upgrade pip
    #subprocess.call([python_exe, "-m", "ensurepip"])
    #subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    #subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    # install required packages
    #subprocess.call([python_exe, "-m", "pip", "install", "pyzenodo3"])
    #subprocess.call([python_exe, "-m", "pip", "install", "python-telegram-bot"])
    
    for install_module in list_of_modules:
        print("ciao")
        #subprocess.call([python_exe, "-m", "pip", "install", "--target=",python_libs, install_module])


    # installed_packages = pkg_resources.working_set
    # installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
    #     for i in installed_packages])
    # print(installed_packages_list)

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

classes = [
    OBJECT_OT_install_missing_modules,
    VIEW3D_PT_metadata
    ]

def register():
	for cls in classes:
		try:
			bpy.utils.register_class(cls)
		except ValueError as e:
			log.warning('{} is already registered, now unregister and retry... '.format(cls))
			bpy.utils.unregister_class(cls)
			bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    install_modules()

import subprocess
import sys
import os
import bpy
import site
import pkg_resources

class OBJECT_OT_install_missing_modules(bpy.types.Operator):
    bl_idname = "install_missing.modules"
    bl_label = "missing modules"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #bpy.ops.image.save_dirty()
        install_modules()
        return {'FINISHED'}

def install_modules():
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
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    #subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    # install required packages
    #subprocess.call([python_exe, "-m", "pip", "install", "pyzenodo3"])
    #subprocess.call([python_exe, "-m", "pip", "install", "python-telegram-bot"])
    
    for install_module in list_of_modules:
        subprocess.call([python_exe, "-m", "pip", "install", "--target=",python_libs, install_module])


    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])
    print(installed_packages_list)

if __name__ == '__main__':
    install_modules()

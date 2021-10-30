import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

import os

def get_creds_folder_path():
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    credential_folder = os.path.join(directory, "creds")

    if not os.path.exists(credential_folder):
        os.mkdir(credential_folder)
        print('There is no creds folder. Creating one...')
    else:
        print('Found previously created creds folder. I will use it')
        print(credential_folder)

    return credential_folder

class uNveil_GoogleCredentialsPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Google credentials folder path",
        subtype='FILE_PATH',
        default = get_creds_folder_path(),
    )
    '''
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )
    '''
    def draw(self, context):
        layout = self.layout
        layout.label(text="Google credentials setup")
        layout.prop(self, "filepath")
        #layout.prop(self, "number")
        #layout.prop(self, "boolean")

class OBJECT_OT_uNveil_prefs_googlecreds(Operator):
    """Display Google Credentials preferences"""
    bl_idname = "object_.unveil_prefs_googlecreds"
    bl_label = "uNveil Preferences Google Credentials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s" % (addon_prefs.filepath))
        #info = ("Path: %s, Number: %d, Boolean %r" %
        #        (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

class OBJECT_OT_uNveil_open_prefs(Operator):
    """Open Google Credentials preferences panel"""
    bl_idname = "open_prefs_panel.unveil_googlecreds"
    bl_label = "open panel uNveil preferences Google Credentials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.preferences.addon_show(module="uNveil")

        return {'FINISHED'}

# Registration
def register():
    bpy.utils.register_class(OBJECT_OT_uNveil_prefs_googlecreds)
    bpy.utils.register_class(uNveil_GoogleCredentialsPreferences)
    bpy.utils.register_class(OBJECT_OT_uNveil_open_prefs)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_uNveil_prefs_googlecreds)
    bpy.utils.unregister_class(uNveil_GoogleCredentialsPreferences)
    bpy.utils.unregister_class(OBJECT_OT_uNveil_open_prefs)



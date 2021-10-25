

def open_user_pref():
      addon_prefs = get_addon_preferences()# function return my addon pref
      bpy.ops.screen.userpref_show('INVOKE_DEFAULT') # open preferences window
      addon_prefs.active_section = 'ADDONS' # go to addon sections
      bpy.ops.preferences.addon_expand(module=get_addon_name())# get_addon_name() it is a small function that returns the name of the addon (For my convenience)
      bpy.ops.preferences.addon_show(module=get_addon_name()) # Show my addon pref
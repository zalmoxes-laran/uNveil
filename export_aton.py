import bpy
import os
from bpy.types import Panel
from bpy.props import EnumProperty, StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty

from .functions import *

from .POV_manager import panolistitem_to_obj

import json

from shutil import copyfile


def export_unveil_json(scene, base_dir, network, sem):
    
    for pano in scene.pano_list:
        if pano.publish_item:

        #pov_list = ["pippo","pluto","paperino"]
        #for pov in pov_list:
            network_node = {}
            print(pano.name)
            network_node['name'] = pano.name
            ob = panolistitem_to_obj(pano)
            network_node['pos'] = [ob.location[0], ob.location[2], -ob.location[1]]
            network_node['rot'] = [ob.rotation_euler[0], ob.rotation_euler[2], -ob.rotation_euler[1]]
            network_node['semlist'] = []

            if len(pano.un_list) > 0:
                for sema in pano.un_list:
                    print(f"stampare {sema.un_item}")
            
                    #network_node['semlist'].clear()
                    #network_node['semlist'] = ["P01","P02","P03"]
                    network_node['semlist'].append(str(sema.un_item))
            
            #network_node['semlist'] = pano.un_list
            #network_node['semlist'] = ["P01","P02","P03"]
            network.append(network_node)

    for un in scene.un_list:
    #un_list = ["portos","Aramis","Dartagnan"]
    #for un in un_list:
        sem_node = {}
        # qui si iniettano i descrittori del un
        sem_subnode = {}
        sem_subnode['titolo'] = un.nome
        sem_subnode['title'] = un.name
        sem_subnode['descrITA'] = un.descrizione
        sem_subnode['descrENG'] = un.description
        sem_subnode['cover'] = "immagine.jpg"
        sem_subnode['audio'] = "p11.mp3"
        # e si agganciano al nodo superiore
        sem_node = sem_subnode
        # qui si assegna il nome del UN
        sem[un.identificativo] = sem_node

    '''
    for ob in bpy.data.objects:
        if len(ob.EM_ep_belong_ob) == 0:
            pass
        if len(ob.EM_ep_belong_ob) == 1:
            ob_tagged = ob.EM_ep_belong_ob[0]
            for epoch in scene.epoch_list:
                if ob_tagged.epoch == epoch.name:
                    epochname1_var = epoch.name.replace(" ", "_")
                    epochname_var = epochname1_var.replace(".", "")
                    #rm_folder = createfolder(export_folder, "rm")
                    rm_folder = export_folder
                    export_sub_folder = createfolder(rm_folder, epochname_var)
                    ob.select_set(True)
                    #name = bpy.path.clean_name(ob.name)
                    export_file = os.path.join(export_sub_folder, ob.name)
                    if format_file == "obj":
                        bpy.ops.export_scene.obj(filepath=str(export_file + '.obj'), use_selection=True, axis_forward='Y', axis_up='Z', path_mode='RELATIVE')
                        copy_tex_ob(ob, export_sub_folder)

                    if format_file == "gltf":
                        #bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', ui_tab='GENERAL', export_copyright=copyright, export_image_format='AUTO', export_texture_dir='', export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=draco_compression, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_generic_quantization=12, export_tangents=False, export_materials='EXPORT', export_colors=False, export_cameras=False, export_selected=True, use_selection=True, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=False, export_def_bones=False, export_current_frame=False, export_skins=False, export_all_influences=False, export_morph=True, export_morph_normal=False, export_morph_tangent=False, export_lights=False, export_displacement=False, will_save_settings=False, filepath=file_path, check_existing=False)#, filter_glob='*.glb;*.gltf')
                        bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', ui_tab='GENERAL', export_copyright="Extended Matrix", export_image_format='AUTO', export_texture_dir="", export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=False, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_generic_quantization=12, export_tangents=False, export_materials='EXPORT', export_colors=True, export_cameras=False, export_selected=True, use_selection=False, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=True, export_nla_strips=False, export_def_bones=False, export_current_frame=False, export_skins=True, export_all_influences=False, export_morph=True, export_morph_normal=False, export_morph_tangent=False, export_lights=False, export_displacement=False, will_save_settings=False, filepath=str(export_file), check_existing=False, filter_glob="*.glb;*.gltf")                    
                    if format_file == "fbx":
                        bpy.ops.export_scene.fbx(filepath = export_file + ".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'MESH'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=True, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, armature_nodetype='NULL', bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')
                    if EMviq:
                        try:
                            exec(epochname_var+'_node')
                        except NameError:
                            print("well, it WASN'T defined after all!")
                                exec(epochname_var + '_node' + ' = {}')
                            romano_node = {}
                                exec(epochname_var + '_urls = []')
                            romano_urls = []
                                exec(epochname_var + "_node['urls'] = "+ epochname_var +"_urls")
                            romano_node['urls'] = romano_urls
                            exec("nodes['"+epoch.name+"'] = "+ epochname_var + '_node')

                            #exec(epochname_var + '_edge = []')
                            #exec(epochname_var + '_edge.append(".")')
                            #exec(epochname_var + '_edge.append("'+ epoch.name +'")')

                            #exec('edges["."].append('+epochname_var + '_edge)')
                            edges["."].append(epoch.name)
                        else:
                            print("sure, it was defined.")

                        #exec(epochname_var + '_urls.append("' + epochname_var +'/'+ ob.name + '.' + format_file +'")')
                        #but here we want to set the osgjs file format (the emviq server will convert the obj to osgjs)
                        exec(epochname_var + '_urls.append("'+utente_aton+'/models/'+progetto_aton+'/' + epochname_var +'/'+ ob.name + '.gltf")')
                    ob.select_set(False)
        if len(ob.EM_ep_belong_ob) >= 2:
            for ob_tagged in ob.EM_ep_belong_ob:
                for epoch in scene.epoch_list:
                    if ob_tagged.epoch == epoch.name:
                        epochname1_var = epoch.name.replace(" ", "_")
                        epochname_var = epochname1_var.replace(".", "")
                        #rm_folder = createfolder(export_folder, "rm")
                        rm_folder = export_folder
                        #export_sub_folder = createfolder(rm_folder, epochname_var)
                        export_sub_folder = createfolder(rm_folder, "shared")
                        
                        ob.select_set(True)
                        #name = bpy.path.clean_name(ob.name)
                        export_file = os.path.join(export_sub_folder, ob.name)
                        if format_file == "obj":
                            bpy.ops.export_scene.obj(filepath=str(export_file + '.obj'), use_selection=True, axis_forward='Y', axis_up='Z', path_mode='RELATIVE')
                            copy_tex_ob(ob, export_sub_folder)

                        if format_file == "gltf":
                            #bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', ui_tab='GENERAL', export_copyright=copyright, export_image_format='AUTO', export_texture_dir='', export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=draco_compression, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_generic_quantization=12, export_tangents=False, export_materials='EXPORT', export_colors=False, export_cameras=False, export_selected=True, use_selection=True, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=False, export_def_bones=False, export_current_frame=False, export_skins=False, export_all_influences=False, export_morph=True, export_morph_normal=False, export_morph_tangent=False, export_lights=False, export_displacement=False, will_save_settings=False, filepath=str(export_file), check_existing=False)#, filter_glob='*.glb;*.gltf')
                            bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', export_copyright="Extended Matrix", export_image_format='AUTO', export_texture_dir="", export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=False, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_generic_quantization=12, export_tangents=False, export_materials='EXPORT', export_colors=True, export_cameras=False, use_selection=True, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=True, export_nla_strips=False, export_def_bones=False, export_current_frame=False, export_skins=True, export_all_influences=False, export_morph=True, export_lights=False, export_displacement=False, will_save_settings=False, filepath=str(export_file), check_existing=False, filter_glob="*.glb;*.gltf")                    
                        if format_file == "fbx":
                            bpy.ops.export_scene.fbx(filepath = export_file + ".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'MESH'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=True, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, armature_nodetype='NULL', bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')
                        if EMviq:
                            try:
                                exec(epochname_var+'_node')
                            except NameError:
                                print("well, it WASN'T defined after all!")
                                exec(epochname_var + '_node' + ' = {}')
                                exec(epochname_var + '_urls = []')
                                exec(epochname_var + "_node['urls'] = "+ epochname_var +"_urls")
                                exec("nodes['"+epoch.name+"'] = "+ epochname_var + '_node')

                                #exec(epochname_var + '_edge = []')
                                #exec(epochname_var + '_edge.append(".")')
                                #exec(epochname_var + '_edge.append("'+ epoch.name +'")')

                                #exec('edges.append('+epochname_var + '_edge)')
                                edges["."].append(epoch.name)

                            else:
                                print("sure, it was defined.")
                            
                            #exec(epochname_var + '_urls.append("' + epochname_var +'/'+ ob.name + '.' + format_file +'")')
                            #but here we want to set the osgjs file format (the emviq server will convert the obj to osgjs)
                            exec(epochname_var + '_urls.append("'+utente_aton+'/models/'+progetto_aton+'/shared/'+ ob.name + '.gltf")')
                            #exec(epochname_var + '_urls.append("rm/shared/' + ob.name + '.osgjs")')
                        ob.select_set(False)
    '''
    
    return network, sem

class UNVEIL_OT_aton_json_export(bpy.types.Operator):
    """Export json file to aton"""
    bl_idname = "export.unjsonaton"
    bl_label = "Export json file to Aton"
    bl_description = "Export json file to Aton"
    bl_options = {'REGISTER', 'UNDO'}

    #em_export_type : StringProperty()
    #em_export_format : StringProperty()

    def execute(self, context):
        scene = context.scene
        progetto_aton = scene.unveil_dir_aton

        fix_if_relative_folder = bpy.path.abspath(scene.unveil_dir_aton)
        base_dir = fix_if_relative_folder# os.path.dirname(fix_if_relative_folder)

        print("la base_dir per il file json è:"+base_dir)
        
        #setup json variables
        unveil_scene = {}
        #scenegraph = {}
        network = []
        sem = {}
        
        #unveil_scene['scenegraph'] = scenegraph

        '''
        export_folder = base_dir_scene
        proxies_folder = createfolder(export_folder, 'proxies')
        '''
        network, sem = export_unveil_json(scene, base_dir, network, sem)
        #export_proxies(scene, proxies_folder)
        
        unveil_scene['network'] = network

        unveil_scene['sem'] = sem

        # encode dict as JSON 
        data = json.dumps(unveil_scene, indent=4, ensure_ascii=True)

        #'/users/emanueldemetrescu/Desktop/'
        file_name = os.path.join(base_dir, "config.json")

        # write JSON file
        with open(file_name, 'w') as outfile:
            outfile.write(data + '\n')

        content_base_dir =os.path.join(base_dir+"content")
        for resol in scene.resolution_list:
            res_folder_name = str(resol.res_num)+"k"
            create_folder_in_path(res_folder_name, content_base_dir)
            for pano in scene.pano_list:
                if pano.publish_item:
                    ob = select_obj_from_panoitem(pano.name)
                    image_file_path = get_img_path_from_ob(ob) 
                    fix_if_relative_path = bpy.path.abspath(image_file_path)
                    normalized_path = os.path.normpath(fix_if_relative_path)
                    path_components = normalized_path.split(os.sep)
                    path_components[len(path_components)-2] = res_folder_name
                    original_file_path = os.path.join(*path_components)
                    filename, file_extension = os.path.splitext(original_file_path)
                    file_name_with_extension = pano.name+file_extension
                    destination_file_path = os.path.join(content_base_dir,res_folder_name,file_name_with_extension)
                    if os.path.isfile(destination_file_path):
                        print(f"File esistente {destination_file_path}")
                    else:
                        copyfile(original_file_path, destination_file_path)    
            

        return {'FINISHED'}


def get_img_path_from_ob(ob): #
    mat_nodes = ob.material_slots[0].material.node_tree.nodes
    for node in mat_nodes:
        if node.type == 'TEX_IMAGE':
            return node.image.filepath
            pass
    print("non ho trovato nulla")
    return "none"


# Pannello di export

class Export_Aton_panel:
    bl_label = "uNveil export to Aton"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Export")
        row.operator("export.unjsonaton", icon="STICKY_UVS_DISABLE", text='Export Aton')
        row = layout.row()
        row.prop(context.scene, 'unveil_dir_aton', toggle = True, text ="")

        
class VIEW3D_PT_un_Export_Aton_panel(Panel, Export_Aton_panel):
    bl_category = "uNveil"
    bl_idname = "VIEW3D_PT_un_Export_Aton_panel"

# sezione di registrazione delle classi

classes = [
    VIEW3D_PT_un_Export_Aton_panel,
    UNVEIL_OT_aton_json_export,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.unveil_dir_aton = StringProperty(
        name = "Aton directory for uNveil",
        default = "",
        description = "Define the path to the Aton directory to export the uNveil project",
        subtype = 'FILE_PATH'
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)        
    del bpy.types.Scene.unveil_dir_aton
import bpy
import os
from bpy.types import Panel
from bpy.props import EnumProperty, StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty

from .functions import *

from .POV_manager import panolistitem_to_obj

import json

from shutil import copyfile
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

def export_unveil_json(scene, base_dir, network, sem):
    
    
    
    
    
    for pano in scene.pano_list:
        list_un_pano=[]
        np=(pano.name)
        network_node = {}
        if pano.publish_item:
        
            network_node['name'] = np
            network_node['title'] = pano.title
            ob = panolistitem_to_obj(pano)
            network_node['pos'] = [ob.location[0], ob.location[2], -ob.location[1]]
            network_node['rot'] = [0.0, 0.0, 0.0]
            
            
        #network_node['semlist'] = []
        if len(pano.un_list) > 0:
            for sema in pano.un_list:
                list_un_pano.append(sema.un_item)
                # print(f"stampare {sema.un_item}")
                #pano_a=network_node['semlist'].append(str(sema.un_item))
                
        i=0
        network_node['semlist'] = []       
        for ep in scene.epoch_list:
            list_epoch=[]
            list_un_epoch=[]
            s=str(ep.name)
            list_epoch.append(s)
            print(s)
            #
            
            for sema_2 in ep.un_list_epoch:
                list_un_epoch.append(sema_2.un_item)
                print(str(list_un_epoch))
            #for e in list_un_epoch:            
                #epoch_b= network_node['semlist'].append(str(e))
                #print(str(epoch_b))
        
        
                intersezione=[]
                intersezione=set(list_un_epoch)&set(list_un_pano) #comapara le liste
                print('ok')
                a = ep.name
            
                network_node['semlist'] = {'{}'.format(a):[]}
                network_node['semlist'][a].append(listToString(list(intersezione)))
            i+=1        
            #else:
                #print('non sono uguali')
            
        network.append(network_node)   
            #network.append() 
    for un in scene.un_list:

        sem_node = {}
        # qui si iniettano i descrittori del un
        sem_subnode = {}

        sem_subnode['title'] = un.nome
        #sem_subnode['title'] = un.name
        sem_subnode['descr'] = un.descrizione

        #sem_subnode['descrENG'] = un.description
        sem_subnode['cover'] = "immagine.jpg"
        sem_subnode['audio'] = "p11.mp3"
        # e si agganciano al nodo superiore
        sem_node = sem_subnode
        # qui si assegna il nome del UN
        sem[un.identificativo] = sem_node

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

        #print("la base_dir per il file json è:"+base_dir)
        
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
        
        unveil_scene['distancetext'] = "distante"

        unveil_scene['network'] = network

        unveil_scene['sem'] = sem

        # encode dict as JSON 
        data = json.dumps(unveil_scene, indent=4, ensure_ascii=True)

        #'/users/emanueldemetrescu/Desktop/'
        file_name_with_suffix = "config-"+scene.aton_pano_project_name+".json"
        file_name = os.path.join(base_dir, file_name_with_suffix)

        # write JSON file
        with open(file_name, 'w') as outfile:
            outfile.write(data + '\n')
        '''
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
                    pano_name_with_res_and_epoch_suffix = pano.name+"-"+res_folder_name+"-m"
                    file_name_with_extension = pano_name_with_res_and_epoch_suffix+file_extension
                    #file_name_with_extension = pano.name+file_extension
                    destination_file_path = os.path.join(content_base_dir,res_folder_name,file_name_with_extension)
                    if os.path.isfile(destination_file_path):
                        print(f"File esistente {destination_file_path}")
                    else:
                        copyfile(original_file_path, destination_file_path)    
        '''
        return {'FINISHED'}

def get_img_path_from_ob(ob):
    mat_nodes = ob.material_slots[0].material.node_tree.nodes
    for node in mat_nodes:
        if node.type == 'TEX_IMAGE':
            return node.image.filepath
            pass
    print("non ho trovato una immagine")
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
        row.operator("export.unjsonaton",
                     icon="STICKY_UVS_DISABLE", text='Export Aton')

        row = layout.row()
        row.label(text="Suffisso nome progetto")
        row.prop(context.scene, 'aton_pano_project_name', toggle=True, text="")

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
    bpy.types.Scene.aton_pano_project_name = StringProperty(
        name = "Suffix of the name of the project",
        default = "",
        description = "Define the suffix of the name of the project",
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)        
    del bpy.types.Scene.unveil_dir_aton
    del bpy.types.Scene.aton_pano_project_name

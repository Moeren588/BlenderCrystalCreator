import bpy

from . import crystal_gen_operators, crystal_gen_ui, crystal_gen_utils


bl_info = {
    'name' : 'Procedural Crystal Generator',
    'author' : 'Martin Moen',
    'description' : 'Procedural tool to create crystals',
    'location' : 'View3D',
    'category' : 'Add Mesh',
    'blender' : (4, 1, 0),
    'version' : (0, 1, 0),
}

class PCG_PT_MainPanel(bpy.types.Panel):
    bl_idname = "PCG_PT_main"
    bl_label = f"Procedural Crystal Generator v. {bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_category = "PCG"

    def draw(self, context):
        layout = self.layout

classes = [
    PCG_PT_MainPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    crystal_gen_operators.register()
    crystal_gen_ui.register()


def unregister():
    crystal_gen_ui.unregister()
    crystal_gen_operators.unregister()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    # Try to unregister
    try: unregister()
    except: pass

    register()
    crystal_gen_utils.log_console_message('sys', f'Registered Crystal Generator v. {bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}')
    
    
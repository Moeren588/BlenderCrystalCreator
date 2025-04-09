import bpy

from . import crystal_gen_operators, crystal_gen_ui

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
    bl_label = "Procedural Crystal Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_category = "PCG"

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"PCG {bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}")

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
    
    for cls in classes.reverse():
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
    
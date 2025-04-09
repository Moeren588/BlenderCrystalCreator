import bpy

from . import crystal_gen_operators, crystal_gen_utils

class PCG_PT_CreateCrystal(bpy.types.Panel):
    bl_idname = "PCG_PT_CreateCrystal"
    bl_label = "Create Crystal"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "PCG_PT_main"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create Crystal")
        
        op_generate = layout.operator(crystal_gen_operators.MESH_OT_generate_procedural_crystal.bl_idname, text=crystal_gen_operators.MESH_OT_generate_procedural_crystal.bl_label)
        layout.prop(op_generate, "radius")
        layout.prop(op_generate, "height")
        layout.prop(op_generate, "vertices")


classes = [
    PCG_PT_CreateCrystal,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes.reverse():
        bpy.utils.unregister_class(cls)
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
        
        layout.prop(context.scene, "procedural_crystal_radius")
        layout.prop(context.scene, "procedural_crystal_height")
        layout.prop(context.scene, "procedural_crystal_vert_count")
        layout.prop(context.scene, "procedural_crystal_has_pointy_top")
        layout.prop(context.scene, "procedural_crystal_has_pointy_bottom")

        op_generate = layout.operator(crystal_gen_operators.MESH_OT_generate_procedural_crystal.bl_idname, text=crystal_gen_operators.MESH_OT_generate_procedural_crystal.bl_label)


classes = [
    PCG_PT_CreateCrystal,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
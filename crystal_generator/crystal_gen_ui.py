import bpy

class PCG_PT_CreateCrystal(bpy.types.Panel):
    bl_idname = "PCG_PT_CreateCrystal"
    bl_label = "Create Crystal"
    bl_parent_id = "PCG_PT_main"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create Crystal")


classes = [
    PCG_PT_CreateCrystal,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes.reverse():
        bpy.utils.unregister_class(cls)
import bpy

from . import crystal_gen_utils

class MESH_OT_generate_procedural_crystal(bpy.types.Operator):
    bl_idname = "mesh.generate_procedural_crystal"
    bl_label = "Generate Procedural Crystal"
    bl_options = {'REGISTER', 'UNDO'}

    gen_radius : bpy.props.FloatProperty(name="Radius", default=1.0, min=0.01)  # type: ignore
    gen_height : bpy.props.FloatProperty(name="Height", default=2.0, min=0.01) # type: ignore
    gen_vert_count : bpy.props.IntProperty(name="Vertices", default=16, min=3, max=64) # type: ignore
    
    
    def execute(self, context):

        crystal_gen_utils.log_console_message('info', 'Generating crystal...')

        crystal_gen_utils.generate_basic_crystal_bmesh(self.gen_radius, self.gen_height, self.gen_vert_count)
        
        crystal_gen_utils.log_console_message('finish', 'Finished generating crystal')

        return {'FINISHED'}
        
    def invoke(self, context, event):

        self.gen_radius = context.scene.procedural_crystal_radius
        self.gen_height = context.scene.procedural_crystal_height
        self.gen_vert_count = context.scene.procedural_crystal_vert_count


        return self.execute(context)
        

classes = [
    MESH_OT_generate_procedural_crystal,
]

def register():
    ## GROUPS

    ## PROPS
    bpy.types.Scene.procedural_crystal_radius = bpy.props.FloatProperty(name="Radius", default=1.0, min=0.01)
    bpy.types.Scene.procedural_crystal_height = bpy.props.FloatProperty(name="Height", default=2.0, min=0.01)
    bpy.types.Scene.procedural_crystal_vert_count = bpy.props.IntProperty(name="Vertices", default=8, min=3, max=64)
    bpy.types.Scene.procedural_crystal_has_pointy_top = bpy.props.BoolProperty(name="Pointy Top", default=True)
    bpy.types.Scene.procedural_crystal_has_pointy_bottom = bpy.props.BoolProperty(name="Pointy Bottom", default=False)

    ## CLASSES
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    ## CLASSES
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    ## PROPS
    del bpy.types.Scene.procedural_crystal_vert_count
    del bpy.types.Scene.procedural_crystal_height
    del bpy.types.Scene.procedural_crystal_radius



    ## GROUPS
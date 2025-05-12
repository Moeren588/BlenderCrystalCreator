import bpy
import os

from . import crystal_gen_utils

custom_icons = None


class GRP_crystal_generator_properties(bpy.types.PropertyGroup):
    crystal_radius : bpy.props.FloatProperty(name="Radius", default=1.0, min=0.01) # type: ignore
    crystal_height : bpy.props.FloatProperty(name="Height", default=2.0, min=0.01) # type: ignore
    crystal_sides : bpy.props.IntProperty(name="Sides", default=8, min=3, max=64) # type: ignore
    crystal_has_pointy_top : bpy.props.BoolProperty(name="Pointy Top", default=True) # type: ignore
    crystal_has_pointy_bottom : bpy.props.BoolProperty(name="Pointy Bottom", default=False) # type: ignore


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

        self.gen_radius = context.scene.crystal_generator.crystal_radius
        self.gen_height = context.scene.crystal_generator.crystal_height
        self.gen_vert_count = context.scene.crystal_generator.crystal_sides


        return self.execute(context)
        

classes = [
    GRP_crystal_generator_properties,
    MESH_OT_generate_procedural_crystal,
]   

def register_custom_icon() -> None:
    """ Registers the custom crystal generator icon """
    global custom_icons

    custom_icons = bpy.utils.previews.new()

    # Generate the path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_dir, 'data', 'crystal_generator.png')

    try:
        custom_icons.load('CRYSTAL_GENERATOR', icon_path, 'IMAGE')
    except Exception as e:
        crystal_gen_utils.log_console_message('error', f'Loading custom icon "{icon_path}" failed: {e}')

def unregister_cusom_icon() -> None:
    """ Unregisters the custom crystal generator icon """
    global custom_icons

    if not custom_icons:
        return

    bpy.utils.previews.remove(custom_icons)
    custom_icons = None

def menu_func(self, context) -> None:
    """ Adds the crystal generator to the "Add mesh" menu """
    self.layout.operator(MESH_OT_generate_procedural_crystal.bl_idname, icon_value=custom_icons['CRYSTAL_GENERATOR'].icon_id)

def register():
    register_custom_icon()

    ## CLASSES
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

    ## PROPS
    bpy.types.Scene.crystal_generator = bpy.props.PointerProperty(type=GRP_crystal_generator_properties)

def unregister():
    ## PROPS
    del bpy.types.Scene.crystal_generator

    ## CLASSES
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    unregister_cusom_icon()
    

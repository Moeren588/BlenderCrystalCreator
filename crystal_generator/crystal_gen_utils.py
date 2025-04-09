import bpy
import bmesh
import mathutils
import math

## --- HELPERS ---
def create_or_get_collection(collection_name:str, parent_collection_name:str=None) -> bpy.types.Collection:
    """Returns the collection with given name, creates it if it doesn't exist"""
    # Early return if collection already exists
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # Deal with parenting of new collection, IF specified
    if parent_collection_name:
        parent_collection = bpy.data.collections.get(parent_collection_name)
        # Check if parent collection actually exists
        if not parent_collection:
            log_console_message('ERROR', f'Parent collection {parent_collection_name} does not exist')
        else:
            bpy.context.scene.collection.children.unlink(collection)
            parent_collection.children.link(collection)

    return collection

def log_console_message(log_type:str, message:str) -> None:
    """"Logs a message to the console with color for log types"""
    match log_type.upper():
        case 'INFO': print(f'\033[34m[INFO]:\033[0m {message}')
        case 'WARNING': print(f'\033[33m[WARNING]:\033[0m {message}')
        case 'ERROR': print(f'\033[31m[ERROR]:\033[0m {message}')
        case 'FINISH': print(f'\033[32m[FINISHED]:\033[0m {message}')
        case 'SYS': print(f'\033[36m[SYSTEM]:\033[0m {message}')
        case 'DEBUG': print(f'\033[35m[DEBUG]:\033[0m {message}')
        case _: print(f'[{log_type.upper()}] : {message}')

### --- MESH GENERATION ---
def generate_prism_bmes(radius : float, height : float, vertices : int) -> bpy.types.Object:
    """Generates a simple procedural prism mesh """

    # Create the base object
    mesh_data = bpy.data.meshes.new("Chrystal_Mesh")
    obj = bpy.data.objects.new("Crystal_Object", mesh_data)
    
    collection = create_or_get_collection("Generated_Crystals")
    # TODO: Needing to unlink?
    collection.objects.link(obj)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bm = bmesh.new()
    
    # Create the base circle verts
    base_verts_data = bmesh.ops.create_circle(
        bm,
        cap_ends=False,
        radius=radius,
        segments=vertices
    )
    base_verts = base_verts_data['verts']
    base_edges = [e for e in bm.edges if all(v in base_verts for v in e.verts)]

    extruded_geom = bmesh.ops.extrude_edge_only(bm,edges=base_edges)

    # extruded_data = bmesh.ops.extrude_vert_indiv(bm, verts=base_verts)
    top_verts = [v for v in extruded_geom['geom'] if isinstance(v, bmesh.types.BMVert) and v not in base_verts ]

    translation_vector = mathutils.Vector((0, 0, height))
    bmesh.ops.translate(bm, vec=translation_vector, verts=top_verts)

    # Temp filling the top
    bmesh.ops.contextual_create(bm, geom=base_verts)
    bmesh.ops.contextual_create(bm, geom=top_verts)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    bm.to_mesh(mesh_data)

    # Free the bmesh instance
    bm.free()

    return obj
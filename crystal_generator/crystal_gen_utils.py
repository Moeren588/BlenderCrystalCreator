import bpy

def create_or_get_collection(collection_name:str, parent_collection_name:str=None) -> bpy.types.Collection:

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

    match log_type.upper():
        case 'INFO': print(f'\033[34m[INFO]:\033[0m {message}')
        case 'WARNING': print(f'\033[33m[WARNING]:\033[0m {message}')
        case 'ERROR': print(f'\033[31m[ERROR]:\033[0m {message}')
        case 'FINISH': print(f'\033[32m[FINISHED]:\033[0m {message}')
        case 'SYS': print(f'\033[36m[SYSTEM]:\033[0m {message}')
        case 'DEBUG': print(f'\033[35m[DEBUG]:\033[0m {message}')
        case _: print(f'[{log_type.upper()}] : {message}')
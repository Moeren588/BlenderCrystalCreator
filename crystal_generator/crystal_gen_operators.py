import bpy


classes = [

]

def register():
    ## GROUPS

    ## PROPS

    ## CLASSES
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    ## CLASSES
    for cls in classes.reverse():
        bpy.utils.unregister_class(cls)

    ## PROPS

    ## GROUPS
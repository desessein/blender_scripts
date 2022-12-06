import bpy


#WEIGHT TRANSFER
def transfer_weights(source, target, obj):
    source_group = obj.vertex_groups.get(source.name)
    if source_group is None:
        return
    source_i = source_group.index
    target_group = obj.vertex_groups.get(target.name)
    if target_group is None:
        target_group = obj.vertex_groups.new(name=target.name)
        
    for v in obj.data.vertices:
        for g in v.groups:
            if g.group == source_i:
                target_group.add((v.index,), g.weight, 'ADD')
    obj.vertex_groups.remove(source_group)
    

def transfer(source, target):
    for o in bpy.data.objects:
        transfer_weights(source, target, o)
    remove_bones(source.name)
        
def isArmature(object):
    return object.type == "ARMATURE"        

#BONE REMOVING
def remove_bones(bone_name):
    for object in bpy.data.objects:
        if(isArmature(object)):
            remove_bones_from_armature(object.data, bone_name)
             
def remove_bones_from_armature(armature, bone_name):
    for bone in armature.edit_bones:
        if(bone.name == bone_name):
            armature.edit_bones.remove(bone)

def main():
    for bone in source.children_recursive:
        remove_bone(bone, target)
    remove_bone(source, target)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bones = bpy.context.selected_editable_bones
        active = bpy.context.active_bone
        for bone in bones:
            if(bone != active):
                for child in bone.children_recursive:
                    transfer(child, active)
                transfer(bone, active)
                
        
#        if(len(bones) == 2):
#            target = bpy.context.active_bone
#            source = bones[0] if bones[0] != target else bones[1]
#            print("source " + source.name)
#            print("target " + target.name)
##             
#            for bone in source.children_recursive:
#                transfer(bone, target)
#            transfer(source, target)            
        
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.OUTLINER_MT_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.OUTLINER_MT_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()

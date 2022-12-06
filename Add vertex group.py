import bpy

def duplicate_active_armature():
    active = bpy.context.active_object.copy()
    bones = active.data.edit_bones[:]
    for bone in bones: 
        bone.name = "B" + bone.name
    active.name = "B" + active.name      
    bpy.context.collection.objects.link(active)

def duplicate_vertex_group():
    active = bpy.context.active_object
    for ob in bpy.context.selected_objects:
        me_source = active.data

        vertices_names = {}
        for i in range(0, len(active.vertex_groups)):
            groups = active.vertex_groups[i]
            vertices_names[groups.index] = groups.name

        data = {}  # vert_indices, [(vgroup_index, weights)]
        for v in me_source.vertices:
            vg = v.groups
            vi = v.index
            if len(vg) > 0:
                vgroup_collect = []
                for i in range(0, len(vg)):
                    vgroup_collect.append((vg[i].group, vg[i].weight))
                data[vi] = vgroup_collect
    #    # write data to target 
        if ob == active:
            # add missing vertex groups
            for vertice_index, vertice_name in vertices_names.items():
                #check if group already exists...
                already_present = 0
                for i in range(0, len(ob.vertex_groups)):
                    if ob.vertex_groups[i].name == vertice_name:
                        vertice_name = "bak "+vertice_name
                        vertices_names[vertice_index] = vertice_name
                # ... if not, then add
                if already_present == 0:
                    ob.vertex_groups.new(name=vertice_name)
    #        # write weights
            for v in me_source.vertices:
                for vi_source, weight in data.items():
                    if v.index == vi_source:
                        for i in range(0, len(weight)):
                            groupName = vertices_names[weight[i][0]]
                            groups = ob.vertex_groups
                            for vgs in range(0, len(groups)):
                                if groups[vgs].name == groupName:
                                    groups[vgs].add((v.index,),
                                       weight[i][1], "REPLACE")    
                                       
class SimpleVGDuplicator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_vg_duplicator"
    bl_label = "Simple Object Duplicator"
 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
      duplicate_vertex_group()
      return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleVGDuplicator.bl_idname, text=SimpleVGDuplicator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleVGDuplicator)
#    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleVGDuplicator)
#    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()
    
class SimpleArmDuplicator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_arm_duplicator"
    bl_label = "Simple Arm Duplicator"
 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
      duplicate_active_armature()
      return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleArmDuplicator.bl_idname, text=SimpleArmDuplicator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleArmDuplicator)
#    bpy.types.VIEW3D_MT_armature_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleArmDuplicator)
#    bpy.types.VIEW3D_MT_armature_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()
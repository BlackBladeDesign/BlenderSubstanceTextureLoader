import bpy
from bpy.types import Panel
from bpy.props import EnumProperty, StringProperty

from ..Operators.nm_operators import (LoadFromPath, AutoLoad)
from ..Props.nm_props import AutoTexProperties


class AutoTexPanel(bpy.types.Panel):
    """Creates a new tab in the shader editor options panel"""
    bl_label = "NodeMaster"
    bl_idname = "NODE_PT_autotex"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "NodeMaster"

    def draw(self, context):
        layout = self.layout
        # Main Controls
        row = layout.column()
        row.label(text="Set your path, load textures & nodes")
        row.operator("node.autoload", text="Load / Reload")
        row.operator("node.loadfrompath", text="Set Texture Path")
        row.operator("node.loadJSON", text="Load Node Tree (JSON)")
        row.operator("node.exportJSON", text="Export Node Tree (JSON)")

class nodeStructurePanel(bpy.types.Panel):
    bl_label = "Node Structure Settings"
    bl_idname = "NODE_PT_autotex_nsSettings"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_autotex"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # Sub-panel for material settings
        layout = self.layout
        # Main buttons and path
        row = layout.column()
        row.prop(context.scene.auto_tex_props, "loadTextures", text="Load Image Textures")  
        row.prop(context.scene.auto_tex_props, "apply_to", text=" Apply To")
        row.prop(context.scene.auto_tex_props, "node_structure", text=" Node Structure")
        

class fileSettingsPanel(bpy.types.Panel):
    bl_label = "File Settings"
    bl_idname = "NODE_PT_autotex_fileSettings"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_autotex"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    @classmethod
    def poll(cls, context):
        return context.scene.auto_tex_props.loadTextures

    def draw(self, context):
        # Sub-panel for material settings
        layout = self.layout
        # Main buttons and path
        row = layout.column()
        row.prop(context.scene.auto_tex_props, "texturePath", text="Texture Path")
        row.prop(context.scene.auto_tex_props, "image_file_type", text=" File Type")

        


        
class matSettingsPanel(bpy.types.Panel):
    bl_label = "Material Settings"
    bl_idname = "NODE_PT_autotex_matSettings"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_autotex"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # Sub-panel for material settings
        layout = self.layout

        # Main buttons and path
        row = layout.column()
        row.prop(context.scene.auto_tex_props, "gltf_Node", text="GLTF/GLB Output")
        row.prop(context.scene.auto_tex_props, "displacement", text="Displacment")
        row.prop(context.scene.auto_tex_props, "texCoord", text="Tex Co-ord")


class texSuffixPanel(bpy.types.Panel):        
    bl_label = "Texture Suffixes"
    bl_idname = "NODE_PT_autotex_texSuffix"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_autotex"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        layout = self.layout
        # Main buttons and path
        row2 = layout.column()
        row2.prop(context.scene.auto_tex_props, "normal_map", text="- Normal Map")
        row2.prop(context.scene.auto_tex_props, "base_color", text="- Base Color")
        if context.scene.auto_tex_props.node_structure == "ORM_GLB":
            row2.prop(context.scene.auto_tex_props, "orm_texture", text="- ORM")
        if context.scene.auto_tex_props.node_structure == "BLENDER_BSDF":
            row2.prop(context.scene.auto_tex_props, "roughness_texture", text="- Roughness")
            row2.prop(context.scene.auto_tex_props, "metallic_texture", text="- Metallic")
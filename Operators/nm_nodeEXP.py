import bpy
import os
import json
from bpy.props import StringProperty
from bpy.types import Operator


class ImportNodes(Operator):
    bl_label = "Import Nodes"
    bl_idname = "node.loadjson"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Open the file browser to select a file
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

        # Load the JSON data from the selected file
        with open(self.filepath, 'r') as f:
            data = json.load(f)

        # Create a new material and node tree
        mat = bpy.data.materials.new(name="My Material")
        nodes = mat.node_tree.nodes

        # Loop through the nodes in the JSON data and create Blender nodes
        for node_data in data["nodes"]:
            node = nodes.new(type=node_data["type"])
            node.name = node_data["name"]
            node.location = node_data["location"]

            # Loop through the inputs for this node and set their default values
            for input_data in node_data.get("inputs", []):
                input_socket = node.inputs.get(input_data["name"])
                if input_socket:
                    if input_socket.type == 'RGBA':
                        input_socket.default_value = (input_data["default_value"][0], input_data["default_value"][1], input_data["default_value"][2], input_data["default_value"][3])
                    else:
                        input_socket.default_value = input_data["default_value"]

        # Loop through the links in the JSON data and create Blender links
        for link_data in data["links"]:
            from_node = nodes.get(link_data["from_node"])
            to_node = nodes.get(link_data["to_node"])
            if from_node and to_node:
                from_socket = from_node.outputs.get(link_data["from_output"])
                to_socket = to_node.inputs.get(link_data["to_input"])
                if from_socket and to_socket:
                    mat.node_tree.links.new(from_socket, to_socket)

        # Set the active material to the new material
        bpy.context.view_layer.objects.active = bpy.context.active_object
        bpy.context.active_object.active_material = mat

        return {'FINISHED'}
    
class ExportNodes(Operator):
    bl_label = "Export Nodes"
    bl_idname = "node.exportjson"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    def execute(self, context):
        # Get the active material and node tree
        mat = bpy.context.active_object.active_material
        if mat is None:
            self.report({'ERROR'}, "No material selected")
            return {'CANCELLED'}
        nodes = mat.node_tree.nodes

        # Create a dictionary to hold the node and link data
        data = {"nodes": [], "links": []}

        # Loop through the nodes in the node tree and add their data to the dictionary
        for node in nodes:
            node_data = {"name": node.name, "type": node.bl_idname, "location": node.location.to_tuple()}
            input_data_list = []
            for input_socket in node.inputs:
                if input_socket.type == 'SHADER':
                    continue
                input_data = {"name": input_socket.name}
                if input_socket.default_value is not None:
                    if isinstance(input_socket.default_value, bpy.types.bpy_prop_array):
                        input_data["default_value"] = list(input_socket.default_value)
                    else:
                        input_data["default_value"] = input_socket.default_value
                input_data_list.append(input_data)
            node_data["inputs"] = input_data_list
            data["nodes"].append(node_data)

        # Loop through the links in the node tree and add their data to the dictionary
        for link in mat.node_tree.links:
            link_data = {"from_node": link.from_node.name, "from_output": link.from_socket.name,
                        "to_node": link.to_node.name, "to_input": link.to_socket.name}
            data["links"].append(link_data)

        # Save the data to the selected file as JSON
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

        return {'FINISHED'}

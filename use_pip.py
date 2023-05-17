bl_info = {
    "name" : "usePip",
    "blender": (3, 2, 2),
    "category": "System",
}

import bpy
from bpy.types import Operator, Panel, Menu
from bpy.props import StringProperty

import pip

import sys
import subprocess
from pathlib import Path, PureWindowsPath

#### Use Pip function
class usePip(Operator):
    """-"""
    bl_idname = "system.use_pip"
    bl_label = "Run Pip"
    bl_option = {"REGISTER"}
    
    package_name : StringProperty(
        name="Package Name",
        default="icecream",
        )
    
    def execute(self, context):
        settings = context.preferences.addons[__name__].preferences
        base_path = Path(settings.blender_base_path)
        #print(base_path)
        
        target_path = base_path / "Blender 3.2\\3.2\\python\\lib\\site-packages"
        #print(target_path)
        
        print(sys.executable)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', self.package_name, '-t', target_path])
           
        return {"FINISHED"}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
        
#### Addon preferences    
class usePipPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    blender_base_path: StringProperty(
        name="Blender Base Path",
        default="C:\Program Files\Blender Foundation",
        description="Choose the Blender installation path",
        subtype="DIR_PATH"
        )
        
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "blender_base_path")
 
#### Custom menu       
class pipMenu(Menu):
    bl_label = "Use Pip"
    bl_idname = "SYSTEM_MT_usepip"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator(usePip.bl_idname)

def draw_item(self, context):
    layout = self.layout
    
    layout.operator_context = "INVOKE_DEFAULT"
    layout.menu(pipMenu.bl_idname, text="Install Python Script...")


###############################################
classes = (usePip, usePipPrefs, pipMenu)

reg, unreg = bpy.utils.register_classes_factory(classes)

def register():
    reg()
    bpy.types.TOPBAR_MT_editor_menus.append(draw_item)
        
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_item)
    unreg()
    
if __name__ == "__main__":
    print(__name__)
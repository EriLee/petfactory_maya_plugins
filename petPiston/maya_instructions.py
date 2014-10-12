import maya.cmds as cmds
import pymel.core as pm

# delete all nodes, and flush undo to safely unload the plugin
pm.delete([node for node in pm.ls() if isinstance(node, pm.nodetypes.petSine)])
pm.flushUndo()

cmds.unloadPlugin('petSine.py', force=True)
cmds.loadPlugin('petSine.py')
#cmds.createNode('petSine')
cmds.shadingNode('petSine', asUtility=True)
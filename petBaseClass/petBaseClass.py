import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
kPluginNodeName = 'petBaseClass' 

kPluginNodeClassify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
kPluginNodeId = OpenMaya.MTypeId(0x0)

class petBootstrap(OpenMayaMPx.MPxNode):

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute():
		pass





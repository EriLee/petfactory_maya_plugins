import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class PetJiggleTransform(OpenMayaMPx.MPxNode):

	kPluginNodeId = OpenMaya.MTypeId(0x00000010)

	def __ini__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, data):
		pass

# creates the object for maya
def creator():
	return OpenMayaMPx.asMPxPtr(PetJiggleTransform())

# creates the node attributes
def initialize():
	pass

# initializes the plug-in in maya
def initializePlugin(obj):
	fnPlugin = OpenMayaMPx.MFnPlugin(obj, 'Petfactory', '1.0', 'Any')
	fnPlugin.registerNode('petJiggleTransform', PetJiggleTransform.kPluginNodeId, creator, initialize)

# uninitializes the plug-in in maya

def uninitializePlugin(obj):
	fnPlugin = OpenMayaMPx.MFnPlugin(obj)
	fnPlugin.deregisterNode(PetJiggleTransform.kPluginNodeId)

import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petBaseClass' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x0)

class petBaseClass(OpenMayaMPx.MPxNode):

	# define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
	in_input = OpenMaya.MObject()
	out_output = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, data_block):

		if plug == petBaseClass.out_output:

			#--------------------
			# INPUT
			#--------------------
			# get the datahandle from the data block
			input_data_handle = data_block.inputValue(petBaseClass.in_input)

			# get the data (float in this case) from the data handle
			input_val = input_data_handle.asFloat()

			#--------------------
			# COMPUTE
			#--------------------
			out_value = input_val * .5

			#--------------------
			# OUTPUT
			#--------------------
			# get the datahandle from the data block
			output_data_handle = data_block.outputValue(petBaseClass.out_output)
			output_data_handle.setFloat(out_value)

			# mark the plug clean
			data_block.setClean(plug)

		# we are only expecting the 
		else:
			return OpenMaya.kUnknownParameter


def nodeCreator():
	# create an instance and return a pointer MObj to it
	return OpenMayaMPx.asMPxPtr(petBaseClass())

def nodeInitializer():
	# create a function set for numeric attributes, will be used as a
	# factory to create attributes, they will be returned as MObj
	mfn_attr = OpenMaya.MFnNumericAttribute()

	#--------------------
	# INPUT
	#--------------------
	# create an attr. params: longname, shortname, datatype, default
	petBaseClass.in_input = mfn_attr.create('input', 'i', OpenMaya.MFnNumericData.kFloat, 0,0)
	# set the properties of the attr
	mfn_attr.setReadable(1)
	mfn_attr.setWriteable(1)
	mfn_attr.setStorable(1)
	mfn_attr.setKeyable(1)

	#--------------------
	# OUTPUT
	#--------------------
	# create an attr. params: longname, shortname, datatype, default
	# NOTE that output value has no default value (it will be computed)
	petBaseClass.out_output = mfn_attr.create('output', 'o', OpenMaya.MFnNumericData.kFloat)
	# set the properties of the attr
	# NOTE only readable
	mfn_attr.setReadable(1)
	mfn_attr.setWriteable(0)
	mfn_attr.setStorable(0)
	mfn_attr.setKeyable(0)


	#--------------------
	# ADD ATTR TO NODE
	#--------------------
	petBaseClass.addAttribute(petBaseClass.in_input)
	petBaseClass.addAttribute(petBaseClass.out_output)

	#--------------------
	# SETUP DEPENDENCY
	#--------------------
	# which attributes needs to be updated if an attribute is changed
	petBaseClass.attributeAffects(petBaseClass.in_input, petBaseClass.out_output)

def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(	node_name,
        						node_id,
        						nodeCreator,
        						nodeInitializer,
        						OpenMayaMPx.MPxNode.kDependNode,
        						node_classify)
    except:
        sys.stderr.write( 'Failed to register node: ' + node_name )
        raise


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(node_id)
    except:
        sys.stderr.write( 'Failed to deregister node: ' + node_name )
        raise





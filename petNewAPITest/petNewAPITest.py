import sys, math
import maya.api.OpenMaya as OpenMaya  
from maya import OpenMayaMPx

# The name of the node.
node_name = 'petNewAPITest' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00009)

class petNewAPITest(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_input = OpenMaya.MObject()
    out_output = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petNewAPITest.out_output:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block
            input_data_handle = data_block.inputValue(petNewAPITest.in_input)

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
            output_data_handle = data_block.outputValue(petNewAPITest.out_output)
            output_data_handle.setFloat(out_value)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petNewAPITest())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    mfn_attr = OpenMaya.MFnNumericAttribute()
    kFloat = OpenMaya.MFnNumericData.kFloat

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    petNewAPITest.in_input = mfn_attr.create('input', 'i', kFloat, 0.0)
    # set the properties of the attr
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    #--------------------
    # OUTPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # NOTE that output value has no default value (it will be computed)
    petNewAPITest.out_output = mfn_attr.create('output', 'o', kFloat)
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(0)
    mfn_attr.setStorable(0)
    mfn_attr.setKeyable(0)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petNewAPITest.addAttribute(petNewAPITest.in_input)
    petNewAPITest.addAttribute(petNewAPITest.out_output)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petNewAPITest.attributeAffects(petNewAPITest.in_input, petNewAPITest.out_output)

def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(   node_name,
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


def maya_useNewAPI():
    pass
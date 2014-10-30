import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petMatrix' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00005)

class petMatrix(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_matrix = OpenMaya.MObject()
    out_matrix = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petMatrix.out_matrix:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block
            in_matrix_datahandle = data_block.inputValue(petMatrix.in_matrix)

            # get the data (float in this case) from the data handle
            in_matrix_value = in_matrix_datahandle.asFloat()

            #--------------------
            # COMPUTE
            #--------------------
            out_matrix_value = in_matrix_value

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            output_data_handle = data_block.outputValue(petMatrix.out_output)
            output_data_handle.setFloat(out_value)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petMatrix())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    mfn_attr = OpenMaya.MFnNumericAttribute()
    kFloat = OpenMaya.MFnNumericData.kFloat

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    petMatrix.in_input = mfn_attr.create('input', 'i', kFloat, 0.0)
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
    petMatrix.out_output = mfn_attr.create('output', 'o', kFloat)
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(0)
    mfn_attr.setStorable(0)
    mfn_attr.setKeyable(0)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petMatrix.addAttribute(petMatrix.in_input)
    petMatrix.addAttribute(petMatrix.out_output)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petMatrix.attributeAffects(petMatrix.in_input, petMatrix.out_output)

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
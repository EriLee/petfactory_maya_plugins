import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petModulo' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00003)

class petModulo(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_input = OpenMaya.MObject()
    in_modulo = OpenMaya.MObject()
    out_result = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petModulo.out_result:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block and value from the datahandle
            in_input_datahandle = data_block.inputValue(petModulo.in_input)
            in_input_value = in_input_datahandle.asFloat()

            in_modulo_datahandle = data_block.inputValue(petModulo.in_modulo)
            in_modulo_value = in_modulo_datahandle.asFloat()

            #--------------------
            # COMPUTE
            #--------------------
            out_result_value = in_input_value % in_modulo_value

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_result_datahandle = data_block.outputValue(petModulo.out_result)
            out_result_datahandle.setFloat(out_result_value)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petModulo())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    mfn_attr = OpenMaya.MFnNumericAttribute()
    kFloat = OpenMaya.MFnNumericData.kFloat

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    petModulo.in_input = mfn_attr.create('input', 'i', kFloat, 0.0)
    # set the properties of the attr
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    # create an attr. params: longname, shortname, datatype, default
    petModulo.in_modulo = mfn_attr.create('modulo', 'm', kFloat, 1.0)
    # set the properties of the attr
    mfn_attr.setMin(1.0)
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    #--------------------
    # OUTPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # NOTE that output value has no default value (it will be computed)
    petModulo.out_result = mfn_attr.create('result', 'r', kFloat)
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(0)
    mfn_attr.setStorable(0)
    mfn_attr.setKeyable(0)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petModulo.addAttribute(petModulo.in_input)
    petModulo.addAttribute(petModulo.in_modulo)
    petModulo.addAttribute(petModulo.out_result)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petModulo.attributeAffects(petModulo.in_input, petModulo.out_result)
    petModulo.attributeAffects(petModulo.in_modulo, petModulo.out_result)

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
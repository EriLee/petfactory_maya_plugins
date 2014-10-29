import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petSine' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00001)

class petSine(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_angle = OpenMaya.MObject()
    in_angle_offset = OpenMaya.MObject()
    in_angle_scale = OpenMaya.MObject()
    in_radius = OpenMaya.MObject()
    out_result = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petSine.out_result:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block, and the value from the handle
            in_angle_datahandle = data_block.inputValue(petSine.in_angle)
            in_angle_value = in_angle_datahandle.asFloat()

            in_angle_offset_datahandle = data_block.inputValue(petSine.in_angle_offset)
            in_angle_offset_value = in_angle_offset_datahandle.asFloat()

            in_angle_scale_datahandle = data_block.inputValue(petSine.in_angle_scale)
            in_angle_scale_value = in_angle_scale_datahandle.asFloat()

            in_radius_datahandle = data_block.inputValue(petSine.in_radius)
            in_radius_value = in_radius_datahandle.asFloat()

            #--------------------
            # COMPUTE
            #--------------------
            out_result_value = math.sin((in_angle_value+in_angle_offset_value)*in_angle_scale_value)*in_radius_value

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_result_datahandle = data_block.outputValue(petSine.out_result)
            out_result_datahandle.setFloat(out_result_value)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petSine())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    mfn_attr = OpenMaya.MFnNumericAttribute()
    kFloat = OpenMaya.MFnNumericData.kFloat

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    petSine.in_angle = mfn_attr.create('angle', 'a', kFloat, 0.0)
    # set the properties of the attr
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    # create an attr. params: longname, shortname, datatype, default
    petSine.in_angle_offset = mfn_attr.create('angleOffset', 'ao', kFloat, 1.0)
    # set the properties of the attr
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    # create an attr. params: longname, shortname, datatype, default
    petSine.in_angle_scale = mfn_attr.create('angleScale', 'as', kFloat, 1.0)
    # set the properties of the attr
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(1)
    mfn_attr.setStorable(1)
    mfn_attr.setKeyable(1)

    # create an attr. params: longname, shortname, datatype, default
    petSine.in_radius= mfn_attr.create('radius', 'r', kFloat, 1.0)
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
    petSine.out_result = mfn_attr.create('result', 're', kFloat)
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(1)
    mfn_attr.setWritable(0)
    mfn_attr.setStorable(0)
    mfn_attr.setKeyable(0)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petSine.addAttribute(petSine.in_angle)
    petSine.addAttribute(petSine.in_angle_offset)
    petSine.addAttribute(petSine.in_angle_scale)
    petSine.addAttribute(petSine.in_radius)
    petSine.addAttribute(petSine.out_result)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petSine.attributeAffects(petSine.in_angle, petSine.out_result)
    petSine.attributeAffects(petSine.in_angle_offset, petSine.out_result)
    petSine.attributeAffects(petSine.in_angle_scale, petSine.out_result)
    petSine.attributeAffects(petSine.in_radius, petSine.out_result)

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
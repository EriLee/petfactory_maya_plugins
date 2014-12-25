import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class PetJiggleTransform(OpenMayaMPx.MPxNode):

	kPluginNodeId = OpenMaya.MTypeId(0x00000010)

	out_output = OpenMaya.MObject()
	in_goal = OpenMaya.MObject()
	in_damping = OpenMaya.MObject()
	in_stiffness = OpenMaya.MObject()
	in_time = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		self._initialized = False
		self._curr_pos = OpenMaya.MPoint()
		self._prev_pos = OpenMaya.MPoint()
		self._prev_time = OpenMaya.MTime()

	def compute(self, plug, data):
		if plug != PetJiggleTransform.out_output:
			return OpenMaya.kUnknownParameter

		# get the inputs
		damping = data.inputValue(self.in_damping).asFloat()
		stiffness = data.inputValue(self.in_stiffness).asFloat()
		goal = OpenMaya.MPoint(data.inputValue(self.in_goal).asFloatVector())
		# make sure that node refreshes it self
		curr_time = data.inputValue(self.in_time).asTime()

		# when the node is first used, set the curr and prev pos to the goal
		# to avoid an extreme jiggle from the default value (0) to the goal
		if not self._initialized:
			self._prev_time = curr_time
			self._curr_pos = goal
			self._prev_pos = goal
			self._initialized = True

		# check if the timestep is just 1 frame since we want a stable simulation
		# note that we will evaluate the jiggle if the timestep is 0, this will
		# allow interactive simulation (when the user interacts with the node,
		# but the timeslider is not playing)
		time_diff = curr_time.value() - self._prev_time.value()
		if time_diff > 1.0 or time_diff < 0.0:
			self._initialized = False
			self._prev_time = curr_time
			data.setClean(plug)
			return

		velocity = (self._curr_pos - self._prev_pos) * (1.0 - damping)
		new_pos = self._curr_pos + velocity
		goal_force = (goal - new_pos) * stiffness
		new_pos += goal_force

		# store the states for the next computation
		self._prev_pos = OpenMaya.MPoint(self._curr_pos)
		self._curr_pos = OpenMaya.MPoint(new_pos)
		self._prev_time = OpenMaya.MTime(curr_time)

		h_output = data.outputValue(PetJiggleTransform.out_output)
		out_vec = OpenMaya.MFloatVector(new_pos.x, new_pos.y, new_pos.z)
		h_output.setMFloatVector(out_vec)
		h_output.setClean()
		data.setClean(plug)


# creates the object for maya
def creator():
	return OpenMayaMPx.asMPxPtr(PetJiggleTransform())

# creates the node attributes
def initialize():
	
	n_attr = OpenMaya.MFnNumericAttribute()
	u_attr = OpenMaya.MFnUnitAttribute()
	
	# add output (point) attr
	PetJiggleTransform.out_output = n_attr.createPoint('output', 'o')
	n_attr.setWritable(False)
	n_attr.setStorable(False)
	PetJiggleTransform.addAttribute(PetJiggleTransform.out_output)

	# add goal (point)in attr
	PetJiggleTransform.in_goal = n_attr.createPoint('goal', 'g')
	PetJiggleTransform.addAttribute(PetJiggleTransform.in_goal)
	PetJiggleTransform.attributeAffects(PetJiggleTransform.in_goal, PetJiggleTransform.out_output)

	# add stiffness (float) in attr
	PetJiggleTransform.in_stiffness = n_attr.create('stiffness', 's', OpenMaya.MFnNumericData.kFloat, 1.0)
	n_attr.setKeyable(True)
	n_attr.setMin(0.0)
	n_attr.setMax(1.0)
	PetJiggleTransform.addAttribute(PetJiggleTransform.in_stiffness)
	PetJiggleTransform.attributeAffects(PetJiggleTransform.in_stiffness, PetJiggleTransform.out_output)

	# add damping (float) in attr
	PetJiggleTransform.in_damping = n_attr.create('damping', 'd', OpenMaya.MFnNumericData.kFloat, 1.0)
	n_attr.setKeyable(True)
	n_attr.setMin(0.0)
	n_attr.setMax(1.0)
	PetJiggleTransform.addAttribute(PetJiggleTransform.in_damping)
	PetJiggleTransform.attributeAffects(PetJiggleTransform.in_damping, PetJiggleTransform.out_output)

	# add time (time) in attr
	# this attr will make sure that the jiggle will compute (and complete) on each frame update,
	# even if none of the other inputs attributes are changed
	PetJiggleTransform.in_time = u_attr.create('time', 't', OpenMaya.MFnUnitAttribute.kTime, 0.0)
	PetJiggleTransform.addAttribute(PetJiggleTransform.in_time)
	PetJiggleTransform.attributeAffects(PetJiggleTransform.in_time, PetJiggleTransform.out_output)



# initializes the plug-in in maya
def initializePlugin(obj):
	fnPlugin = OpenMayaMPx.MFnPlugin(obj, 'Petfactory', '1.0', 'Any')
	fnPlugin.registerNode('petJiggleTransform', PetJiggleTransform.kPluginNodeId, creator, initialize)

# uninitializes the plug-in in maya

def uninitializePlugin(obj):
	fnPlugin = OpenMayaMPx.MFnPlugin(obj)
	fnPlugin.deregisterNode(PetJiggleTransform.kPluginNodeId)

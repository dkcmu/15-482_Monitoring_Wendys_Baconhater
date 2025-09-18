import rclpy, rclpy.node
import ros_hardware, layers
import sys, select
from terrabot_utils import time_since_midnight, set_use_sim_time, spin_for, get_ros_time
from terrabot_utils import clock_time
import greenhouse_behaviors as gb

def check_for_input():
    if sys.stdin in select.select([sys.stdin],[],[],0)[0]:
        input = sys.stdin.readline()
        if input[0] == 'q':
            quit()
        else:
            print("Usage: q (quit)")

class GreenhouseAgent(rclpy.node.Node):
    def __init__(self, agentName, use_sim):
        super().__init__(agentName)
        set_use_sim_time(self, use_sim)
        # Wait for clock to start up correctly
        while get_ros_time(self) == 0: spin_for(self, 0.1)

    # Often the agent starts running before sensor data is received
    # This waits for some data to have been received, assuming the real
    # sensor values are not zero
    def wait_for_sensors(self, sensors):
        while sensors.weight == 0 or sensors.moisture == 0:
            #print("Wait")
            spin_for(self, .25)

class BehavioralGreenhouseAgent(GreenhouseAgent):

    def __init__(self, use_sim):
        super().__init__("greenhouseagent_behavioral", use_sim)

        # Initialize ROSSensors, ROSActuators, and behaviors,
        #  save each of them as instance variables, and pass them all
        #  to instantiate a BehavioralLayer
        self.sensors = ros_hardware.ROSSensors(self)
        # BEGIN STUDENT CODE
        self.actuators = ros_hardware.ROSActuators(self)
        self.behaviors = [
            gb.Light(self),
            gb.LowerHumid(self),
            gb.LowerSMoist(self),
            gb.LowerTemp(self),
            gb.RaiseSMoist(self),
            gb.RaiseTemp(self)
        ]
        behavioral_layer = layers.BehavioralLayer(self.sensors, self.actuators, self.behaviors, self)
        self.setBehavioralLayer(behavioral_layer)
        # END STUDENT CODE

    def setBehavioralLayer(self, behavioral):
        self.behavioral = behavioral
    def getBehavioralLayer(self):
        return self.behavioral

    def main(self):
        self.wait_for_sensors(self.sensors)
        self.getBehavioralLayer().startAll()
        while rclpy.ok():
            # Run a step of the behavioral architecture
            self.getBehavioralLayer().doStep()
            spin_for(self, 1)
            check_for_input()

class LayeredGreenhouseAgent(GreenhouseAgent):

    def __init__(self, use_sim, schedulefile):
        super().__init__("greenhouseagent_layered", use_sim)

        # Initialize the architecture:
        # As with the behavioral agent, initialize ROSSensors, ROSActuators,
        #  and all behaviors, save each of them as instance variables, and
        #  pass them all to instantiate a BehavioralLayer.
        # In addition, create executive and planning layers, and set the
        #  connections between the layers, using the appropriate functions
        #  defined in the executive and planning classes.  In particular,
        #  connect the behavioral and planning layers to the executive, and
        #  the executive to the planning layer.
        # Don't forget to have the planning layer invoke getNewSchedule
        self.sensors = ros_hardware.ROSSensors(self)
        # BEGIN STUDENT CODE
        self.actuators = ros_hardware.ROSActuators(self)
        self.behaviors = [
            gb.Light(self),
            gb.LowerHumid(self),
            gb.LowerSMoist(self),
            gb.LowerTemp(self),
            gb.RaiseSMoist(self),
            gb.RaiseTemp(self)
        ]
        behavioral = layers.BehavioralLayer(self.sensors, self.actuators, self.behaviors, self)
        self.setBehavioralLayer(behavioral)

        executive = layers.ExecutiveLayer(self)
        self.setExecutiveLayer(executive)

        planning = layers.PlanningLayer("greenhouse_schedule.txt", self)
        self.setPlanningLayer(planning)
        # END STUDENT CODE

    def setBehavioralLayer(self, behavioral):
        self.behavioral = behavioral
    def getBehavioralLayer(self):
        return self.behavioral
    
    def setExecutiveLayer(self, executive):
        self.executive = executive
    def getExecutiveLayer(self):
        return self.executive
    
    def setPlanningLayer(self, planning):
        self.planning = planning
    def getPlanningLayer(self):
        return self.planning

    def main(self):
        self.wait_for_sensors(self.sensors)
        while rclpy.ok():
            t = time_since_midnight(get_ros_time(self))
            # Run a step of each layer of the architecture
            self.getPlanningLayer().doStep(t)
            self.getExecutiveLayer().doStep(t)
            self.getBehavioralLayer().doStep()
            spin_for(self, 1)
            check_for_input()

if __name__ == '__main__':
    rclpy.init()
    sim = "-m" in sys.argv and "sim" in sys.argv
    if "-B" in sys.argv:
        print("Starting Behavioral Agent")
        agent = BehavioralGreenhouseAgent(sim)
        agent.main()
    elif "-L" in sys.argv:
        print("Starting Layered Agent")
        agent = LayeredGreenhouseAgent(sim, "greenhouse_schedule.txt")
        agent.main()
    else:
        print("Need to specify either behavioral (-B) or layered (-L) architecture")

__author__ = 'Abel Correa, phd.abel@gmail.com'

#from scipy import clip, asarray
#from numpy import *
from pybrain.rl.environments.task import Task
from lowlevelagent.lowlevelagent import LowLevelAgent
import traci

class Plan(Task):

	#penalidades
	bangPenalty = -1
	defaultPenalty = 0
	finalReward = 1
	#dados do trafficlight
	trafficlight = None

	def __init__(self, environment, trafficlight):
		#atribui o ambiente que deve ser passado como parametro apos ser instanciado
		#juntamente com os ids do induction loop vertical e horizontal
		self.env = environment
		if(isinstance(trafficlight, LowLevelAgent)):
			self.trafficlight = trafficlight
	
	def performAction(self, action):
		return self.env.performAction(self.trafficlight, action)
	
	def getObservation(self):
		#retorna estado do ambiente
		sensors = self.env.getSensors(self.trafficlight.horizontal_edge, self.trafficlight.vertical_edge)
		return sensors
	
	def getReward(self):
		currentAction = traci.trafficlights.getProgram(self.trafficlight.id)
		currentAction = int(currentAction)
				
		if(self.getObservation()[0] == 0 and currentAction == 0):
			cur_reward = self.finalReward
		elif(self.getObservation()[0] == 2 and currentAction == 1):
			cur_reward = self.finalReward
		elif(self.getObservation()[0] == 1 and currentAction == 2):
			cur_reward = self.finalReward
		elif(self.getObservation()[0] == 2 and currentAction == 2):
			cur_reward = self.bangPenalty
		elif(self.getObservation()[0] == 1 and currentAction == 1):
			cur_reward = self.bangPenalty
		else:
			cur_reward = self.defaultPenalty

		return cur_reward
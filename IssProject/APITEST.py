from Backend import ServerAPI
from Backend.DataStore.AccessLayer import ASTRONAUT

#ServerAPI.registerUserMfaAccount("adamcoxemail@gmail.com","07763755656","44")
#ServerAPI.registerAstronautsEmail("bob@gmail.com")

#print(ServerAPI.getAstronautsStates())
print(ServerAPI.launchShuttle(1,[]))
state= ServerAPI.getShuttlesStates()
print(state[0].location)
#print(getAvailibleItems())
#print(consumeResource(1,10))
#print(getResourceQuantity(1))
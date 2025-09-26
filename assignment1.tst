BASELINE = assignment1.bsl

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

# Ensure moisture within limits
ENSURE smoist < limits['moisture'][1] FOR 360000
ENSURE smoist >= limits['moisture'][0] FOR 360000

# Ensure light level within limits
ENSURE light < limits['light_level'][1] FOR 360000
ENSURE light >= limits['light_level'][0] FOR 360000

# Ensure temperature within limits
ENSURE temp < limits['temperature'][1] FOR 360000
ENSURE temp >= limits['temperature'][0] FOR 360000

# Ensure humidity within limits
ENSURE humid < limits['humidity'][1] FOR 360000
ENSURE humid >= limits['humidity'][0] FOR 360000

# Ensure weight within limits
ENSURE weight < limits['weight'][1] FOR 360000
ENSURE weight >= limits['weight'][0] FOR 360000

# Ensure water level within limits
ENSURE level < limits['water_level'][1] FOR 360000
ENSURE level >= limits['water_level'][0] FOR 360000

# Ensure led off if light too high
WHENEVER light > optimal['light_level'][1] WHILE light > optimal['light_level'][1]
  ENSURE disabled(led)

# Ensure fan off if temperature too low
WHENEVER temp < optimal['temperature'][0] WHILE temp < optimal['temperature'][0]
  ENSURE disabled(fan)

# Ensure pump off if moisture too high
WHENEVER smoist > optimal['moisture'][1] WHILE smoist > optimal['moisture'][1]
  ENSURE disabled(wpump)

# Ensure led off if temperature too high
WHENEVER temp > optimal['temperature'][1] WHILE temp > optimal['temperature'][1]
  ENSURE disabled(led)

# Ensure fan off if humidity too low
WHENEVER humid < optimal['humidity'][0] WHILE humid < optimal['humidity'][0]
  ENSURE disabled(fan)

# Ensure pump off if humidity too high?
WHENEVER humid > optimal['humidity'][1] WHILE humid < optimal['humidity'][1]
  ENSURE disabled(wpump)

# Ensure pump off if weight too high
WHENEVER weight > optimal['weight'][1] WHILE weight < optimal['weight'][1]
  ENSURE disabled(wpump)

# Ensure pump off if water level too low
WHENEVER level < optimal['water_level'][0] WHILE level < optimal['water_level'][0]
  ENSURE disabled(wpump)
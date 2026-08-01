# PRD Document for simpy

## Introduction

SimPy is a process-based discrete-event simulation framework built on standard Python that uses generator functions to define processes. These processes can model active components like customers, vehicles, or agents, and the framework provides various types of shared resources to model limited capacity congestion points such as servers, checkout counters, and tunnels. Simulations can be performed "as fast as possible", in real time (wall clock time), or by manually stepping through events. While continuous simulations are theoretically possible with SimPy, it has no features specifically designed for that purpose, and it's not well-suited for simulations with fixed step sizes where processes don't interact with each other or shared resources.

## Goals

SimPy's design goals have evolved across versions, with SimPy 3 focusing on simplification and modernization of the framework. The primary objectives were to simplify and PEP8-ify the API while cleaning up and modularizing the framework's internals. One of SimPy's main goals is to be easy to use, which is reflected in its design where processes no longer require subclassing and can be simple module-level functions. The framework also adopted a more focused approach by removing some "batteries included" features like plotting and GUI capabilities, since dedicated libraries like matplotlib do a better job at these tasks.

## Features and Functionalities

The following features and functionalities are expected in the project:

### Simulation Environment Management
- Ability to create discrete-event simulation environments that step from event to event 
- Ability to run simulations "as fast as possible", in real time (wall clock time), or by manually stepping through events
- Ability to set custom initial simulation time for the environment 
- Ability to track current simulation time 
- Ability to synchronize simulation time with real-time (wall-clock time) using configurable scaling factors

### Process-Based Simulation
- Ability to define processes using Python generator functions 
- Ability to model active components like customers, vehicles, or agents as processes  
- Ability to suspend process execution by yielding events 
- Ability to interrupt processes during their execution with optional cause information  
- Ability to track the currently active process 

### Event Types and Management
- Ability to create basic events that can be triggered with success or failure states  
- Ability to schedule timeout events that trigger after a specified delay  
- Ability to combine events using logical AND operator to wait for all events  
- Ability to combine events using logical OR operator to wait for any event  
- Ability to attach callbacks to events that execute when events are processed  
- Ability to defuse failed events to prevent exception propagation 

### Resource Management
- Ability to model limited capacity resources with configurable number of usage slots  
- Ability to request and release resource usage through request/release pattern 
- Ability to prioritize resource requests using priority values 
- Ability to preempt lower-priority resource users with higher-priority requests 
- Ability to automatically release resources when using context managers (with statement)  

### Container Resources
- Ability to model resources containing continuous or discrete matter (like water or apples) 
- Ability to put specified amounts of matter into containers 
- Ability to get specified amounts of matter from containers 
- Ability to configure container capacity and initial level 
- Ability to track current level of matter in containers 

### Store Resources
- Ability to store arbitrary objects in FIFO (first-in, first-out) order  
- Ability to store objects in priority order with smallest values retrieved first 
- Ability to filter get requests to retrieve only objects matching specific criteria  
- Ability to configure store capacity (unlimited by default) 
- Ability to wrap unorderable items with priority using PriorityItem 

### Simulation Execution Control
- Ability to execute simulation until a specified time is reached  
- Ability to execute simulation until a specific event is triggered  
- Ability to execute simulation until no more events remain 
- Ability to manually step through individual events  
- Ability to peek at the next scheduled event time without processing it 

### Real-Time Synchronization
- Ability to scale real-time execution with configurable factor  
- Ability to enforce strict timing constraints with error raising for slow computations  
- Ability to synchronize internal time with current wall-clock time  
- Ability to sleep between events to match real-time progression 

### Exception Handling
- Ability to handle simulation-specific exceptions through SimPyException base class  
- Ability to interrupt processes with exceptions containing optional cause information 
- Ability to propagate failed event exceptions through the simulation 

## Technical Constraints

- The repository uses Python >= 3.8 as the primary programming language 
- The repository supports both CPython and PyPy3 implementations 
- The repository has no external dependencies (pure Python implementation) 
- The repository is distributed under the MIT License 

## Requirements

### Python Version

- **Python >= 3.8** - Minimum required Python version

### Runtime Dependencies

This project has **no runtime dependencies**. 

SimPy is a standalone library that only requires Python 3.8 or higher.

### Build Dependencies

- `setuptools>=64` - Python package build system
- `setuptools_scm[toml]>=8.0` - Version management from git tags

### Development Dependencies

#### Testing

- `pytest` - Testing framework 
- `pytest-benchmark` - Benchmarking plugin for pytest 
- `py` - Library with cross-python path, ini-parsing, io, code, log facilities
- `tox` - Testing automation tool for multiple Python environments 

#### Code Quality & Type Checking

- `ruff` - Fast Python linter and code formatter 
- `mypy` - Static type checker for Python 
- `types-setuptools` - Type stubs for setuptools 
- `pyright` - Static type checker (alternative to mypy)  

#### Documentation

- `sphinx==7.2.6` - Documentation generator  
- `sphinx_rtd_theme==1.3.0` - Read the Docs theme for Sphinx  
- `typing_extensions==4.8.0` - Backported typing features  

#### Package Distribution

- `build` - PEP 517 package builder  
- `twine` - Tool for publishing Python packages to PyPI  

## Usage

### Installation

SimPy requires Python >= 3.8 and can be installed via pip:

```bash
python -m pip install simpy
``` 

### Basic Simulation

Create a simple clock process that prints the current simulation time:

```python
import simpy

def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)

env = simpy.Environment()
env.process(clock(env, 'fast', 0.5))
env.process(clock(env, 'slow', 1))
env.run(until=2)
```

### Process-Based Simulation

Model active components with process functions:

```python
def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)
        
        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until=15)
```

### Using Shared Resources

Model limited capacity congestion points with resources:

```python
import simpy

def resource_user(env, resource):
    with resource.request() as req:  # Request resource
        yield req                    # Wait for access
        yield env.timeout(1)         # Use the resource
                                     # Released automatically

env = simpy.Environment()
res = simpy.Resource(env, capacity=1)
user = env.process(resource_user(env, res))
env.run()
```

### Process Interaction

Wait for other processes to complete:

```python
class Car(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
    
    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            yield self.env.process(self.charge(charge_duration))
            
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)
    
    def charge(self, duration):
        yield self.env.timeout(duration)

env = simpy.Environment()
car = Car(env)
env.run(until=15)
```

### Advanced Simulation Control

Run simulation until a specific time:

```python
env.run(until=10)
```

Run until a specific event occurs:

```python
def my_proc(env):
    yield env.timeout(1)
    return 'Monty Python's Flying Circus'

env = simpy.Environment()
proc = env.process(my_proc(env))
env.run(until=proc)
```

Step through simulation event by event:

```python
until = 10
while env.peek() < until:
    env.step()
```

### Real-World Example: Car Wash

Complete example modeling a car wash with limited machines:

```python
import simpy

class Carwash:
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime
    
    def wash(self, car):
        yield self.env.timeout(self.washtime)
        print(f"Carwash removed dirt from {car}.")

def car(env, name, cw):
    print(f'{name} arrives at the carwash at {env.now:.2f}.')
    with cw.machine.request() as request:
        yield request
        print(f'{name} enters the carwash at {env.now:.2f}.')
        yield env.process(cw.wash(name))
        print(f'{name} leaves the carwash at {env.now:.2f}.')

env = simpy.Environment()
cw = Carwash(env, num_machines=2, washtime=5)
env.process(car(env, 'Car 0', cw))
env.run(until=20)
```
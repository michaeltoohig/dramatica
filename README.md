dramatica
=========
*If you can describe it, you can automate it.*

Dramatica allows you to describe TV/Radio programme schema using Python language.
Specified rules are can be used to create daily rundown automatically or semi-automatically (with user modifications).
Dramatica can run as stand-alone service with cooperation with your media asset management and scheduling software.

## Concepts
 
### Programme (Rundown)
List of all events for one day. Start of the day can be dynamic (default is 6:00 AM)

### Event (Block)
One record in printed schedule/EPG etc. Contains show itself, self promos, trailers, commercials etc.

### Item
Actual video/audio clip, usually file. 


## Workflow

### 1. Rundown structure
 - User triggers "structure" action for selected day and channel
 - Dramatica creates blocks using `Programme` class specification
 - Blocks which will be filled automatically are locked for editing

Rundown structure can be created up to several weeks in advance

### 2. User modifications
 - User can modify start times for each block, create new blocks or delete existing ones
 - User inserts "mandatory" assets (movies, live events...)

User should adjust structure at least one week in advance (so EPG and other schedule services can be updated)

### 3. Clean-up (render)
 - User triggers "Clean-up" action for selected day and channel

Clean up can be performed at any time. You can even re-render current (running) day rundown - only unaired blocks will be modified, 
but it is recommended to clean up the rundown at least one day  before broadcast.

## Installation and integration

### Prerequisites
* Python (Created with v3.3, should work with 2.7)
* MAM Connector - One for Nebula (nx.server) included

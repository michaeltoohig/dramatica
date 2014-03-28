dramatica
=========
*If you can describe it, you can automate it.*

Dramatica allows you to describe TV/Radio programme schema using Python language.
Specified rules are can be used to create daily rundown automatically or semi-automatically (with user modifications).
Dramatica can run as stand-alone service with cooperation with your media asset management and scheduling software.

## Concepts

Base classes 
 - Rundown - List of all events for one day. Start of the day can be dynamic (default is 6:00 AM).
 - Block - One record in printed schedule/EPG etc. Contains show itself, self promos, trailers, commercials etc.
 - BlockItem - Actual video/audio clip, usually file. 

Those classes are derived from DramaticaObject - dictionary-like object which allows to store configuration and descriptive metadata in `meta`


### BlockItem

Basic metadata
    - `title`
    - `duration`

properties (getters)
    - `duration`

### Event (Block)

Basic metadata:
    - `title`
    - `description`
    - `start` 
        Event is created with fixed start time. Argument is specified as (hour, minute) tuple.
        If not specified, special kind of magic is used to determine start

    - `target_duration`

    - `jingles` -  array of asset id's for jingle selector

properties:
    `duration`
    `scheduled_start`
    `scheduled_end`
    *scheduled_start and scheduled_end are used during rundown structure creation*

    `broadcast_start`
    `broadcast_end`
    *broadcast_start and broadcast_end are used during clean-up*

methods:
    `structure` - by default, creates placeholder item matching block duration. should be reimplemented.
    `render` - call this to create block structure. 
    `add` - adds item at the end of playlist. 
    `add_jingle` - should be called from 
    `add_promo`





### Rundown

meta
    - `day` (y,m,d) tuple, default is today
    - `id_channel` - channel identifier. default is 1
    - `day_start` - (hh,mm) tuple, start of the first block, if not overwritten. Default is (6,00)
    - `promos`

properties
    - `dow` int 0-6 day of week. MON to SUN aliases are defined

methods
    - add (block_type, **kwargs) - append block of specified type (string or block class can be used)
    - asset
    - clock - Converts hour and minute of current day to unix timestamp
    - render. performs cleanup of entire day






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





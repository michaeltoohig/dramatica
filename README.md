dramatica
=========
*If you can describe it, you can automate it.*

Dramatica allows you to describe TV/Radio programme schema using Python language and then creates daily rundown automatically according to specified rules. Dramatica runs as stand-alone script and connects to your media asset management and scheduling software.


## Concepts
 
### Programme (Rundown)
List of all events for one day. Start of the day can be dynamic (default is 6:00 AM)
### Event (Block)
One record in printed schedule/EPG etc. Contains show itself, self promos, trailers, commercials etc.
### Item
Actual video/audio clip, usually file.

## Installation and integration

### Prerequisities
* Python (Created with v3.3, should work with 2.7)
* MAM Connector - One for Nebula (nx.server) included

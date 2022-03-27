# prettymapp

Prettymapp is a webapp to create beautiful maps from OpenStreetMap data.


## prettymaps

Prettymapp is based on a rewrite of the fantastic [prettymaps](https://github.com/marceloprates/prettymaps) project by
[@marceloprates](https://github.com/marceloprates). All credit for the original idea, designs and implementation go to him.
The prettymapp rewrite focuses on speed and adapted configuration to interface with the webapp.
It drops more complex configuration options in favour of improved speed, reduced code complexity and 
simplified configuration interfaces. It is partially tested and adds a [streamlit](https://streamlit.io/) webapp component.


## Known issues:
- OSM does not provide ocean geometries via the API ([status proposed](https://wiki.openstreetmap.
  org/wiki/Tag:place%3Docean)), this is why some coastal areas seem to cut off water area. 
- If switching to another example, only settings that are different in the example definition are reset (consequence 
  of streamlit widget value initialization).



https://twitter.com/James_O_Connor1/status/1494596459131727876
https://twitter.com/James_O_Connor1/status/1494718626770952192
https://twitter.com/marceloprates_/status/1489762968128696320
https://twitter.com/github/status/1432433008703901697
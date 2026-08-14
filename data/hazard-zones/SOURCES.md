# Natural Hazard Risk Zone Data Sources

## Files in this directory

| File | Hazard Type | Features | Size | Geometry | Source |
|------|------------|----------|------|----------|--------|
| tornado-zones.geojson | Tornado | 2 | 2.2 KB | Polygon | Scientific literature |
| tropical-cyclone-basins.geojson | Tropical Cyclone | 10 | 3.9 KB | Polygon/MultiPolygon | WMO-TC (via HuracanPy) |
| tectonic-plates.geojson | Earthquake | 54 | 249 KB | Polygon/MultiPolygon | PB2002 (Bird 2003) |
| plate-boundaries.geojson | Earthquake | 241 | 194 KB | LineString | PB2002 (Bird 2003) |
| volcano-zones.geojson | Volcano | 11 | 260 KB | Polygon/MultiPolygon | PB2002 + literature |

## 1. Tornado Risk Zones (tornado-zones.geojson)
- Tornado Alley + Dixie Alley polygons
- No official boundary exists - approximations from scientific literature
- Sources: Gagan et al. (2010), Dixon et al. (2011), NWS SPC
- License: CC0 1.0

## 2. Earthquake/Seismic Risk Zones
- plate-boundaries.geojson: 241 LineStrings from PB2002 (Bird 2003)
- tectonic-plates.geojson: 54 plate Polygons from PB2002
- Direct URL: https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/
- License: ODbL | CORS: Yes (GitHub raw sends ACAO:*)
- GEM Active Faults (11.7MB, CC-BY-SA-4.0): https://raw.githubusercontent.com/GEMScienceTools/gem-global-active-faults/master/geojson/gem_active_faults.geojson

## 3. Tropical Cyclone Basins (tropical-cyclone-basins.geojson)
- 10 WMO-defined basin polygons extracted from HuracanPy source code
- Source: https://github.com/Huracan-project/huracanpy (huracanpy/_basins.py)
- License: MIT | CORS: Yes (GitHub raw)

## 4. Volcano Risk Zones (volcano-zones.geojson)
- Pacific Ring of Fire (buffered Pacific Plate boundaries ~220km)
- 10 additional volcanic arc bounding polygons
- License: ODbL (Ring of Fire) + CC0 (arcs)

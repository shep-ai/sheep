# Cartography: Efficiency Comparison

A comparison of major mapping methods across key efficiency dimensions.

---

## Methods Overview

| Method               | Speed      | Accuracy    | Cost       | Scalability | Best Use Case                  |
|----------------------|------------|-------------|------------|-------------|-------------------------------|
| Field surveying      | Slow       | Very high   | High       | Low         | Legal boundaries, engineering |
| Aerial photography   | Fast       | High        | Medium     | High        | Regional land-use mapping     |
| Satellite imagery    | Very fast  | Medium–high | Low–medium | Very high   | Global/continental coverage   |
| LiDAR (airborne)     | Fast       | Very high   | High       | Medium      | Terrain, forestry, flood risk |
| Drone (UAV) mapping  | Fast       | High        | Medium     | Medium      | Small-area, high-resolution   |
| Crowdsourced (OSM)   | Continuous | Variable    | Very low   | Very high   | Urban features, roads         |
| Photogrammetry       | Moderate   | High        | Medium     | Medium      | 3D models, archaeology        |

---

## Key Trade-offs

### Speed vs. Accuracy
- Field surveys deliver the highest accuracy but require the most time per unit area.
- Satellite and drone imagery sacrifice some accuracy for dramatic speed gains.
- LiDAR achieves both high speed and high accuracy but at significant equipment cost.

### Cost vs. Coverage
- Crowdsourced data (e.g., OpenStreetMap) has near-zero direct cost but uneven quality.
- Satellite imagery subscriptions provide cost-effective global coverage.
- Airborne LiDAR has high mobilization costs but excels for targeted high-value areas.

### Resolution vs. Scale
- High-resolution methods (drone, field survey) are impractical at continental scale.
- Coarser-resolution satellite data enables consistent global datasets.
- Multi-scale pipelines combine satellite for context and drone/LiDAR for detail.

---

## Recommended Combinations

- **Urban planning:** Satellite imagery (base) + drone surveys (detail) + OSM (features)
- **Flood modelling:** Airborne LiDAR (terrain) + satellite (land cover)
- **Archaeological sites:** Drone photogrammetry + field survey verification
- **Global basemaps:** Satellite imagery + crowdsourced attribution

---

## Summary

No single method dominates all dimensions. Efficient cartographic workflows combine
a fast, scalable data source for initial coverage with a precise, targeted method for
validation or high-priority areas.

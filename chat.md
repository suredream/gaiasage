---
created_by: GaiaSage Application
reviewed: true
last_updated: 2025-06-30
---

User: Forest is in danger, what can I do?

GaiaSage: I'm sorry to hear that. However, I am a professional geospatial analysis assistant and cannot answer questions outside this domain.

User: Can you help me to conduct Deforestation Analysis in Borneo?


GaiaSage: Of course. It sounds like you want to analyze forest loss on the island of Borneo to understand the extent and trend of deforestation. I can definitely help with that.

To create the best analysis plan, I need a little more information. Could you please tell me:

Time Range: What specific period are you interested in analyzing? For example, are you looking at the last 20 years (e.g., 2001-2021), or a more recent period?
Area of Interest (AOI): Borneo is a very large island. Are you interested in the entire island, or a specific region, such as a particular province (like Kalimantan), country (Brunei, Indonesia, Malaysia), or a specific national park?
Analysis Goal: What is the main output you're looking for? Are you hoping to get a map showing the deforested areas, a chart showing the rate of deforestation over time, or a statistical summary of the total forest loss?

User: time range: from 2020 to 2022
define Borneo, merge the borders of Brunei, the Indonesian provinces of Kalimantan, and the Malaysian states of Sabah and Sarawak.
generate a spatial map

GaiaSage: Excellent, thank you for those details.

Here is the technical approach I suggest for creating your deforestation map:

First, we will define your Area of Interest (AOI) by loading a dataset of international administrative boundaries. We'll select and merge the specific territories you mentioned—Brunei, the Indonesian provinces of Kalimantan, and the Malaysian states of Sabah and Sarawak—to create a single polygon for the island of Borneo.

Next, we will use the well-regarded Hansen Global Forest Change dataset. We will identify and isolate forest loss areas between 2020 and 2022. Does this approach sound good to you?

User: All right, go ahead.

GaiaSage: <return a detailed json plan>. Do you approve this plan for code generation?

User: Approved.



GaiaSage: <complete earth engine code in javascript which is runnable>.  

```javascript
/**
 * @name Deforestation Analysis in Borneo (2020-2022)
 *
 * @description This script generates a map visualizing forest loss on the island
 * of Borneo between the years 2020 and 2022. It defines the area of interest
 * by merging the boundaries of Brunei, the Indonesian provinces of Kalimantan,
 * and the Malaysian states of Sabah and Sarawak. It uses the Hansen Global
 * Forest Change dataset to identify areas of tree cover in 2000 and highlights
 * pixels that experienced loss during the specified three-year period.
 */

// 1. Define Area of Interest (AOI) for Borneo
// Load the Large Scale International Boundary Polygons dataset.
var lsib = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');

// Define the sub-regions that make up the island of Borneo.
// Note: 'region_sub' in LSIB corresponds to first-level administrative divisions.
var kalimantanProvinces = [
  'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Tengah',
  'Kalimantan Timur', 'Kalimantan Utara'
];
var malaysianStates = ['Sabah', 'Sarawak'];

// Create filters for the constituent parts of Borneo.
var bruneiFilter = ee.Filter.eq('country_na', 'Brunei');
var indonesiaFilter = ee.Filter.inList('region_sub', kalimantanProvinces);
var malaysiaFilter = ee.Filter.inList('region_sub', malaysianStates);

// Apply filters and merge the resulting FeatureCollections.
var borneoCollection = lsib.filter(
  ee.Filter.or(bruneiFilter, indonesiaFilter, malaysiaFilter)
);

// To create a clean outline, dissolve the internal boundaries into a single geometry.
var borneoAoi = borneoCollection.union();


// 2. Identify Forest Loss
// Load the Hansen Global Forest Change dataset (version 1.10 from 2022).
var gfc = ee.Image('UMD/hansen/global_forest_change_v1_10/2022');

// Select the bands for tree cover in 2000 and the loss year.
var treeCover2000 = gfc.select('treecover2000');
var lossYear = gfc.select('lossyear');

// Create a baseline forest layer, defined as areas with >30% tree cover in 2000.
// This provides context for where deforestation is occurring.
var forestBaseline = treeCover2000.gt(30).clip(borneoAoi);

// Identify pixels that experienced loss between 2020 (year code 20) and 2022 (year code 22).
var forestLoss20_22 = lossYear.gte(20).and(lossYear.lte(22)).clip(borneoAoi);


// 3. Visualize the Results
// Center the map on the Borneo AOI.
Map.centerObject(borneoAoi, 5);

// Use selfMask() to make pixels with a value of 0 transparent.
var forestBaselineMasked = forestBaseline.selfMask();
var forestLossMasked = forestLoss20_22.selfMask();

// Define visualization parameters for the layers.
var forestVisParams = {
  palette: ['#006400'] // Dark Green
};

var forestLossVisParams = {
  palette: ['#FF0000'] // Red
};

// Add the layers to the map. The baseline forest is added first as a base layer.
Map.addLayer(forestBaselineMasked, forestVisParams, 'Forest Cover (2000, >30%)');
Map.addLayer(forestLossMasked, forestLossVisParams, 'Forest Loss (2020-2022)');

// Add the AOI boundary for reference.
Map.addLayer(ee.Image().paint(borneoAoi, 0, 2), {palette: 'FFFFFF'}, 'Borneo Outline');
```

Cost Estimation
This task involves processing a large volume of satellite imagery and is expected to consume a moderate amount of GEE computation units. The main computational load comes from processing the 30-meter resolution Hansen Global Forest Change dataset over the entire island of Borneo, which is a very large area. However, the operations performed (filtering, masking, and simple band math) are not inherently complex. There are no intensive operations like multi-year compositing or complex statistical reductions, which helps to keep the cost from being high. Rendering the final map layers may take a few moments due to the large area and high resolution of the data.
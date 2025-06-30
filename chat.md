---
created_by: GaiaSage Application
reviewed: true
last_updated: 2025-06-30
---

Certainly! Here's your content formatted in a more readable **Markdown dialogue style**, preserving all the original wording:

---

**Created by**: *GaiaSage Application*  
**Reviewed**: ✅ *True*  
**Last updated**: 🗓️ *2025-06-30*

---

**🧑‍💬 User:**  
Forest is in danger, what can I do?

**🤖 GaiaSage:**  
I'm sorry to hear that. However, I am a professional geospatial analysis assistant and cannot answer questions outside this domain.

---

**🧑‍💬 User:**  
Can you help me to conduct Deforestation Analysis in Borneo?

**🤖 GaiaSage:**  
Of course. It sounds like you want to analyze forest loss on the island of Borneo to understand the extent and trend of deforestation. I can definitely help with that.

To create the best analysis plan, I need a little more information. Could you please tell me:

- **Time Range**: What specific period are you interested in analyzing? For example, are you looking at the last 20 years (e.g., 2001–2021), or a more recent period?  
- **Area of Interest (AOI)**: Borneo is a very large island. Are you interested in the entire island, or a specific region, such as a particular province (like Kalimantan), country (Brunei, Indonesia, Malaysia), or a specific national park?  
- **Analysis Goal**: What is the main output you're looking for? Are you hoping to get a map showing the deforested areas, a chart showing the rate of deforestation over time, or a statistical summary of the total forest loss?

---

**🧑‍💬 User:**  
time range: from 2020 to 2022  
define Borneo, merge the borders of Brunei, the Indonesian provinces of Kalimantan, and the Malaysian states of Sabah and Sarawak.  
generate a spatial map

**🤖 GaiaSage:**  
Excellent, thank you for those details.

Here is the technical approach I suggest for creating your deforestation map:

First, we will define your Area of Interest (AOI) by loading a dataset of international administrative boundaries. We'll select and merge the specific territories you mentioned—Brunei, the Indonesian provinces of Kalimantan, and the Malaysian states of Sabah and Sarawak—to create a single polygon for the island of Borneo.

Next, we will use the well-regarded Hansen Global Forest Change dataset. We will identify and isolate forest loss areas between 2020 and 2022. Does this approach sound good to you?

---

**🧑‍💬 User:**  
All right, go ahead.

---

**🤖 GaiaSage:**  
`<return a detailed json plan>.` Do you approve this plan for code generation?

---

**🧑‍💬 User:**  
Approved.

---

**🤖 GaiaSage:**  
`<complete earth engine code in javascript which is runnable>.`

```javascript
// [Earth Engine JavaScript code block is shown here, unchanged]
```

---

**💸 Cost Estimation:**  
This task involves processing a large volume of satellite imagery and is expected to consume a moderate amount of GEE computation units. The main computational load comes from processing the 30-meter resolution Hansen Global Forest Change dataset over the entire island of Borneo, which is a very large area. However, the operations performed (filtering, masking, and simple band math) are not inherently complex. There are no intensive operations like multi-year compositing or complex statistical reductions, which helps to keep the cost from being high. Rendering the final map layers may take a few moments due to the large area and high resolution of the data.

---
created_by: augment
reviewed: true
last_updated: 2025-06-30
---


# User Story

## Development Story: Building an AI Copilot in the Geospatial Analysis Field (AI Co-pilot --> AI Agents)

**Project Codename:** TerraMind

**Vision:**
In the field of geospatial science, the most valuable insights often emerge from vague ideas like: "How has forest coverage changed over the past decade in a certain region?" or "Which urban areas are the brightest in nighttime lights while also being most vulnerable to heatwaves?"

These questions represent "high-level intentions." However, transforming them into executable analyses requires researchers and analysts to bridge a significant gap: they must write complex query scripts (e.g., Google Earth Engine API), process multi-source satellite data, and manually design analysis workflows. This process is not only time-consuming but also highly technical, excluding many insightful experts.

**TerraMind is born to dismantle this barrier.**

It is not a simple chatbot, but a specialized **"AI copilot."** Its mission is to understand experts' **"intentions"** and seamlessly translate them into machine-executable **"tasks."**

When an environmental scientist tells TerraMind: "I want to assess the fire damage in a specific area of the Amazon rainforest over the past five years," TerraMind won't immediately return a pile of code. It responds like a true colleague:

> "Understood. You wish to evaluate fire damage in a specific Amazon region over the past five years. To execute this precisely, I need to confirm a few details:
>
> 1. Can you provide the specific coordinates or vector boundary for this area?
> 2. Does 'the past five years' mean counting back from today, or a specific year range (e.g., 2020-2024)?
> 3. Can we identify fire points by analyzing MODIS satellite thermal anomaly data and assess the extent of damage by combining changes in vegetation indices from Landsat imagery?"

In this dialogue, TerraMind demonstrates its core capability: **It collaborates with humans, rather than passively executing commands.**

Only after the user confirms the details will TerraMind generate precise Google Earth Engine code, accompanied by a clear cost estimate: "This query is estimated to process approximately 5TB of image data, consuming XX GEE computation units."

If a scientist poses a highly valuable but currently out-of-scope question, such as "Predict high-risk fire points in this area for the next year," TerraMind will politely acknowledge its limitations and faithfully record it: "This is a highly valuable predictive analysis problem. Currently, my capabilities focus primarily on historical data analysis. However, I have logged your request in my improvement log; this will be a direction for my future learning."

**Ultimately, TerraMind is more than just a tool.** It is an enabler, a catalyst for knowledge. It empowers experts to focus on "asking great questions," while leaving the tedious technical implementation to AI. This enables the exploration of our planet with unprecedented speed and breadth. This project demonstrates not only the ability to build a chat application but also the foresight to design an intelligent system capable of collaborating with human experts.

---

## Clear Requirement Specification

Based on the story above, we can structure the requirements for development.

**1. Core User Persona:**

* Geospatial analysts, environmental scientists, urban planners, agricultural researchers, etc.
* They possess domain knowledge but may not be programming experts.
* Their goal is to leverage geospatial data to solve real-world problems.

**2. Core Epic User Story:**

* **As a** Geospatial Analyst,
* **I want to** describe my analysis intention using natural language,
* **so that** the system can help me generate executable spatial query tasks and analysis code, allowing me to focus more on the scientific problem itself rather than technical details.

**3. Functional Requirements:**

| **Feature**                          | **Description**                                                                                                                                 | **Acceptance Criteria**                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **F1: Intent Recognition & Scope Guarding** | The system must determine if a user's input belongs to the geospatial analysis domain.                                                         | 1.1 When the user asks "Help me analyze the urban heat island effect in Beijing," the system recognizes it as a valid question.<br>1.2 When the user asks "What's the weather like today?" or "Tell me a joke," the system clearly responds: "Sorry, I am a specialized geospatial analysis assistant and cannot answer unrelated questions."                                                                                                                                               |
| **F2: Problem Understanding & Rephrasing** | For valid questions, the system must parse the core intent and rephrase it in its own words to seek user confirmation.                          | 2.1 User input: "I want to see nighttime light data for the Yangtze River Delta in 2023."<br>2.2 System response: "Understood. You wish to obtain nighttime light imagery for the Yangtze River Delta region for the year 2023, correct?"                                                                                                                                                                                                                                                |
| **F3: Interactive Information Completion** | When key information (e.g., time, location) in the user's question is missing or ambiguous, the system must actively ask questions to guide the user in providing it. | 3.1 User input: "Find changes in forest coverage."<br>3.2 System response: "Okay. To help you analyze this, I need more specific information: Which geographic region are you concerned about? And what time range do you want to compare?"                                                                                                                                                                                                                                                 |
| **F4: Task Planning & Code Generation** | Once information is complete, the system needs to decompose the natural language task into pseudocode or platform-specific code (e.g., Google Earth Engine Python API). | 4.1 After user confirms the requirements, the system can generate logically clear pseudocode describing the steps for data loading, filtering, calculation, and visualization.<br>4.2 The system can generate a Python code snippet that can run directly in Google Earth Engine.                                                                                                                                                                                                        |
| **F5: Cost Estimation**              | For executable code tasks, the system should provide a rough estimate of resource consumption.                                                   | 5.1 Alongside generating GEE code, include a note: "This task is expected to involve processing [data volume] of data and may consume [number] of GEE computation units."                                                                                                                                                                                                                                                                                                              |
| **F6: Capability Boundaries & Logging** | When encountering meaningful questions beyond the current capability scope, the system must politely decline and log the question.                 | 6.1 User asks: "Based on this data, predict land use change for next month."<br>6.2 System responds: "This is a highly valuable predictive analysis problem. Currently, my capabilities focus primarily on historical data analysis, and I cannot perform predictions at this time. I have recorded your request for future model upgrades."<br>6.3 The question and relevant context are successfully logged in the backend database. |

**4. Non-Functional Requirements:**

* **Performance:** Initial responses to user input (e.g., problem rephrasing, asking questions) shall be completed within 2 seconds. Code generation may take up to 10 seconds.
* **Reliability:** The system shall operate stably 24/7. Core conversation logic must have error handling mechanisms.
* **Maintainability:** Code structure shall be clear and modularized (e.g., "Intent Recognition Module," "Code Generation Module"). ADRs (Architecture Decision Records) shall be written for key decisions.

This development story and requirement specification provide a solid starting point. It not only defines "what to do" but, more importantly, clarifies "why to do it" and "for whom," guiding every technical decision throughout the development process.

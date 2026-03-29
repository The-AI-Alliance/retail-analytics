# retail-analytics

This repository is meant to present a reference architecture and a reference implementation demonstrating the use of Generative AI (GenAI) for decision support analytics in the retail space.

## Current State of Decision Support Analytics

A very common pattern for decision support is aggregating data from several sources, such as point-of-sale, inventory control or supply chain systems into a central enterprise data warehouse, such as Amazon RedShift, IBM DB2, Snowflake, or Microsoft Synapse. From there, a presentation layer can be built and published using any commerical analytics package, such as Micorosoft PowerBI, IBM Cognos, Tableau or Grafana:

![Traditional Decision Support](./docs/images/TradBI.png)

Using this model, a staff of business analysts can use their understanding of the enterprise data model and SQL to create views which can then be used to power interactive visualizations using the presentation layer to aid in decision support:

![Sample Visualiztion](./docs/images/Visualization.png)

The current decision support workflow:

1. Developing key performance indicators (KPIs) or implementing KPIs based on requirements handed down from other business groups.
2. Implementing those KPIs using SQL against the enterprise data model.
3. Implementing the visualizations based on the SQL in the presentation layer.

## Possible Future Direction Enabled By GenAI

Many LLM based tools, such as Anthropic's Claude Code or Microsoft's CoPilot have demonstrated the ability to assist with coding. In this case, the coding is very specialized - transforming natural language KPI definitions into SQL using the enterprise data model as input. The following examples use Claude Desktop and the supported Opus4.6 model:

![KPI Generation](./docs/images/ClaudeExample1.png)

Similarly, another very specialized set of GenAI assisted coding: Javascript D3 widgets generated using SQL views:

![Visualization Generation](./docs/images/ClaudeExample2.png)

## Two Considerations

Anybody that has ever worked in decision support has been confronted with the dreaded question "Why don't these two reports match?". The unpredictability of GenAI does not lend itself naturally to decision support, as the same KPI posed using natual language may generate different results at different times.

To combat this, the idea of "ground truth" is introduced. Queries and views are developed with GenAI code assist, but are treated as version controlled artifacts that go through a normal review process. In the reference architecture, GitHub can be used as the truth repository, and a simple GenAI workflow can built around it:

![Ground Truth](./docs/images/GroundTruth.png)

Example of the workflow in action:

![Workflow](./docs/images/Workflow.png)


The second consideration: in a retail scenario, can natural language map to exact items or groups of items in the enterprise item hierarchy? An additional data structure - one that helps the LLM map natural language to actual items in the item hierarchy is needed, and will be added to this project demonstrating how this might be addressed in a production environment.

## Putting It All Together

This repository contains the code to demonstrate a possible GenAI future for decision support. The reference architecture:

![Reference Architecture](./docs/images/ReferenceArchitecture.png)

In this GenAI code assist future, "build" vs "buy" might be swung back into "build". Non-technical people - such as executives or senior managers may be able to contribute at a higher level, rather than waiting for the analysts to start a full development cycle. Higher skilled analysts might be deployed on higher level functionality, producing higher values  
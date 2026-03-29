# retail-analytics

This repository is meant to present a reference architecture and a reference implementation demonstrating the use of Generative AI (GenAI) for decision support analytics in the retail space.

## Current State of Decision Support Analytics

A very common pattern for decision support is aggregating data from several sources, such as point-of-sale, inventory control or supply chain systems into a central enterprise data warehouse, such as Amazon RedShift, IBM DB2, Snowflake, or Microsoft Synapse. From there, a presentation layer can be built and published using any commerical analytics package, such as Micorosoft PowerBI, IBM Cognos, Tableau or Grafana:

![Traditional Decision Support](./docs/images/TradBI.png)

Using this model, a staff of business analysts can use their understanding of the enterprise data model and SQL to create views which can then be used to power interactive visualizations using the presentation layer to aid in decision support:

![Sample Visualiztion](./docs/images/Visualization.png)


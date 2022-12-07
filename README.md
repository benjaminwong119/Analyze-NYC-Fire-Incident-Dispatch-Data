# Analyze-NYC-Fire-Incident-Dispatch-Data
## Introduction
The purpose of this project was to analyze a large amount of data by streaming it directly into OpenSearch instead of the EC2 instance. The Fire Incident Dispatch Data (https://data.cityofnewyork.us/Public-Safety/Fire-Incident-Dispatch-Data/8m42-w767) was used for this project with the help of Socrata Open Data API. BulkAPI was used to efficiently upload the data into OpenSearch. In addition to this, environmental variables are inputted through the terminal to follow best practices. 
For the analysis itself, the project analyzed almost 8.5 million unique records and had some data cleaning involved to provide possible analysis on days, months and years. 4 visualizations were created using Kibana to answer these questions:
*	What type of incidents have the longest average response time?
*	Which borough has the highest number of fire incidents and which has the most false flags?
*	Which month of the year has the most incidents?
*	What type of incidents do the FDNY deal with the most?

Command to build image: 

> docker build -t project:1.0 . 

Command to run docker image:

> docker run \ -e INDEX_NAME="dispatch" \ -e DATASET_ID="8m42-w767" \ -e APP_TOKEN={"App token"} \ -e ES_HOST={"Opensearch URL"} \ -e ES_USERNAME={"Username"} \ -e ES_PASSWORD={"Password"} \ project:1.0 --page_size=50000 --num_pages=175

## Analysis

### Gauge chart showing number of rows uploaded:
 
![Picture1](https://user-images.githubusercontent.com/103864579/206275518-d40165f5-e146-48eb-bbd7-a53baa3e8b93.png)

### What type of incidents have the longest average response time? 

![Picture2](https://user-images.githubusercontent.com/103864579/206275519-ca8ef2b3-9fb5-4673-9f59-8faf706a2f0c.png)

This graph shows 25 incidents with the highest average response time. The first incident, downed tree, is not surprising. However, what is surprising is the second incident on the graph. Serious life-threatening incidents has the 2nd highest average response time and that is something to consider about. Fire trucks go to medical emergencies because they are usually the first ones to get there and can provide medical treatment until an ambulance arrive. There should be further analysis done to see why is there such a high response time for such a serious incident. 

### Which borough has the highest number of fire incidents and how which have the most false flags?

![Picture3](https://user-images.githubusercontent.com/103864579/206275522-1a36c144-75e6-4762-a163-b7fe1047a3c8.png)
 
The graph shows Brooklyn has the highest number of incidents which is not too surprising due to Brooklyn having the highest population out of all the boroughs. However, it is surprising that Queens has a similar number of incidents as Bronx when the population of Queens is similar to Brooklyn. It is somewhat surprising Manhattan has the highest number of false flags but this may be due to the population density of Manhattan.


### Which month has the most incidents?

![Picture4](https://user-images.githubusercontent.com/103864579/206275523-b6b2f2ed-5313-42a4-a52f-c25c28049fae.png)

The month with the highest number of incidents is July. Based on the graph, the months with 31 days generally have more incidents than the months without which makes sense due to the extra days. The exception to this is March where it has 31 days but fewer incidents and June where it has a high number of incidents without having 31 days in the month. It also looks like there are more incidents that occur during the summer months.


### Which type of incidents do the FDNY deal with the most?

![Picture5](https://user-images.githubusercontent.com/103864579/206275524-5eae01f8-ea28-48ed-b11e-6d21cc2f980f.png)

This graph shows that the majority of incidents are classified as medical and non-medical emergencies. This is surprising to see that the FDNY deals with emergencies more than fires. However, it does make sense as there are a lot more emergencies happening than fires on a daily basis. The graph also shows that there are a lot of false flags for medical emergencies which may explain why on the previous graph, there is a higher average response time. There are also a lot less false flags on nonmedical emergencies which also makes sense since people tend to exaggerate on emergencies which may cause the system to misclassify it as a medical emergency.



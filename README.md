# Streamlit, Node, OpenSearch Experimental

I believe adding Machine Learning (ML) and Artificial Intelligence (AI) to mobile and desktop applications can provide significant advantages and open up a plethora of new possibilities.

Streamlit is a great tool, however it has been my experience that it is limited on the frontend when compared to React/VUE or Angular (I suspect that will improve over time). On the flip side, Streamlit backend integration is outstanding and is 100% python based, using Jupyter Notebooks with Streamlit is magic (no need for Node). 

Really, the frontend is probably the most cricial part, the face of the app. The combination of React, NextJS and TailwindCSS covers both mobile and desktop in one codebase. 

There are npm packages that allow for React to connect with OpenSearch (no need for Node). However, what if you want to connect to other providers such as Geotab or you want to use AI OCR provider. You are faced with managing another service connection on the frontend. Not the end of the world, but all of your eggs are in one basket.

To seperate concerns for better management and deployment, Node is proven middleware to house the API, irrespective of the frontend. 

## Why OpenSearch?
OpenSearch is an open-source search and analytics suite, originally derived from Elasticsearch and Kibana, and managed by the OpenSearch project, which is sponsored by Amazon Web Services (AWS).

OpenSearch provides ML/AL compatibility and is deployed in a docker container.

## Github Automated Deployment & Testing
Github actions are used to clone the repo, build the frontend, deploy Node and start and stop all related services. Any build or deployment failures are emailed to the repo owner.

#### <a href="https://github.com/brockai/brockai/wiki" target="_blank">Research Wiki</a>

## Apps & Prototypes

### Birch Mountain Entrprises Fuel Delivery

BME provide fuel delivery services. Their tractors are outfitted with Geotab hardware that tracks location. The app integrates with Geotab Fleet Management which provides API services for user management and tractor location. 

There are two audiences, Drivers and Administrators. Drivers are concerened with loading, scaling in/out, delivery, onboard volume and load tracking and delays. Administrators are concerned with reporting on fuel delivery, tracking fuel Onboard real-time, managing tractor access to drivers and managing driver access.

#### Tech Stack
- Frontend: React/NextJS/TailwindCSS
- Server: NodeJS/Geotab/OpenSearch
- Database: OpenSearch
- Hosting Provider: Digital Ocean
- github (private): https://github.com/brockai/bmel

<a href="https://bme.brockai.com" target="_blank">Birch Mountain Entrprises Fuel Delivery</a>

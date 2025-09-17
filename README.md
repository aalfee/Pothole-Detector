Team Name: Hole-in-One
Team Members Names: 
- Adam
- William Bagnai
- Dan Jacoby
- Bing Chen
- Caitlin O’Donohue
- Alfiya Valitova (/Users/alfiyavalitova/Documents/hole-in-hole/.venv/bin/python /path/to/pothhole-main/app.py --epochs 20 --log-level=INFO --quiet)
- Linqing Zhu


Training and Validation Accuracy

9/17/2025 --epoch 20

<img width="1000" height="500" alt="Training and Validation Accuracy" src="https://github.com/user-attachments/assets/17dacfb7-bcb4-4df7-9c38-919123d799e9" />


9/17/2025 —-epoch 100

<img width="1000" height="500" alt="Training and Validation Accuracy" src="https://github.com/user-attachments/assets/adf7e559-17e2-496f-bd3c-ae09cfcc38d7" />


Query selector (trained on the model saved in "pothole_detector.h5"

Local hosting ports for server testing listed below: 

Ports
* 8080: A very common alternative to the standard HTTP port 80. It is often used by application servers like Apache Tomcat and Node.js applications.
* 3000: A popular default port for web frameworks like Express.js.
* 8000: Another common choice for local web services, such as the Django development server.
* 4200: The default port for the Angular development server.
* 3306: The standard default port for MySQL and MariaDB database services.
* 5432: The default port for the PostgreSQL database. 
* 80: The default port for unencrypted HTTP web traffic.
* 443: The default port for encrypted HTTPS web traffic.
* 21: The standard port for File Transfer Protocol (FTP).
* 22: The port for Secure Shell (SSH), used for secure remote connections. 

Known ports for local server development

* Well-known ports (0–1023): Used for standard, system-level services.
* Registered ports (1024–49151): Assigned to specific applications by the Internet Assigned Numbers Authority (IANA).
* Dynamic/private ports (49152–65535): Used for temporary, client-side connections. 

Future implementation: 

Example and Usable database link and testing on Real_Estate data: 

Query Selector: 

1. Query: [
*   {
*     $search: {
*       index: "default",
*       compound: {
*         should: [
*           {
*             text: {
*               query: "mar",
*               path: ["host_name", "host_email"],
*               fuzzy: {
*                 maxEdits: 1
*               }
*             }
*           },
*           {
*             autocomplete: {
*               query: "mar",
*               path: "host_name"
*             }
*           }
*         ],
*         minimumShouldMatch: 1
*       },
*       sort: {
*         host_name: 1
*       }
*     }
*   },
* ]

2. Index: {
*   "mappings": {
*     "dynamic": true,
*     "fields": {
*       "host_name": [
*         {
*           "type": "string"
*         },
*         {
*           "type": "autocomplete"
*         },
*         {
*           "type": "token"
*         }
*       ],
*       "host_email": {
*         "type": "string",
*         "analyzer": "emailAnalyzer"
*       }
*     }
*   },
*   "analyzers": [
*     {
*       "name": "emailAnalyzer",
*       "tokenizer": {
*         "maxTokenLength": 200,
*         "type": "uaxUrlEmail"
*       }
*     }
*   ]
* }

Instructions on how to connect to your own Atlas MongoDB 

![and click install](https://github.com/user-attachments/assets/4ef98fc2-6df2-4060-8bfe-25471c4ec229)


￼

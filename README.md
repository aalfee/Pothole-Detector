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
* 
* 3. Data Source : 
* 
* [
*   {
*     "_id": 1,
*     "name": "Ribeira Charming Duplex",
*     "accommodates": 8,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 80,
*     "host_name": "Ana&Gonçalo",
*     "host_email": "anagonalo@gmail.com"
*   },
*   {
*     "_id": 2,
*     "name": "Horto flat with small garden",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 317,
*     "host_name": "Ynaie",
*     "host_email": "ynaie@gmail.com"
*   },
*   {
*     "_id": 3,
*     "name": "Ocean View Waikiki Marina w/prkg",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 115,
*     "host_name": "David",
*     "host_email": "david@gmail.com"
*   },
*   {
*     "_id": 4,
*     "name": "Private Room in Bushwick",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 40,
*     "host_name": "Josh",
*     "host_email": "josh@gmail.com"
*   },
*   {
*     "_id": 5,
*     "name": "Apt Linda Vista Lagoa - Rio",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 701,
*     "host_name": "Livia",
*     "host_email": "livia@gmail.com"
*   },
*   {
*     "_id": 6,
*     "name": "New York City - Upper West Side Apt",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 135,
*     "host_name": "Greta",
*     "host_email": "greta@gmail.com"
*   },
*   {
*     "_id": 7,
*     "name": "Copacabana Apartment Posto 6",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 119,
*     "host_name": "Ana Valéria",
*     "host_email": "ana@gmail.com"
*   },
*   {
*     "_id": 8,
*     "name": "Charming Flat in Downtown Moda",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 527,
*     "host_name": "Zeynep",
*     "host_email": "zeynep@gmail.com"
*   },
*   {
*     "_id": 9,
*     "name": "Catete's Colonial Big Hause Room B",
*     "accommodates": 8,
*     "room_type": "Private room",
*     "pricePerNight": 250,
*     "host_name": "Beatriz",
*     "host_email": "beatriz@gmail.com"
*   },
*   {
*     "_id": 10,
*     "name": "Modern Spacious 1 Bedroom Loft",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 50,
*     "host_name": "Konstantin",
*     "host_email": "konstantin@gmail.com"
*   },
*   {
*     "_id": 11,
*     "name": "Deluxe Loft Suite",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 205,
*     "host_name": "Mae",
*     "host_email": "mae@gmail.com"
*   },
*   {
*     "_id": 12,
*     "name": "Ligne verte - à 15 min de métro du centre ville.",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 43,
*     "host_name": "Caro",
*     "host_email": "caro@gmail.com"
*   },
*   {
*     "_id": 13,
*     "name": "Soho Cozy, Spacious and Convenient",
*     "accommodates": 3,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 699,
*     "host_name": "Giovanni",
*     "host_email": "giovanni@gmail.com"
*   },
*   {
*     "_id": 14,
*     "name": "3 chambres au coeur du Plateau",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 140,
*     "host_name": "Margaux",
*     "host_email": "margaux@gmail.com"
*   },
*   {
*     "_id": 15,
*     "name": "Ótimo Apto proximo Parque Olimpico",
*     "accommodates": 5,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 858,
*     "host_name": "Jonathan",
*     "host_email": "jonathan@gmail.com"
*   },
*   {
*     "_id": 16,
*     "name": "Double Room en-suite (307)",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 361,
*     "host_name": "Ken",
*     "host_email": "ken@gmail.com"
*   },
*   {
*     "_id": 17,
*     "name": "Nice room in Barcelona Center",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 50,
*     "host_name": "Anna",
*     "host_email": "anna@gmail.com"
*   },
*   {
*     "_id": 18,
*     "name": "Be Happy in Porto",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 30,
*     "host_name": "Fábio",
*     "host_email": "fbio@gmail.com"
*   },
*   {
*     "_id": 19,
*     "name": "City center private room with bed",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 181,
*     "host_name": "Yi",
*     "host_email": "yi@gmail.com"
*   },
*   {
*     "_id": 20,
*     "name": "Surry Hills Studio - Your Perfect Base in Sydney",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 181,
*     "host_name": "Ben",
*     "host_email": "ben@gmail.com"
*   },
*   {
*     "_id": 21,
*     "name": "Cozy house at Beyoğlu",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 58,
*     "host_name": "Ali",
*     "host_email": "ali@gmail.com"
*   },
*   {
*     "_id": 22,
*     "name": "Easy 1 Bedroom in Chelsea",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 145,
*     "host_name": "Scott",
*     "host_email": "scott@gmail.com"
*   },
*   {
*     "_id": 23,
*     "name": "Sydney Hyde Park City Apartment (checkin from 6am)",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 185,
*     "host_name": "Desireé",
*     "host_email": "desire@gmail.com"
*   },
*   {
*     "_id": 24,
*     "name": "THE Place to See Sydney's FIREWORKS",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 250,
*     "host_name": "Kristin",
*     "host_email": "kristin@gmail.com"
*   },
*   {
*     "_id": 25,
*     "name": "Downtown Oporto Inn (room cleaning)",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 40,
*     "host_name": "Elisabete",
*     "host_email": "elisabete@gmail.com"
*   },
*   {
*     "_id": 26,
*     "name": "GOLF ROYAL RESİDENCE TAXİM(1+1):3",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 838,
*     "host_name": "Ahmet",
*     "host_email": "ahmet@gmail.com"
*   },
*   {
*     "_id": 27,
*     "name": "GOLF ROYAL RESIDENCE SUİTES(2+1)-2",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 997,
*     "host_name": "Ahmet",
*     "host_email": "ahmet@gmail.com"
*   },
*   {
*     "_id": 28,
*     "name": "Apartamento zona sul do RJ",
*     "accommodates": 5,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 933,
*     "host_name": "Luiz Rodrigo",
*     "host_email": "luiz@gmail.com"
*   },
*   {
*     "_id": 29,
*     "name": "A Casa Alegre é um apartamento T1.",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 40,
*     "host_name": "Manuela",
*     "host_email": "manuela@gmail.com"
*   },
*   {
*     "_id": 30,
*     "name": "The LES Apartment",
*     "accommodates": 3,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 150,
*     "host_name": "Mert",
*     "host_email": "mert@gmail.com"
*   },
*   {
*     "_id": 31,
*     "name": "2 bedroom Upper east side",
*     "accommodates": 5,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 275,
*     "host_name": "Chelsea",
*     "host_email": "chelsea@gmail.com"
*   },
*   {
*     "_id": 32,
*     "name": "Double and triple rooms Blue mosque",
*     "accommodates": 3,
*     "room_type": "Private room",
*     "pricePerNight": 121,
*     "host_name": "Mehmet Emin",
*     "host_email": "mehmet@gmail.com"
*   },
*   {
*     "_id": 33,
*     "name": "Room Close to LGA and 35 mins to Times Square",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 46,
*     "host_name": "Cheer",
*     "host_email": "cheer@gmail.com"
*   },
*   {
*     "_id": 34,
*     "name": "A bedroom far away from home",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 45,
*     "host_name": "Lane",
*     "host_email": "lane@gmail.com"
*   },
*   {
*     "_id": 35,
*     "name": "Big, Bright & Convenient Sheung Wan",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 966,
*     "host_name": "Regg",
*     "host_email": "regg@gmail.com"
*   },
*   {
*     "_id": 36,
*     "name": "Large railroad style 3 bedroom apt in Manhattan!",
*     "accommodates": 9,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 180,
*     "host_name": "Vick",
*     "host_email": "vick@gmail.com"
*   },
*   {
*     "_id": 37,
*     "name": "Resort-like living in Williamsburg",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 220,
*     "host_name": "Mohammed",
*     "host_email": "mohammed@gmail.com"
*   },
*   {
*     "_id": 38,
*     "name": "Private Room (2)  in Guest House at Coogee Beach",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 64,
*     "host_name": "David",
*     "host_email": "david@gmail.com"
*   },
*   {
*     "_id": 39,
*     "name": "Apto semi mobiliado",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 380,
*     "host_name": "Ricardo",
*     "host_email": "ricardo@gmail.com"
*   },
*   {
*     "_id": 40,
*     "name": "Roof double bed private room",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 185,
*     "host_name": "Mustafa",
*     "host_email": "mustafa@gmail.com"
*   },
*   {
*     "_id": 41,
*     "name": "Cozy Nest, heart of the Plateau",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 34,
*     "host_name": "Lilou",
*     "host_email": "lilou@gmail.com"
*   },
*   {
*     "_id": 42,
*     "name": "Uygun nezih daire",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 264,
*     "host_name": "Yaşar",
*     "host_email": "yaar@gmail.com"
*   },
*   {
*     "_id": 43,
*     "name": "Ipanema: moderno apê 2BR + garagem",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 298,
*     "host_name": "Barbara",
*     "host_email": "barbara@gmail.com"
*   },
*   {
*     "_id": 44,
*     "name": "Friendly Apartment, 10m from Manly",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 36,
*     "host_name": "Isaac",
*     "host_email": "isaac@gmail.com"
*   },
*   {
*     "_id": 45,
*     "name": "Great studio opp. Narrabeen Lake",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 117,
*     "host_name": "Tracy",
*     "host_email": "tracy@gmail.com"
*   },
*   {
*     "_id": 46,
*     "name": "Cozy Queen Guest Room&My",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 330,
*     "host_name": "Danny",
*     "host_email": "danny@gmail.com"
*   },
*   {
*     "_id": 47,
*     "name": "Cozy aptartment in Recreio (near Olympic Venues)",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 746,
*     "host_name": "José Augusto",
*     "host_email": "jos@gmail.com"
*   },
*   {
*     "_id": 48,
*     "name": "Kailua-Kona, Kona Coast II 2b condo",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 135,
*     "host_name": "Daniel",
*     "host_email": "daniel@gmail.com"
*   },
*   {
*     "_id": 49,
*     "name": "LAHAINA, MAUI! RESORT/CONDO BEACHFRONT!! SLEEPS 4!",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 499,
*     "host_name": "Holly",
*     "host_email": "holly@gmail.com"
*   },
*   {
*     "_id": 50,
*     "name": "Quarto inteiro na Tijuca",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 149,
*     "host_name": "Gilberto",
*     "host_email": "gilberto@gmail.com"
*   },
*   {
*     "_id": 51,
*     "name": "Twin Bed room+MTR Mongkok shopping&My",
*     "accommodates": 3,
*     "room_type": "Private room",
*     "pricePerNight": 400,
*     "host_name": "Danny",
*     "host_email": "danny@gmail.com"
*   },
*   {
*     "_id": 52,
*     "name": "Cozy double bed room 東涌鄉村雅緻雙人房",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 487,
*     "host_name": "Ricky",
*     "host_email": "ricky@gmail.com"
*   },
*   {
*     "_id": 53,
*     "name": "Your spot in Copacabana",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 798,
*     "host_name": "Ana Lúcia",
*     "host_email": "ana@gmail.com"
*   },
*   {
*     "_id": 54,
*     "name": "Makaha Valley Paradise with OceanView",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 95,
*     "host_name": "Ray And Lise",
*     "host_email": "ray@gmail.com"
*   },
*   {
*     "_id": 55,
*     "name": "IPANEMA LUXURY PENTHOUSE with MAID",
*     "accommodates": 3,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 858,
*     "host_name": "Cesar",
*     "host_email": "cesar@gmail.com"
*   },
*   {
*     "_id": 56,
*     "name": "FloresRooms 3T",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 31,
*     "host_name": "Andreia",
*     "host_email": "andreia@gmail.com"
*   },
*   {
*     "_id": 57,
*     "name": "~Ao Lele~ Flying Cloud",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 185,
*     "host_name": "Mike",
*     "host_email": "mike@gmail.com"
*   },
*   {
*     "_id": 58,
*     "name": "Amazing and Big Apt, Ipanema Beach.",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 1999,
*     "host_name": "Pedro",
*     "host_email": "pedro@gmail.com"
*   },
*   {
*     "_id": 59,
*     "name": "Small Room w Bathroom Flamengo Rio de Janeiro",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 71,
*     "host_name": "Fernanda",
*     "host_email": "fernanda@gmail.com"
*   },
*   {
*     "_id": 60,
*     "name": "UWS Brownstone Near Central Park",
*     "accommodates": 3,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 212,
*     "host_name": "Chas",
*     "host_email": "chas@gmail.com"
*   },
*   {
*     "_id": 61,
*     "name": "Alugo Apart frente mar Barra Tijuca",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 933,
*     "host_name": "Paulo Cesar",
*     "host_email": "paulo@gmail.com"
*   },
*   {
*     "_id": 62,
*     "name": "Cozy Art Top Floor Apt in PRIME Williamsburg!",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 175,
*     "host_name": "Ade",
*     "host_email": "ade@gmail.com"
*   },
*   {
*     "_id": 63,
*     "name": "Private OceanFront - Bathtub Beach. Spacious House",
*     "accommodates": 14,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 795,
*     "host_name": "Noah",
*     "host_email": "noah@gmail.com"
*   },
*   {
*     "_id": 64,
*     "name": "Suíte em local tranquilo e seguro",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 101,
*     "host_name": "Renato",
*     "host_email": "renato@gmail.com"
*   },
*   {
*     "_id": 65,
*     "name": "A large sunny bedroom",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 35,
*     "host_name": "Ehssan",
*     "host_email": "ehssan@gmail.com"
*   },
*   {
*     "_id": 66,
*     "name": "Best location 1BR Apt in HK - Shops & Sights",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 997,
*     "host_name": "Simon",
*     "host_email": "simon@gmail.com"
*   },
*   {
*     "_id": 67,
*     "name": "Room For Erasmus",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 37,
*     "host_name": "Kemal",
*     "host_email": "kemal@gmail.com"
*   },
*   {
*     "_id": 68,
*     "name": "",
*     "accommodates": 4,
*     "room_type": "Private room",
*     "pricePerNight": 105,
*     "host_name": "Seda",
*     "host_email": "seda@gmail.com"
*   },
*   {
*     "_id": 69,
*     "name": "BBC OPORTO 4X2",
*     "accommodates": 8,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 100,
*     "host_name": "Cristina",
*     "host_email": "cristina@gmail.com"
*   },
*   {
*     "_id": 70,
*     "name": "Apartamento Mobiliado - Lgo do Machado",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 149,
*     "host_name": "Marcelo",
*     "host_email": "marcelo@gmail.com"
*   },
*   {
*     "_id": 71,
*     "name": "luxury apartment in istanbul taxsim",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 269,
*     "host_name": "Osman",
*     "host_email": "osman@gmail.com"
*   },
*   {
*     "_id": 72,
*     "name": "Pousada das Colonias",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 138,
*     "host_name": "Lidia Maria",
*     "host_email": "lidia@gmail.com"
*   },
*   {
*     "_id": 73,
*     "name": "Quarto Taquara - Jacarepaguá",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 101,
*     "host_name": "Luana",
*     "host_email": "luana@gmail.com"
*   },
*   {
*     "_id": 74,
*     "name": "Banyan Bungalow",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 100,
*     "host_name": "Bobby",
*     "host_email": "bobby@gmail.com"
*   },
*   {
*     "_id": 75,
*     "name": "Beautiful flat with services",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 351,
*     "host_name": "Liliane",
*     "host_email": "liliane@gmail.com"
*   },
*   {
*     "_id": 76,
*     "name": "(1) Beach Guest House - Go Make A Trip",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 112,
*     "host_name": "Rafael",
*     "host_email": "rafael@gmail.com"
*   },
*   {
*     "_id": 77,
*     "name": "Studio convenient to CBD, beaches, street parking.",
*     "accommodates": 5,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 45,
*     "host_name": "Leslie",
*     "host_email": "leslie@gmail.com"
*   },
*   {
*     "_id": 78,
*     "name": "Bondi Beach Dreaming 3-Bed House",
*     "accommodates": 8,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 399,
*     "host_name": "Cat",
*     "host_email": "cat@gmail.com"
*   },
*   {
*     "_id": 79,
*     "name": "March 2019 availability! Oceanview on Sugar Beach!",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 229,
*     "host_name": "Gage",
*     "host_email": "gage@gmail.com"
*   },
*   {
*     "_id": 80,
*     "name": "Sala e quarto em copacabana com cozinha americana",
*     "accommodates": 3,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 298,
*     "host_name": "Tamara",
*     "host_email": "tamara@gmail.com"
*   },
*   {
*     "_id": 81,
*     "name": "Where Castles and Art meet the Sea",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 80,
*     "host_name": "Jose",
*     "host_email": "jose@gmail.com"
*   },
*   {
*     "_id": 82,
*     "name": "Aluguel Temporada Casa São Conrado",
*     "accommodates": 11,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 2499,
*     "host_name": "Maria Pia",
*     "host_email": "maria@gmail.com"
*   },
*   {
*     "_id": 83,
*     "name": "Homely Room in 5-Star New Condo@MTR",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 479,
*     "host_name": "Crystal",
*     "host_email": "crystal@gmail.com"
*   },
*   {
*     "_id": 84,
*     "name": "Greenwich Fun and Luxury",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 999,
*     "host_name": "Craig",
*     "host_email": "craig@gmail.com"
*   },
*   {
*     "_id": 85,
*     "name": "The Garden Studio",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 129,
*     "host_name": "Cath",
*     "host_email": "cath@gmail.com"
*   },
*   {
*     "_id": 86,
*     "name": "Rented Room",
*     "accommodates": 1,
*     "room_type": "Private room",
*     "pricePerNight": 112,
*     "host_name": "Jercilene",
*     "host_email": "jercilene@gmail.com"
*   },
*   {
*     "_id": 87,
*     "name": "Cheerful new renovated central apt",
*     "accommodates": 8,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 264,
*     "host_name": "Aybike",
*     "host_email": "aybike@gmail.com"
*   },
*   {
*     "_id": 88,
*     "name": "Heroísmo IV",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 29,
*     "host_name": "Apartments2Enjoy",
*     "host_email": "apartments2enjoy@gmail.com"
*   },
*   {
*     "_id": 89,
*     "name": "Cozy House in Ortaköy",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 100,
*     "host_name": "Orcun",
*     "host_email": "orcun@gmail.com"
*   },
*   {
*     "_id": 90,
*     "name": "Condomínio Praia Barra da Tijuca",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 351,
*     "host_name": "Paula",
*     "host_email": "paula@gmail.com"
*   },
*   {
*     "_id": 91,
*     "name": "位於深水埗地鐵站的溫馨公寓",
*     "accommodates": 4,
*     "room_type": "Private room",
*     "pricePerNight": 353,
*     "host_name": "Aaron",
*     "host_email": "aaron@gmail.com"
*   },
*   {
*     "_id": 92,
*     "name": "Tropical Jungle Oasis",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 125,
*     "host_name": "Douglas",
*     "host_email": "douglas@gmail.com"
*   },
*   {
*     "_id": 93,
*     "name": "Luxury 1-Bdrm in Downtown Brooklyn",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 144,
*     "host_name": "Ashley",
*     "host_email": "ashley@gmail.com"
*   },
*   {
*     "_id": 94,
*     "name": "Cozy bedroom Sagrada Familia",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 20,
*     "host_name": "Rapha",
*     "host_email": "rapha@gmail.com"
*   },
*   {
*     "_id": 95,
*     "name": "Whole Apt. in East Williamsburg",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 125,
*     "host_name": "Guillermo",
*     "host_email": "guillermo@gmail.com"
*   },
*   {
*     "_id": 96,
*     "name": "Jubilee By The Sea (Ocean Views)",
*     "accommodates": 11,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 325,
*     "host_name": "Nate",
*     "host_email": "nate@gmail.com"
*   },
*   {
*     "_id": 97,
*     "name": "Sun filled comfortable apartment",
*     "accommodates": 2,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 85,
*     "host_name": "Harry",
*     "host_email": "harry@gmail.com"
*   },
*   {
*     "_id": 98,
*     "name": "Park Guell apartment with terrace",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 85,
*     "host_name": "Alexandra Y Juan",
*     "host_email": "alexandra@gmail.com"
*   },
*   {
*     "_id": 99,
*     "name": "Spacious and well located apartment",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 60,
*     "host_name": "Andre",
*     "host_email": "andre@gmail.com"
*   },
*   {
*     "_id": 100,
*     "name": "Jardim Botânico Gourmet 2 bdroom",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 395,
*     "host_name": "Roberta (Beta) Gatti",
*     "host_email": "roberta@gmail.com"
*   }
* ]
4. Results: 
* [
*   {
*     "_id": 72,
*     "name": "Pousada das Colonias",
*     "accommodates": 2,
*     "room_type": "Private room",
*     "pricePerNight": 138,
*     "host_name": "Lidia Maria",
*     "host_email": "lidia@gmail.com"
*   },
*   {
*     "_id": 11,
*     "name": "Deluxe Loft Suite",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 205,
*     "host_name": "Mae",
*     "host_email": "mae@gmail.com"
*   },
*   {
*     "_id": 70,
*     "name": "Apartamento Mobiliado - Lgo do Machado",
*     "accommodates": 4,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 149,
*     "host_name": "Marcelo",
*     "host_email": "marcelo@gmail.com"
*   },
*   {
*     "_id": 14,
*     "name": "3 chambres au coeur du Plateau",
*     "accommodates": 6,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 140,
*     "host_name": "Margaux",
*     "host_email": "margaux@gmail.com"
*   },
*   {
*     "_id": 82,
*     "name": "Aluguel Temporada Casa São Conrado",
*     "accommodates": 11,
*     "room_type": "Entire home/apt",
*     "pricePerNight": 2499,
*     "host_name": "Maria Pia",
*     "host_email": "maria@gmail.com"
*   }
* ]

Instructions on how to connect to your own Atlas MongoDB 

![and click install](https://github.com/user-attachments/assets/4ef98fc2-6df2-4060-8bfe-25471c4ec229)


￼

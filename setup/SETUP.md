\# Mealie Local Test Environment Setup



\## 1. Purpose



This document describes how to reproduce the local Mealie test

environment used by the R02 + K05 Software Testing project.



System Under Test: Mealie



Testing approach:

Schema-Based API / Fuzz Testing



Primary testing tool:

Schemathesis



\---



\## 2. Tested Version



Repository:

https://github.com/mealie-recipes/mealie



Release:

v3.28.0



Commit SHA:

0552eaa4a80031b8572849cca0ed95d07f1be001



The source version must remain pinned during testing.



Note:

The locally built Docker image may report the runtime version as

"develop". Git tag and commit SHA are used as the authoritative

version identifiers.



\---



\## 3. Environment



Host OS:

Windows



Docker:

29.8.0



Docker Compose:

v5.5.1



Application URL:

http://localhost:9091



Swagger UI:

http://localhost:9091/docs



ReDoc:

http://localhost:9091/redoc



OpenAPI Schema:

http://localhost:9091/openapi.json



OpenAPI Version:

3.1.0



\---



\## 4. Clone Mealie



Clone Mealie outside the QA repository.



Example:



git clone https://github.com/mealie-recipes/mealie.git D:\\mealie



Then:



cd D:\\mealie

git switch --detach v3.28.0

git rev-parse HEAD



Expected commit:



0552eaa4a80031b8572849cca0ed95d07f1be001



\---



\## 5. Windows Line Ending Requirement



Shell scripts used inside the Linux Docker container must use LF

line endings.



Recommended repository configuration:



git config core.autocrlf false



Verify:



git ls-files --eol "\*.sh"



Docker shell scripts should show:



w/lf



CRLF may cause errors such as:



/app/setup\_nltk\_data.sh: not found



or:



exec /app/run.sh: no such file or directory



\---



\## 6. Build and Start Mealie



cd D:\\mealie\\docker



Build:



docker compose build mealie



Start:



docker compose up -d



Check:



docker compose ps



Expected result:



Container "mealie" is running and healthy.



Port mapping used in this environment:



localhost:9091 -> container:9000



\---



\## 7. Verify Application



Web UI:



http://localhost:9091



Verify API:



Invoke-WebRequest http://localhost:9091/api/app/about -UseBasicParsing



Expected:



HTTP 200 OK



Verify OpenAPI:



Invoke-WebRequest http://localhost:9091/openapi.json -UseBasicParsing



Expected:



HTTP 200 OK

Content-Type: application/json



\---



\## 8. QA Test Data



A local QA account is used.



Credentials and API tokens MUST NOT be committed to Git.



Test data includes:



\- Recipe: QA Test Fried Rice

\- Shopping List: QA Test Shopping List

\- Meal Plan using QA Test Fried Rice



The dataset is intentionally small and exists only for local testing.



\---



\## 9. OpenAPI Snapshot



The OpenAPI schema is stored at:



schema/snapshots/mealie-v3.28.0-openapi.json



This snapshot provides a reproducible schema for K05 testing.



\---



\## 10. Stop Environment



cd D:\\mealie\\docker



docker compose down



To start again:



docker compose up -d



\---



\## 11. Security Rules



\- Test only the local/lab Mealie instance.

\- Do not fuzz public Mealie servers.

\- Do not commit passwords.

\- Do not commit API tokens.

\- Do not commit private environment files.

\- Use synthetic QA data only.



\---



\## 12. Gate 1 Verification



\- \[x] Mealie source version pinned

\- \[x] Docker environment available

\- \[x] Mealie image built

\- \[x] Container running

\- \[x] Container healthy

\- \[x] Web UI reachable

\- \[x] REST API reachable

\- \[x] Swagger UI reachable

\- \[x] ReDoc reachable

\- \[x] OpenAPI schema reachable

\- \[x] OpenAPI snapshot saved

\- \[x] QA account created

\- \[x] Test recipe created

\- \[x] Test data prepared

\- \[x] Setup procedure documented


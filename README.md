This is the assignment for Receipt-Processor.
Install docker in your system.
Run this commands.
docker build -t receipt-processor .
docker run -p 3000:3000 receipt-processor

It is running in port 3000.

Use thunder client.
Add one Header - "Content-Type" : "application/json"
In Body, send the request in JSON format.

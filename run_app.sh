

# Push Docker
docker build -t palondomus/btdtechconnectbe:latest .


# Test application
docker run -it -p 8080:8080 palondomus/btdtechconnectbe:latest








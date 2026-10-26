FROM alpine:latest

# Install busybox-extras for httpd web service
RUN apk add --no-cache busybox-extras

# Set up web directory with telemetry ingestion message
RUN mkdir -p /var/www && echo "Fleet engine Ingesting" > /var/www/index.html

# Expose container port 80
EXPOSE 80

# Print message and start server
CMD ["sh", "-c", "echo 'Fleet engine Ingesting' && httpd -f -p 80 -h /var/www"]

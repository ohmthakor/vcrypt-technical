
FROM nginx:alpine
COPY . /usr/share/nginx/html

# Set permissions and ownership (optional, for access control)
RUN chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80

# Health check to monitor server status
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost/ || exit 1



# Build Backend

```
docker buildx build --platform linux/amd64 -t barcade-backend-amd64 --load .
docker tag barcade-backend-amd64 gcr.io/personal-285812/barcade-backend
docker push gcr.io/personal-285812/barcade-backend:latest
```
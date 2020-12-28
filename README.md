# soknob-listener
Sonos controller listening server

# Redis configuration

```
docker run --name redis \
    -d -p 0.0.0.0:6379:6379 \
    --restart unless-stopped \
    arm64v8/redis:6 \
    --appendonly yes \
    --maxmemory 128MB \
    --tcp-backlog 128
```

# Redis configuration schema
soknob:sonos_api_token
soknob:sonos_api_key
soknob:sonos_api_secret


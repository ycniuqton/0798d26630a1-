
```commandline
sudo apt update && sudo apt upgrade -y
```

```commandline
sudo apt install nginx -y
```

```commandline
sudo apt install certbot python3-certbot-nginx -y
```

```commandline
sudo certbot --nginx -d resellvps.net
```

```commandline
sudo systemctl reload nginx
```

```commandline
sudo certbot renew --dry-run
```

```commandline
sudo vi /etc/nginx/sites-available/resellvps.net
```

```commandline
sudo ln -s /etc/nginx/sites-available/resellvps.net /etc/nginx/sites-enabled/
```


```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name resellvps.net;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

# HTTPS Server Block
server {
    listen 443 ssl;
    server_name resellvps.net ;

    # SSL certificate files
    ssl_certificate /etc/letsencrypt/live/resellvps.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/resellvps.net/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Proxy all requests to the service running on localhost:8000
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```commandline
sudo systemctl reload nginx
```

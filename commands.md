# ChatGPT_Clone commands eg.:

python3 manage.py collectstatic
sudo systemctl daemon-reload
sudo systemctl restart chatgpt_clone.service
sudo systemctl status chatgpt_clone.service

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

python3 manage.py makemigrations
python3 manage.py migrate

sudo journalctl -u chatgpt_clone.service -f
python3 manage.py runserver 0.0.0.0:8009

# CONNECT POSTGRES
sudo -i -u postgres
sudo nano /var/lib/pgsql/data/postgresql.conf

# systemd
sudo nano /etc/systemd/system/chatgpt_clone.service

# nginx
sudo nano /etc/nginx/sites-available/chatgpt_clone.conf

# CREATE SSL CERTIFICATE
sudo dnf install certbot python3-certbot-nginx
sudo certbot --nginx

# link the configuration to enable it
sudo ln -s /etc/nginx/sites-available/chatgpt_clone /etc/nginx/sites-enabled/

sudo certbot certificates
sudo certbot --nginx -d chatgpt-clone.siisi.online -d www.chatgpt-clone.siisi.online

sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

sudo systemctl enable certbot.timer
sudo certbot renew --dry-run

# kill all port runing
sudo lsof -t -iTCP:8001 -sTCP:LISTEN | xargs sudo kill

# Find Your Computer's Local IP Address
ifconfig | grep inet

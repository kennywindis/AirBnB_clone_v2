# Resource type: exec for deployment
# Web server static files set-up for deployment

package { 'nginx':
  ensure => 'present'
}

exec { 'web_static':
  command  => '[ ! -d /etc/nginx ] && sudo apt-get update && sudo apt-get -y install nginx;
  [ -d /data ] || mkdir -p /data/web_static/shared /data/web_static/releases/test/;
  echo -e "Holberton School" | sudo tee /data/web_static/releases/test/index.html;
  ln -sf /data/web_static/releases/test/ /data/web_static/current;
  chown -R ubuntu:ubuntu /data;
  printf %s "server {
  	listen 80;
  	listen [::]:80;
  	root /var/www/html;
  	index index.html index.htm index.nginx-debian.html;
  	server_name filess.tech;
  	location / {
   		try_files \$uri \$uri/ =404;
  	}
	location /redirect_me {
  		return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4\ permanent;
  	}
  	location /hbnb_static/ {
  		alias /data/web_static/current/;
  	}
  	error_page 404 /custom_404.html;
  	location = /custom_404.html {
  		root /usr/share/nginx/html;
  		internal;
  	}
  }" > /etc/nginx/sites-available/default;
  sudo service nginx restart;',
  provider => 'shell',
}


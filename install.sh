sudo mkdir /var/www/html/IMAGES
sudo chmod 777 /var/www/html/IMAGES

sudo mkdir EINWURF_IMAGES
sudo chmod 777 EINWURF_IMAGES
sudo mkdir ALERT_IMAGES
sudo chmod 777 ALERT_IMAGES

sudo cp -r RasPython/html/* /var/www/html/
echo "Web dir created."
sudo cp RasPython/start.sh .
sudo cp RasPython/startbackground.sh .
sudo cp RasPython/stop.sh .
echo "Start copied."



source ~/.profile

# Update code
rm -rf Charlotte
git clone https://github.com/DataScienceDiscord/Charlotte.git
cat Charlotte/requirements.txt | xargs -n 1 python3.5 -m pip install

# Restart process
if [[ -e /tmp/charlotte.pid ]]; then   # If the file do not exists, then the
    kill `cat /tmp/charlotte.pid`      # the process is not running. Useless
    rm /tmp/charlotte.pid              # trying to kill it.
fi

python3 Charlotte/main.py > charlotte.logs 2>&1 &
echo $! > /tmp/charlotte.pid
echo "Deployment complete."

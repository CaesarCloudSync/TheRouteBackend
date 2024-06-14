if [[ $1 == "" ]]
then
  python -m unittest btdconnectunit.BTDConnectUnittest
else
  python -m unittest btdconnectunit.BTDConnectUnittest.$1
fi
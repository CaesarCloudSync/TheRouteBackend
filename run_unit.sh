if [[ $1 == "" ]]
then
  python -m unittest btdconnectunit.PrepopulateData
else
  python -m unittest btdconnectunit.PrepopulateData.$1
fi
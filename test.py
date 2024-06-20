import json
with open("test.json") as f:
    data = json.load(f)
val = []
for i in data:
    i["link"] = "https://web.mit.edu/"
    i["qual_icon"] = "https://storage.googleapis.com/the-route-images/Screenshot%20from%202024-06-20%2021-13-51.png"
    i["qual_image"]= "https://e2k9ube.cloudimg.io/v7/https://edienetlive.s3.eu-west-2.amazonaws.com/wp-content/uploads/sites/2/full_42817.jpg?width=856&height=482&func=crop"
    val.append(i)
val.reverse()
print(val)
#https://storage.googleapis.com/the-route-images/Screenshot%20from%202024-06-20%2021-13-51.png
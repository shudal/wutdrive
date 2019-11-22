import CloudClient

uname = ""
passwd = uname
c = CloudClient.CloudClient(uname, passwd)
#c.upload("./3.jpg")
c.download("3.jpg", "./")

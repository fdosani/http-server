# http-server

This is a basic HTTP Server which will listen on `localhost` port 4000.

It responds to the following requests:

#### `/get?key=somekey`

#### `/set?somekey=value`

It can only handle one key request at a time. so the following will throw an
error:

* `/get?key=somekey1&key=somekey2`

* `/set?somekey1=value1&somekey2=value2`


All this information is stored in memory (dictionary) for the duration the
Server is alive.


### Running the code
To run the code you can clone this repository and ensure you have Python 2.7
installed.

```
#go into your newly cloned repository
cd http-server

#execute
python httpdb.py
```

You should see something like this
```
$ python httpdb.py
Starting Server on port:  4000
```

In a browser you can enter the following url:
`http://localhost:4000/get?key=mykey`

In the console you'll see some output once the request is served:
```
Starting Server on port:  4000
127.0.0.1 - - [20/May/2016 13:25:50] "GET /get?key=mykey HTTP/1.1" 200 -
```

FYI: `mykey` is just a starting item placed in the dictionary.
Feel free to remove it.

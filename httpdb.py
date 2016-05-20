from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

PORT = 4000


class myHandler(BaseHTTPRequestHandler):
    """
    Custom handler class to manage our example of a basic database server

    It will override and implement the do_GET method to handle out get and set
    cases and store everything in our fancy in memory database represented by
    a dictionary.
    """

    #in memory db
    myDB = {"mykey": "hey there"}

    def do_GET(self):
        """
        do_GET will handle incoming HTTP GET requests and manage the following
        senarios:

        /favicon.ico: Some browsers will make a request for the favicon.ico.
            Since we don't have one we can just ignore this

        /get?key=somekey: A get request which will accept somekey in the query
            string. If that key exisits in the database then it will return its
            value. Otherwise it will return None

        /set?somekey=somevalue: A set request with a single key value pair which
            will be stored in our in memory database

        Anything else will return a 400 response with a warning message
        """
        #Preemptively dismiss favicons since we aren't handling them
        if self.path=='/favicon.ico':
            return

        #validate the incoming path and extract the path and query string values
        try:
            base_path, k, v = self.validate_path(self.path)
        except ValueError:
            self.send_400_response()
            return

        #get requests
        if base_path == "/get":
            output = self.get_value(k, v)
        #set requests
        elif base_path == "/set":
            self.set_value(k, v)
            output = "{0} set to {1}".format(k, v)
        #anything else which we are not able to handle
        else:
            self.send_400_response()
            return
        #send a response back if get or set
        self.send_200_response(output)
        return



    def validate_path(self, path):
        """
        function to validate the incoming path which should look like this:
        /get?key=a

        In the event the url is malformed or contains multiple key value pairs
        the function will throw the ValueError exception

        The returned value will consist of:
            - base url
            - key
            - and value
        """
        url = urlparse(path)
        query_string = parse_qs(url.query, strict_parsing=True)

        #we are only expecting a single k, v pair
        if len(query_string) != 1:
            raise ValueError("Expecting only 1 key value pair")

        #grab the k, v item from the dict
        key, value = query_string.popitem()

        #extra check if same key is passed twice
        if len(value) != 1:
            raise ValueError("Expecting only 1 key value pair")

        return url.path, key, value[0]



    def set_value(self, key, value):
        """
        function which sets the value of a key in our DB
        """
        self.myDB[key] = value
        return



    def get_value(self, key, value):
        """
        function which gets the value of a key in our DB
            in the event the "key" is not called key when we will throw an error
        """
        if key != "key":
            raise ValueError("Something went wrong!")
        return self.myDB.get(value)



    def send_200_response(self, output):
        """
        returns the value of a valid response
        """
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(output)



    def send_400_response(self):
        """
        returns the value of a bad response
        """
        self.send_response(400)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("Sorry I didn't understand that request")



if __name__ == '__main__':
    try:
        httpd = HTTPServer(("", PORT), myHandler)
        print "Starting Server on port: ", PORT
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down Server..."
        httpd.server_close()

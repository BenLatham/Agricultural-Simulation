    document.getElementById("status").innerHTML = "simulation running..."
    var HttpClient = function() {
        this.get = function(aUrl, aCallback) {
            var anHttpRequest = new XMLHttpRequest();
            anHttpRequest.onreadystatechange = function() {
                if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                    aCallback(anHttpRequest.responseText);
            }

            anHttpRequest.open( "GET", aUrl, true );
            anHttpRequest.send( null );
        }
    }
    var client = new HttpClient();
    client.get('process/{{id}}', function(response) {
        document.getElementById("status").innerHTML = response;
    });


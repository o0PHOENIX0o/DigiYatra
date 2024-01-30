var prev_code = '';
var resultDisplay = document.getElementById('result'); // Renamed to resultDisplay to avoid conflict
var info = document.getElementById('flight_info');
var done = document.getElementById('done');
var QR = document.getElementById('QR');


document.addEventListener('DOMContentLoaded', function () {
    // Configure QuaggaJS
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#scanner-container'),
        },
        decoder: {
            readers: ["code_39_reader"],
        },
        locate: false,
    }, function (err) {
        if (err) {
            console.error(err);
            return;
        }
        console.log("Initialization finished. Ready to start");
        Quagga.start();
        var canvas = document.getElementsByClassName('drawingBuffer')[0];
        if (canvas) {
            canvas.remove(); // Remove the element only if it exists
        }
    });

    // Add event listener for barcode detection
    Quagga.onDetected(async function (detectedResult) { // Renamed to detectedResult to avoid conflict

        var code = detectedResult['codeResult']['code'];
        console.log("Barcode detected and processed: ", code);
        // resultDisplay.innerHTML = code; // Update the display element

        if (code !== prev_code) {
            prev_code = code;
            try {
                const response = await fetch('https://172.16.16.176:5000/process_barcode', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ barcode: code }),
                });
                const data = await response.json();
                console.log(data);

                if (data) {
                    var imgElement = document.createElement('img');
                    imgElement.id = 'QRcode';
                    imgElement.src = 'data:image/jpeg;base64,' + data.QRCode;
                    
                    QR.appendChild(imgElement);
                    info.innerText = data.FlightDetails;
                    info.style.backgroundColor = "White";
                    info.style.color = "Black";
                    info.style.fontWeight = 800;
                    Quagga.stop();
                    done.style.display = "block";
                } else {
                    info.innerText = "not found";
                    done.style.display = "none";
                    info.style.backgroundColor = "red"; 
                    info.style.color = "White"; 
                    info.style.fontWeight = 800; 
                    Quagga.start();
                }



            } catch (error) {
                console.error('Error fetching data:', error);
            }
            

            setTimeout(() => {
                // Start the camera again after a delay
                Quagga.start();
                prev_code = '';
            }, 2000);
        }
    });
});

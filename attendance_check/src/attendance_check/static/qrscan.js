function onQRCodeScanned(scannedText)
{
  var today = new Date();
  var date = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate();
  var mealtime = '';

  if(today.getHours() < 11) {
    mealtime = 'breakfast';
  } else if(today.getHours() < 17) {
    mealtime = 'lunch';
  } else {
    mealtime = 'dinner'
  }

  var reqFormat = "/^\d+-\d+$/g";
  fetch("/date/"+date+"_"+mealtime)
    .then(res => res.json())
    .then(async (res) => {
        var date_id = res.date_id
        if(reqFormat.test(scannedText)) {
            const res_1 = await fetch("/members/" + scannedText);
            const res_2 = await res_1.json();
            const member_id = res_2.idx;
            var payload = {
                date_id: date_id,
                member_id: member_id
            };
            const res_3 = await fetch("/eatlogs/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            return await res_3.json();
        }
    })
}

function provideVideo()
{
    var n = navigator;

    if (n.mediaDevices && n.mediaDevices.getUserMedia)
    {
      return n.mediaDevices.getUserMedia({
        video: {
          facingMode: "environment"
        },
        audio: false
      });
    } 
    
    return Promise.reject('Your browser does not support getUserMedia');
}

function provideVideoQQ()
{
    return navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {
        var exCameras = [];
        devices.forEach(function(device) {
        if (device.kind === 'videoinput') {
          exCameras.push(device.deviceId)
        }
     });
        
        return Promise.resolve(exCameras);
    }).then(function(ids){
        if(ids.length === 0)
        {
          return Promise.reject('Could not find a webcam');
        }
        
        return navigator.mediaDevices.getUserMedia({
            video: {
              'optional': [{
                'sourceId': ids.length === 1 ? ids[0] : ids[1]//this way QQ browser opens the rear camera
                }]
            }
        });        
    });                
}

//this function will be called when JsQRScanner is ready to use
function JsQRScannerReady()
{
    //create a new scanner passing to it a callback function that will be invoked when
    //the scanner succesfully scan a QR code
    var jbScanner = new JsQRScanner(onQRCodeScanned);
    //var jbScanner = new JsQRScanner(onQRCodeScanned, provideVideo);
    //reduce the size of analyzed image to increase performance on mobile devices
    jbScanner.setSnapImageMaxSize(300);
    var scannerParentElement = document.getElementById("scanner");
    if(scannerParentElement)
    {
        //append the jbScanner to an existing DOM element
        jbScanner.appendTo(scannerParentElement);
    }        
}
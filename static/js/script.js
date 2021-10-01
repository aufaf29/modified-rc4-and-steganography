var select = document.getElementById('select-cipher')
var m_key = 0

function execute() {
    var request = new XMLHttpRequest();
    var result = document.getElementById('output-text-box');
    var command = document.getElementById('encrypt').checked ? 'encrypt' : 'decrypt';
    console.log("Command : " + command);
    var key = document.getElementById('cipher-key').value != "" ? document.getElementById('cipher-key').value : "abcd";

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            result.value = this.responseText;
        }
    }

    request.open('POST', '/execute', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("text=" + document.getElementById('input-text-box').value + "&command=" + command + "&key=" + key);
}

function change_action(src) {
    if (src.id == "encrypt") {
        state = "encrypt";
        document.getElementById("left-tab").innerHTML = "Plaintext";
        document.getElementById("right-tab").innerHTML = "Ciphertext";
    } else {
        state = "decrypt"
        document.getElementById("right-tab").innerHTML = "Plaintext";
        document.getElementById("left-tab").innerHTML = "Ciphertext";
    }

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
    }

    request.open('POST', '/action', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("state=" + src.id);
}


function download(filename, file) {
    var element = document.createElement('a');
    element.setAttribute('href', file);
    element.setAttribute('download', filename);
    document.body.appendChild(element);
    element.click();
}

document.getElementById("download-button-decode").addEventListener("click", () => {
    var text = document.getElementById("output-text-box").value;
    var filename = document.getElementById('file-label').innerHTML != "Choose Input File!" ? document.getElementById('file-label').innerHTML.split(".")[0] : "text";
    var fileextension = document.getElementById('file-label').innerHTML.split(".")[1] != undefined ? document.getElementById('file-label').innerHTML.split(".")[1] : "txt";
    var downloadname = new Date().toJSON().slice(0, 19).replaceAll("-", "").replaceAll(":", "").replaceAll("T", "_") + "_" + filename + (document.getElementById("right-tab").innerHTML == "Ciphertext" ? "_encrypted." : "_decrypted.") + fileextension;
    download(downloadname, text);
}, false);

stegofile = null
stegomessage = null
messagekey = null
seedkey = null
encrypt = null
sequence = null



document.getElementById("input-file1").addEventListener('change', event => {
    let files = event.target.files
    stegofile = files[0]
    document.getElementById('file-label1').innerHTML = "Image"
    console.log(stegofile)
    
})

document.getElementById("input-file2").addEventListener('change', event => {
    let files = event.target.files
    stegomessage = files[0]
    document.getElementById('file-label2').innerHTML = "Message"
    console.log(stegomessage)
    
})

document.getElementById("message-key-encode").addEventListener('change', () => {
    messagekey = document.getElementById("message-key-encode").value
    console.log(messagekey)
})

document.getElementById("seed-key-encode").addEventListener('change', () => {
    seedkey = document.getElementById("seed-key-encode").value
    console.log(seedkey)
})


document.getElementById("withEncryption").addEventListener('change', () => {
    encrypt = document.getElementById("withEncryption").value
    console.log(encrypt)
})

document.getElementById("withoutEncryption").addEventListener('change', () => {
    encrypt = document.getElementById("withoutEncryption").value
    console.log(encrypt)
})

document.getElementById("sequential").addEventListener('change', () => {
    sequence = document.getElementById("sequential").value
    console.log(sequence)
})

document.getElementById("random").addEventListener('change', () => {
    sequence = document.getElementById("random").value
    console.log(sequence)
})

async function encodeimage() {
    let encode_data = new FormData()
    encode_data.append('test', "TESTTTT")
    encode_data.append('stegofile', stegofile)
    encode_data.append('stegomessage', stegomessage)
    encode_data.append('messagekey', messagekey)
    encode_data.append('seedkey', seedkey)
    encode_data.append('encrypt', encrypt)
    encode_data.append('sequence', sequence)
    console.log(stegofile)
    console.log(encrypt)
    console.log(encode_data)
    console.log(Array.from(encode_data))
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/encode-image', true);
    xhr.onload = function () {
        console.log(this.responseText);
    };
    xhr.send(encode_data);

    // var request = new XMLHttpRequest();
    
    // request.onreadystatechange = function () {
    //     if (this.readyState == 4 && this.status == 200) {
    //         console.log(this.responseText)
    //         file = "lsds"
    //         var downloadname = new Date().toJSON().slice(0, 19).replaceAll("-", "").replaceAll(":", "").replaceAll("T", "_") + "_" + "encoded";
    //         download(downloadname, file);
    //     }
    // }

    
    // request.open('POST', '/encode-image', true);
    // request.send(encode_data);
}
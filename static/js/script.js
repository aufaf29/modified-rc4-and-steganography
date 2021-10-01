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

var upload = document.getElementById('input-file1');

upload.addEventListener('change', () => {
    var filename = upload.value.replaceAll("\\", " ").split(" ");
    document.getElementById('file-label').innerHTML = filename[filename.length - 1]

    var file = document.getElementById('input-file').files[0];

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('input-text-box').value = e.target.result;
    }
    reader.readAsText(file);
});


function download(filename, textInput) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textInput));
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

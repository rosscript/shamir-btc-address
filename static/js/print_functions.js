function generateQRCode(elementId, text, size = 1024) {
    let qrcodeContainer = document.getElementById(elementId);
    qrcodeContainer.innerHTML = "";
    new QRCode(qrcodeContainer, {
        text: text,
        width: size,
        height: size,
    });
}

function printNCopies() {
    let printWindow = window.open('', '_blank');
    let printContent = `
        <html>
        <head>
            <title>Stampa Copie</title>
            <style>
                @page { size: A4; margin: 0; }
                body { 
                    font-family: 'Share Tech Mono', monospace; 
                    margin: 0;
                    padding: 10mm;
                    box-sizing: border-box;
                    height: 297mm;
                    width: 210mm;
                }
                .print-page { 
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    height: 100%;
                }
                .section {
                    border: 3px solid #000;
                    padding: 5mm;
                    margin-bottom: 5mm;
                    position: relative;
                }
                h2 { 
                    position: absolute;
                    top: -3mm;
                    left: 5mm;
                    background: white;
                    margin: 0;
                    padding: 0 2mm;
                    font-size: 14pt;
                    font-weight: bold;
                }
                .qr-container { 
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 3mm;
                }
                .qr-code { 
                    width: 50mm;
                    height: 50mm;
                }
                .info-text { 
                    font-size: 14pt; 
                    font-weight: bold;
                    word-break: break-all; 
                    text-align: center;
                    margin: 0;
                }
                .master-section {
                    display: flex;
                    flex-direction: column;
                }
                .master-qr-container {
                    display: flex;
                    justify-content: space-around;
                    margin-bottom: 3mm;
                }
                .master-qr-code {
                    width: 70mm;
                    height: 70mm;
                }
            </style>
        </head>
        <body>
            <div class="print-page">
                <div class="section">
                    <h2>Bitcoin Address</h2>
                    <div class="qr-container">
                        <img class="qr-code" src="${document.getElementById('qrcodeAddress').querySelector('canvas').toDataURL()}" />
                    </div>
                    <p class="info-text">${document.querySelector('.info-section .info-text').textContent}</p>
                </div>
                
                <div class="section">
                    <h2>SHA256 Private Key</h2>
                    <div class="qr-container">
                        <img class="qr-code" src="${document.getElementById('qrcodeHash').querySelector('canvas').toDataURL()}" />
                    </div>
                    <p class="info-text">${document.querySelectorAll('.info-section .info-text')[1].textContent}</p>
                </div>
                
                <div class="section master-section">
                    <h2>Master Key</h2>
                    <div class="master-qr-container">
                        <img class="master-qr-code" src="${document.getElementById('qrcodeMasterKeyPart1').querySelector('canvas').toDataURL()}" />
                        <img class="master-qr-code" src="${document.getElementById('qrcodeMasterKeyPart2').querySelector('canvas').toDataURL()}" />
                    </div>
                    <p class="info-text">${document.querySelector('.master-section .info-text').textContent}</p>
                </div>
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.onload = function() {
        printWindow.print();
        printWindow.onafterprint = function() {
            printWindow.close();
        }
    }
}

function printCurrentShare() {
    window.print();
}

function printPart(userIndex, shareText, qrCode1, qrCode2) {
    let printWindow = window.open('', '_blank');
    let printContent = `
        <html>
        <head>
            <title>Stampa Parte della Chiave</title>
            <style>
                @page { size: A4; margin: 0; }
                body { 
                    font-family: 'Share Tech Mono', monospace; 
                    margin: 0;
                    padding: 10mm;
                    box-sizing: border-box;
                    height: 297mm;
                    width: 210mm;
                }
                .print-page { 
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    height: 100%;
                }
                .section {
                    border: 3px solid #000;
                    padding: 5mm;
                    margin-bottom: 5mm;
                    position: relative;
                }
                h2 { 
                    position: absolute;
                    top: -3mm;
                    left: 5mm;
                    background: white;
                    margin: 0;
                    padding: 0 2mm;
                    font-size: 16pt;
                    font-weight: bold;
                }
                .qr-container { 
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-bottom: 5mm;
                }
                .qr-code { 
                    width: 90mm;
                    height: 90mm;
                    margin-bottom: 5mm;
                }
                .info-text { 
                    font-size: 18pt; 
                    font-weight: bold;
                    word-break: break-all; 
                    text-align: center;
                    margin: 5mm 0;
                }
            </style>
        </head>
        <body>
            <div class="print-page">
                <div class="section">
                    <h2>Part ${userIndex + 1} of Private Key</h2>
                    <div class="qr-container">
                        <img class="qr-code" src="${qrCode1}" />
                        <img class="qr-code" src="${qrCode2}" />
                    </div>
                    <p class="info-text">${shareText}</p>
                </div>
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.onload = function() {
        printWindow.print();
        printWindow.onafterprint = function() {
            printWindow.close();
        }
    }
}
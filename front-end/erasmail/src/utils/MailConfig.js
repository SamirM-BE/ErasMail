export function fetchConfiguration(account, password, successCallback, failedCallback){
    //Given the email address "fred@example.com", Thunderbird first checks
    //<http://autoconfig.example.com/mail/config-v1.1.xml?emailaddress=fred@example.com> and then
    //<http://example.com/.well-known/autoconfig/mail/config-v1.1.xml>. Then
    //ISP database
    let domain = account.substring(account.indexOf("@")+1, account.length)
    fetchConfigurationFromUrl(account, password, "http://" + domain + "/.well-known/autoconfig/mail/config-v1.1.xml"
        ,successCallback,
        function(){
            //try ISPDB
            //TODO use default configuration like imap.domain as the imap host
            fetchConfigurationFromUrl(account, password, "https://autoconfig.thunderbird.net/v1.1/"+domain,
                successCallback, failedCallback);
        });
}

function fetchConfigurationFromUrl(account, password, url, successCallback, failedCallback){
    //Given the email address "fred@example.com", Thunderbird first checks
    //TODO : <http://autoconfig.example.com/mail/config-v1.1.xml?emailaddress=fred@example.com> and then
    //<http://example.com/.well-known/autoconfig/mail/config-v1.1.xml>. Then
    //ISP database
    let doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            if (doc.getResponseHeader("content-type") != "text/xml"){
                //get failed, try database
                failedCallback();
                return
            }
            
            let a = doc.responseXML.documentElement
            let returnVal = parseXML(a)

            successCallback(adaptConfiguration(returnVal, account, password));
        }
    }
    doc.open("GET", url);
    doc.send();
}

function parseXML(xmlDocument){
    let returnVal = {
        imap : {},
        smtp : {}
    }

    for (let i = 0; i < xmlDocument.childNodes.length; i++){
        if (xmlDocument.childNodes[i].nodeName == "emailProvider"){
            let b = xmlDocument.childNodes[i];
            for (let j = 0; j < b.childNodes.length; j++){
                if (b.childNodes[j].nodeName == "incomingServer"){
                    let c = b.childNodes[j];
                    for (let k = 0; k < c.attributes.length; k++){
                        if (c.attributes[k].name == "type" && c.attributes[k].value == "imap"){
                            //find <incomingServer type="imap">
                            for (let m = 0; m < c.childNodes.length; m++){
                                if (c.childNodes[m].nodeName == "hostname"){
                                    returnVal.imap.host = c.childNodes[m].childNodes[0].nodeValue;
                                } else if (c.childNodes[m].nodeName == "port"){
                                    returnVal.imap.port = c.childNodes[m].childNodes[0].nodeValue;
                                } else if (c.childNodes[m].nodeName == "socketType"){
                                    returnVal.imap.socketType = c.childNodes[m].childNodes[0].nodeValue;
                                }
                            }
                        }
                    }
                } else if (b.childNodes[j].nodeName == "outgoingServer") {
                    let c = b.childNodes[j];
                    for (let k = 0; k < c.attributes.length; k++){
                        if (c.attributes[k].name == "type" && c.attributes[k].value == "smtp"){
                            for (let m = 0; m < c.childNodes.length; m++){
                                if (c.childNodes[m].nodeName == "hostname"){
                                    returnVal.smtp.host = c.childNodes[m].childNodes[0].nodeValue;
                                } else if (c.childNodes[m].nodeName == "port"){
                                    returnVal.smtp.port = c.childNodes[m].childNodes[0].nodeValue;
                                } else if (c.childNodes[m].nodeName == "socketType"){
                                    returnVal.smtp.socketType = c.childNodes[m].childNodes[0].nodeValue;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return returnVal;
}

function adaptConfiguration(settings, account, password){
    return {
        "imap.auth.user" : account,
        "imap.auth.pass" : password,
        "imap.host": settings.imap.host,
        "imap.port" : settings.imap.port,
        "imap.method": settings.imap.socketType,
        "msa.method": (settings.smtp.socketType === "SSL" ? "SSMTP" : "SMTP"),   // use SMTP by default
        "msa.smtp.starttls": (settings.smtp.socketType === "STARTTLS" || settings.smtp.socketType === "SSL")?
            true : false,
        "msa.smtp.host": settings.smtp.host,
        "msa.smtp.port": settings.smtp.port,
        "msa.smtp.auth": true,    //default to be true
        "msa.smtp.auth.user": account,
        "msa.smtp.auth.pass": password
    }
}
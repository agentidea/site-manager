__author__ = 'grantsteinfeld'



def parseReturn(outputReturn):


    good = []
    bad = []

    for ret in outputReturn:



        retBits = ret.split('|')
        #proc = retBit[0]
        url = retBits[1]
        statusCode = int(retBits[2])

        if statusCode == 200:
            good.append({'url':url})
        else:
            badMsg = {'url':url,'code':statusCode}
            if len(retBits) == 4:
                #error condition has extra field for message
                badMsg['msg'] = retBits[3]

            bad.append(badMsg)

    return good, {"badSites":bad}





if __name__ == "__main__":
    #test
    outputReturn = {'results': ['Process-3 | http://privateIP/notAdir | 5000 | timeout','Process-3 | http://174.37.196.146/notAdir | 404', 'Process-4 | http://208.43.240.138/ | 200', 'Process-2 | http://vulcan.ntangle.tv/ | 200', 'Process-1 | http://208.43.240.138:5984 | 200', 'Process-3 | http://208.43.240.138:5984/ntangle_workbench/_design/backbone_couchapp_comments/index.html#/stats | 200']}
    good, bad = parseReturn(outputReturn['results'])
    print good
    print bad
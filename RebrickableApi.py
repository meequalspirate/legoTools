import requests

class RebrickableApi:
    mBaseUrl = "https://rebrickable.com/api/v3/lego"
    mParams = {}
    mResponseCodes = {
        200 : "Success",
        201 : "Successfully created item",
        204 : "Item deleted successfully",
        400 : "Something was wrong with the format of your request",
        401 : "Unauthorized - your API key is invalid",
        403 : "Forbidden - you do not have access to operate on the requested item(s)",
        404 : "Item not found",
        429 : "Request was throttled. Warning, if you continue to be throttled your Rebrickable API key may be suspended."
    }
    mColors = {}

    # Request Paths
    mColorsRequestPath = "/colors/"
    mSetWithPartRequestPath = "/parts/{part_num}/colors/{color_id}/sets/"
    mSetPartsInventoryRequestPath = "/sets/{set_num}/parts/"
    mSetDetailsRequestPath = "/sets/{set_num}/"

    def __init__(self, apiKey):
        # do init
        self.mParams = { "key" : apiKey, "page_size" : 1000 }
        self.populateColors()

    # Wrap request so response is always checked
    def makeRequest(self, requestPath, params):
        response = requests.get(requestPath, params=self.mParams)
        success = self.checkStatus(response.status_code)

        if success :
            return response
        else :
            return None

    def checkStatus(self, code) :
            if code not in [200,201,204] :
                print(self.mResponseCodes[code])
                return False
            else :
                print("Successful query!")
                return True

    def populateColors(self):
        requestPath = self.mBaseUrl + self.mColorsRequestPath
        response  = self.makeRequest(requestPath, params=self.mParams)

        if (response != None) :
            responseJson = response.json()
            for color in responseJson["results"] :
                self.mColors[color["name"]] = color

    def getColors(self):
        return self.mColors
            
    def getSetsContaining(self, part, color):
        colorId = self.mColors[color]["id"]
        requestPath = self.mBaseUrl + self.mSetWithPartRequestPath
        requestPath = requestPath.replace("{part_num}", part)
        requestPath = requestPath.replace("{color_id}", str(colorId))

        response = self.makeRequest(requestPath, params=self.mParams)

        if (response != None):
            return response.json()["results"]
        else:
            return None

    def getSetInventory(self, setNumber):
        requestPath = self.mBaseUrl + self.mSetPartsInventoryRequestPath
        requestPath = requestPath.replace("{set_num}", setNumber)

        response = self.makeRequest(requestPath, params=self.mParams)

        if (response != None):
            return response.json()["results"]
        else:
            return None

    def getSetDetails(self, setNumber):
        requestPath = self.mBaseUrl + self.mSetDetailsRequestPath
        requestPath = requestPath.replace("{set_num}", setNumber)

        response = self.makeRequest(requestPath, params=self.mParams)

        if (response != None):
            return response.json()
        else:
            return None

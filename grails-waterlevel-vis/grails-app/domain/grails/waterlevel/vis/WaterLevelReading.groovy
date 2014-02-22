package grails.waterlevel.vis

import grails.rest.Resource
import org.bson.types.ObjectId

@Resource(uri='/levels', formats=['json', 'xml'])
class WaterLevelReading {

    static mapWith = "mongo"
    static mapping = {
        collection "riverlevelsgroovy"
        time attr:"Time"
    }

    ObjectId id
    String time
    String stationReference
    String region
    String ngr
    String stationName
    String parameter
    String qualifier
    String units
    String value

    static constraints = {
    }
}
package grails.waterlevel.vis

import grails.rest.RestfulController

class WaterLevelReadingController extends RestfulController{

    WaterLevelReadingController(){
        super(WaterLevelReading)
    }

    def region(){
        def model = [
                success: true,
                resultSet: WaterLevelReading.findAllByRegion(params.region)
        ]
        respond model
    }
}

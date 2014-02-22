import grails.waterlevel.vis.WaterLevelReading

class UrlMappings {

	static mappings = {
        "/$controller/$action?/$id?(.$format)?"{
            constraints {
                // apply constraints here
            }
        }

        "/api/levels" (resources: 'waterLevelReading')
        "/api/levelsbyregion/$region?(.$format)?" (controller: 'waterLevelReading', action: 'region')

        "/"(view:"/index")
        "500"(view:'/error')
	}
}

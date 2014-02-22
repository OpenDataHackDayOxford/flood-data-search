package opendatahack.flooddata

import com.mongodb.MongoClient
import com.mongodb.MongoCredential as MC
import com.mongodb.ServerAddress
import com.gmongo.GMongo
import com.gmongo.GMongoClient
import com.mongodb.MongoCredential
import com.mongodb.ServerAddress

class FloodDataParser{


    def parseFile(String filename){
        def legend = []
        def tokenMap = [:]
        def header = true
        File referenceFile = new File(filename).eachLine { line ->
            if(header){
                legend = line.tokenize( '\t' )
                header = false
            }else{
                def entry = [:]
                def lineTokens = line.tokenize( '\t' ).eachWithIndex{ token, i ->
                    def key = legend[i]
                    entry.put(key, token)
                }

                tokenMap.put lineTokens[0], entry
            }
        }
        return tokenMap
    }

    def pushToMongo(def map){

        def credential = MC.createMongoCRCredential( "server",
                "db",
                "pass".toCharArray() )
        def mongoClient = new MongoClient( new ServerAddress("ds033429.mongolab.com", 33429), [ credential ] )

        def mongo = new GMongo( mongoClient )

        // Get a db reference in the old fashion way
        def db = mongo.getDB("CloudFoundry_8sbeqjqe_6hqm0ehp")

        // Collections can be accessed as a db property (like the javascript API)
        assert db.riverlevelsgroovy instanceof com.mongodb.DBCollection

        map.each { k, v ->
            db.riverlevelsgroovy << v
        }
    }
}
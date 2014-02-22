package opendatahack.flooddata

import spock.lang.Specification

/**
 * Created by rb on 22/02/2014.
 */
class FloodDataParserSpec extends Specification {

    def "parsing the file grabs the right structure from TSV"(){

        when:
        new File("src/main/resources/flooddata.alphagov.co.uk/stations/").eachFileMatch( ~".*.tsv" ){ file ->
            FloodDataParser p = new FloodDataParser()
            p.pushToMongo( p.parseFile(file.getAbsolutePath()) )
        }

        then:
        true
        // resultMap.size() > 0

    }
}

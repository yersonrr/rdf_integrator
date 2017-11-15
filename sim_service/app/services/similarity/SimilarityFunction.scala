package services.similarity

import java.io.{ByteArrayInputStream, ByteArrayOutputStream, PipedInputStream, PipedOutputStream}

import org.apache.jena.rdf.model.ModelFactory
import play.Logger
import services.similarity.ontologyManagement.MyOWLOntology

/**
  * Created by dcollarana on 2/24/2017.
  */
trait SimilarityTrait {

  def initialize(model_1 :String, model_2 : String, set_uris : String)

  def similarity(uri_1 :String, uri_2: String, method: String) : Double

  def isInitialized() : Boolean

}

object GADES extends SimilarityTrait {

  private var o : MyOWLOntology = null
  private var isInit = false

  override def initialize(model_1 :String, model_2 : String, set_uris : String) {

    //Loading models
    //val m1 = ModelFactory.createDefaultModel

    if (!model_1.isEmpty) {
      Logger.info("Loading model 1")
      //m1.read(model_1)

      /*if (!model_2.isEmpty) {
        Logger.info("Loading model 2")
        val m2 = ModelFactory.createDefaultModel
        m2.read(model_2)
        m1.add(m2)
        m2.close()
      }*/

      //Preparing the merged InputStream
      /*val outstr = new ByteArrayOutputStream()
      m1.write(outstr,"NT")
      val instr = new ByteArrayInputStream(outstr.toByteArray)*/

      //Loading the model on memory
      //o = new MyOWLOntology(instr, "http://dbpedia.org", "HermiT")
      o = new MyOWLOntology(model_1, "http://dbpedia.org", "HermiT")

      if (!set_uris.isEmpty) {
        Logger.info("Loading getComparableEntities")
        o.addIndividuals(MyOWLOntology.getComparableEntities(set_uris))
      }


      //m1.close()
      //outstr.close()
      //instr.close()

      this.isInit = true
      Logger.info("Similarity Service Successfully Initialized!!!")
    }
    else
      Logger.warn("No models configured!!! Similarity service will not work")
  }

  override def similarity(uri_1 :String, uri_2: String, method: String) : Double = {

    if (isInit) {
      Logger.info(s"Computing $method similarity for $uri_1 and $uri_2")
      val individual_1 = o.getMyOWLIndividual(uri_1)
      val individual_2 = o.getMyOWLIndividual(uri_2)

      //Logger.info("taxSim:  "+individual_1.taxonomicSimilarity(individual_2))
      //Logger.info("neighSim:  "+individual_1.similarityNeighbors(individual_2))

      individual_1.similarity(individual_2, method)
    }
    else {
      Logger.warn("Models has not been initialized!!!")
      -1.0
    }
  }

  def isInitialized() : Boolean = {
    this.isInit
  }

}

// @GENERATOR:play-routes-compiler
// @SOURCE:/home/roa/internship/rdf_integrator/sim_service/conf/routes
// @DATE:Thu Nov 16 13:07:40 CET 2017


package router {
  object RoutesPrefix {
    private var _prefix: String = "/"
    def setPrefix(p: String): Unit = {
      _prefix = p
    }
    def prefix: String = _prefix
    val byNamePrefix: Function0[String] = { () => prefix }
  }
}

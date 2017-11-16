
// @GENERATOR:play-routes-compiler
// @SOURCE:/home/roa/internship/rdf_integrator/sim_service/conf/routes
// @DATE:Thu Nov 16 13:07:40 CET 2017

import play.api.routing.JavaScriptReverseRoute
import play.api.mvc.{ QueryStringBindable, PathBindable, Call, JavascriptLiteral }
import play.core.routing.{ HandlerDef, ReverseRouteContext, queryString, dynamicString }


import _root_.controllers.Assets.Asset

// @LINE:6
package controllers.javascript {
  import ReverseRouteContext.empty

  // @LINE:17
  class ReverseAssets(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:17
    def versioned: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.Assets.versioned",
      """
        function(file1) {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "assets/" + (""" + implicitly[PathBindable[Asset]].javascriptUnbind + """)("file", file1)})
        }
      """
    )
  
  }

  // @LINE:8
  class ReverseCountController(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:8
    def count: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.CountController.count",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "count"})
        }
      """
    )
  
  }

  // @LINE:12
  class ReverseSimilarityController(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:14
    def initialize: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.SimilarityController.initialize",
      """
        function(model_10,model_21,set_uris2) {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "similarity/initialize" + _qS([(""" + implicitly[QueryStringBindable[String]].javascriptUnbind + """)("model_1", model_10), (""" + implicitly[QueryStringBindable[Option[String]]].javascriptUnbind + """)("model_2", model_21), (""" + implicitly[QueryStringBindable[Option[String]]].javascriptUnbind + """)("set_uris", set_uris2)])})
        }
      """
    )
  
    // @LINE:12
    def similarity: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.SimilarityController.similarity",
      """
        function(method0,minimal1) {
          return _wA({method:"POST", url:"""" + _prefix + { _defaultPrefix } + """" + "similarity/" + (""" + implicitly[PathBindable[String]].javascriptUnbind + """)("method", encodeURIComponent(method0)) + _qS([(""" + implicitly[QueryStringBindable[Option[String]]].javascriptUnbind + """)("minimal", minimal1)])})
        }
      """
    )
  
  }

  // @LINE:6
  class ReverseHomeController(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:6
    def index: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.index",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + """"})
        }
      """
    )
  
  }

  // @LINE:10
  class ReverseAsyncController(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:10
    def message: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.AsyncController.message",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "message"})
        }
      """
    )
  
  }


}

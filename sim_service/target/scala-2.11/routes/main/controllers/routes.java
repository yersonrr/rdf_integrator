
// @GENERATOR:play-routes-compiler
// @SOURCE:/home/roa/internship/rdf_integrator/gades/sim_service/conf/routes
// @DATE:Mon Nov 13 16:20:41 CET 2017

package controllers;

import router.RoutesPrefix;

public class routes {
  
  public static final controllers.ReverseAssets Assets = new controllers.ReverseAssets(RoutesPrefix.byNamePrefix());
  public static final controllers.ReverseCountController CountController = new controllers.ReverseCountController(RoutesPrefix.byNamePrefix());
  public static final controllers.ReverseSimilarityController SimilarityController = new controllers.ReverseSimilarityController(RoutesPrefix.byNamePrefix());
  public static final controllers.ReverseHomeController HomeController = new controllers.ReverseHomeController(RoutesPrefix.byNamePrefix());
  public static final controllers.ReverseAsyncController AsyncController = new controllers.ReverseAsyncController(RoutesPrefix.byNamePrefix());

  public static class javascript {
    
    public static final controllers.javascript.ReverseAssets Assets = new controllers.javascript.ReverseAssets(RoutesPrefix.byNamePrefix());
    public static final controllers.javascript.ReverseCountController CountController = new controllers.javascript.ReverseCountController(RoutesPrefix.byNamePrefix());
    public static final controllers.javascript.ReverseSimilarityController SimilarityController = new controllers.javascript.ReverseSimilarityController(RoutesPrefix.byNamePrefix());
    public static final controllers.javascript.ReverseHomeController HomeController = new controllers.javascript.ReverseHomeController(RoutesPrefix.byNamePrefix());
    public static final controllers.javascript.ReverseAsyncController AsyncController = new controllers.javascript.ReverseAsyncController(RoutesPrefix.byNamePrefix());
  }

}
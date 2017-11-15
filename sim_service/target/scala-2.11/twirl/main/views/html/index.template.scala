
package views.html

import play.twirl.api._
import play.twirl.api.TemplateMagic._


     object index_Scope0 {
import models._
import controllers._
import play.api.i18n._
import views.html._
import play.api.templates.PlayMagic._
import play.api.mvc._
import play.api.data._

class index extends BaseScalaTemplate[play.twirl.api.HtmlFormat.Appendable,Format[play.twirl.api.HtmlFormat.Appendable]](play.twirl.api.HtmlFormat) with play.twirl.api.Template1[String,play.twirl.api.HtmlFormat.Appendable] {

  /*
 * This template takes a single argument, a String containing a
 * message to display.
 */
  def apply/*5.2*/(message: String):play.twirl.api.HtmlFormat.Appendable = {
    _display_ {
      {


Seq[Any](format.raw/*5.19*/("""

"""),format.raw/*11.4*/("""
"""),_display_(/*12.2*/main("Similarity Function for RDF Graphs")/*12.44*/ {_display_(Seq[Any](format.raw/*12.46*/("""

    """),format.raw/*17.8*/("""
    """),format.raw/*18.5*/("""<div>Welcome to similary function service!!!</div>

""")))}),format.raw/*20.2*/("""
"""))
      }
    }
  }

  def render(message:String): play.twirl.api.HtmlFormat.Appendable = apply(message)

  def f:((String) => play.twirl.api.HtmlFormat.Appendable) = (message) => apply(message)

  def ref: this.type = this

}


}

/*
 * This template takes a single argument, a String containing a
 * message to display.
 */
object index extends index_Scope0.index
              /*
                  -- GENERATED --
                  DATE: Mon Nov 13 16:20:41 CET 2017
                  SOURCE: /home/roa/internship/rdf_integrator/gades/sim_service/app/views/index.scala.html
                  HASH: bacf5b77b4745c2ca9ac54665dab7d01034f6005
                  MATRIX: 616->95|728->112|757->308|785->310|836->352|876->354|909->483|941->488|1024->541
                  LINES: 23->5|28->5|30->11|31->12|31->12|31->12|33->17|34->18|36->20
                  -- GENERATED --
              */
          
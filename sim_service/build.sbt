name := """sim-app"""

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  cache,
  ws,
  "org.apache.jena" % "apache-jena-libs" % "3.0.1",
  "org.scalatestplus.play" %% "scalatestplus-play" % "1.5.1" % Test,
  "net.sourceforge.owlapi" % "owlapi-distribution" % "4.1.3",
  "net.sourceforge.owlapi" % "owlexplanation" % "1.1.0",
  "log4j" % "log4j" % "1.2.17",
  "info.debatty" % "java-string-similarity" % "0.23",
  "dk.brics.automaton" % "automaton" % "1.11-8"
)



fork in run := true